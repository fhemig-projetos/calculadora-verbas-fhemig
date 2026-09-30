"""
Launcher do executável Windows: sobe o servidor Streamlit local e abre o navegador.

Como funciona quando empacotado pelo PyInstaller:
- sys._MEIPASS aponta para a pasta temporária onde o PyInstaller extraiu os arquivos
  (app.py, ui/, data/, calculadoras/, utils/, assets/, .streamlit/config.toml).
- Chamamos o Streamlit via API interna (bootstrap), não via subprocess, para não
  depender de um segundo binário python/streamlit solto no PATH do usuário.
- secrets.toml é empacotado junto (ver build_exe.md). Se existir um secrets.toml ao
  lado do .exe, ele tem prioridade sobre o embutido (permite trocar credenciais
  sem refazer o build).
"""
import os
import socket
import sys
import threading
import webbrowser


def caminho_base() -> str:
    if getattr(sys, "frozen", False):
        return sys._MEIPASS  # type: ignore[attr-defined]
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def pasta_config_usuario() -> str:
    """Pasta ao lado do .exe onde fica o secrets.toml real (não embutido no binário)."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def porta_livre(preferida: int = 8501) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", preferida))
            return preferida
        except OSError:
            s.bind(("127.0.0.1", 0))
            return s.getsockname()[1]


def localizar_secrets(base: str, pasta_config: str) -> str:
    """Prefere o secrets.toml ao lado do .exe; senão usa o embutido no bundle."""
    for pasta in (pasta_config, base):
        caminho = os.path.join(pasta, ".streamlit", "secrets.toml")
        if os.path.isfile(caminho):
            return caminho
    print(
        "\n[ERRO] Arquivo de configuração 'secrets.toml' não encontrado nem ao lado\n"
        "do executável nem dentro dele. Refaça o build com o arquivo presente.\n"
    )
    input("Pressione ENTER para sair...")
    sys.exit(1)


def main() -> None:
    base = caminho_base()
    pasta_config = pasta_config_usuario()

    os.chdir(base)
    # Streamlit procura .streamlit/secrets.toml relativo ao cwd por padrão;
    # apontamos explicitamente para a pasta do usuário via env var
    # (opção "secrets.files" é `multiple=True` -> STREAMLIT_SECRETS_FILES, no plural).
    os.environ["STREAMLIT_SECRETS_FILES"] = localizar_secrets(base, pasta_config)

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

    def abrir_navegador():
        webbrowser.open_new(url)

    threading.Timer(1.5, abrir_navegador).start()

    from streamlit.web import cli as stcli
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
