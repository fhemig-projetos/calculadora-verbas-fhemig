"""
Launcher do executável Windows: sobe o servidor Streamlit local e abre uma janela de app.

Como funciona quando empacotado pelo PyInstaller:
- sys._MEIPASS aponta para a pasta temporária onde o PyInstaller extraiu os arquivos
  (app.py, ui/, data/, calculadoras/, utils/, assets/, .streamlit/config.toml).
- Chamamos o Streamlit via API interna (bootstrap), não via subprocess, para não
  depender de um segundo binário python/streamlit solto no PATH do usuário.
- O app não usa rede nem credenciais: histórico e base de servidores ficam em um SQLite
  local (%LOCALAPPDATA%/CalculadoraFhemig/calculadora.db, ver data/armazenamento_local.py).
"""
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import webbrowser


def caminho_base() -> str:
    if getattr(sys, "frozen", False):
        return sys._MEIPASS  # type: ignore[attr-defined]
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def porta_livre(preferida: int = 8501) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", preferida))
            return preferida
        except OSError:
            s.bind(("127.0.0.1", 0))
            return s.getsockname()[1]


def mostrar_erro(mensagem: str) -> None:
    """Sem console não há onde imprimir: mostra caixa de diálogo (e grava no log)."""
    print(f"[ERRO] {mensagem}", file=sys.stderr)
    if sys.platform == "win32":
        import ctypes

        ctypes.windll.user32.MessageBoxW(0, mensagem, "Calculadora de Verbas - Fhemig", 0x10)


def redirecionar_saida_para_log() -> None:
    """Em build sem console (console=False) stdout/stderr são None e quebram o Streamlit."""
    if not getattr(sys, "frozen", False) or (sys.stdout and sys.stderr):
        return
    pasta = os.path.join(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()), "CalculadoraFhemig")
    os.makedirs(pasta, exist_ok=True)
    log = open(os.path.join(pasta, "app.log"), "a", encoding="utf-8", buffering=1)
    sys.stdout = sys.stderr = log


def _localizar_navegador_app() -> str | None:
    """Chrome (preferido) ou Edge (presente em todo Windows 10/11), p/ abrir em modo janela de app."""
    pastas = [os.environ.get(v) for v in ("PROGRAMFILES(X86)", "PROGRAMFILES", "LOCALAPPDATA")]
    relativos = (
        r"Google\Chrome\Application\chrome.exe",
        r"Microsoft\Edge\Application\msedge.exe",
    )
    for relativo in relativos:
        for pasta in filter(None, pastas):
            caminho = os.path.join(pasta, relativo)
            if os.path.isfile(caminho):
                return caminho
    return None


def _abrir_janela_app(url: str) -> None:
    """Abre o app numa janela sem barra de endereço (--app). Fechar a janela encerra tudo.

    Usa um perfil temporário próprio para o processo ser independente do navegador
    do usuário; assim sabemos quando a janela fechou e podemos derrubar o servidor.
    Sem Edge/Chrome, cai no navegador padrão (e o servidor segue até fechar o console).
    """
    navegador = _localizar_navegador_app()
    if navegador is None:
        webbrowser.open_new(url)
        return

    perfil = tempfile.mkdtemp(prefix="calculadora_fhemig_")
    processo = subprocess.Popen([
        navegador,
        f"--app={url}",
        f"--user-data-dir={perfil}",
        "--no-first-run",
        "--no-default-browser-check",
        "--window-size=1280,860",
    ])
    processo.wait()
    shutil.rmtree(perfil, ignore_errors=True)
    os._exit(0)  # derruba o servidor Streamlit (roda na thread principal)


def main() -> None:
    redirecionar_saida_para_log()
    base = caminho_base()

    os.chdir(base)

    porta = porta_livre()
    url = f"http://localhost:{porta}"

    sys.argv = [
        "streamlit",
        "run",
        os.path.join(base, "app.py"),
        "--server.port", str(porta),
        "--server.address", "localhost",
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false",
        "--global.developmentMode", "false",
    ]

    def abrir_janela():
        _abrir_janela_app(url)

    threading.Timer(1.5, abrir_janela).start()

    from streamlit.web import cli as stcli
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
