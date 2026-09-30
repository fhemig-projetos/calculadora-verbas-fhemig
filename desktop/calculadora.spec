# PyInstaller spec — build no Windows com:
#   pyinstaller desktop/calculadora.spec --clean
#
# Gera dist/CalculadoraVerbasFhemig/CalculadoraVerbasFhemig.exe (modo --onedir,
# recomendado: --onefile funciona mas fica mais lento para abrir, pois
# descompacta tudo a cada execução).
#
# ATENÇÃO: este build EMPACOTA .streamlit/secrets.toml dentro do .exe (decisão do
# responsável pelo projeto, para distribuição às unidades). Tudo que está no .exe
# é extraível por qualquer pessoa que o receba (ver ../docs/build_exe.md).

import sys
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_submodules, copy_metadata

# __file__ não existe em .spec (o PyInstaller usa exec); SPECPATH é a pasta do spec.
RAIZ = Path(SPECPATH).resolve().parent

datas = [
    (str(RAIZ / "assets"), "assets"),
    (str(RAIZ / "data" / "tabelas.json"), "data"),
]
_secrets_toml = RAIZ / ".streamlit" / "secrets.toml"
if not _secrets_toml.is_file():
    raise SystemExit(
        f"secrets.toml não encontrado em {_secrets_toml}. "
        "Copie-o para .streamlit/ antes de rodar o build."
    )
datas.append((str(_secrets_toml), ".streamlit"))
# config.toml é opcional (o projeto pode não ter; o launcher já passa as opções por CLI).
_config_toml = RAIZ / ".streamlit" / "config.toml"
if _config_toml.is_file():
    datas.append((str(_config_toml), ".streamlit"))
# streamlit e supabase carregam vários arquivos estáticos/metadados via importlib;
# sem isso o exe sobe mas quebra na primeira tela com "module not found" silencioso.
datas += collect_data_files("streamlit")
datas += collect_data_files("supabase")
# zoneinfo no Windows depende dos dados do pacote tzdata (usado em utils/exportador_pdf.py).
datas += collect_data_files("tzdata")
# streamlit lê a própria versão (e a de dependências) via importlib.metadata; sem os
# *.dist-info no bundle dá PackageNotFoundError na importação.
datas += copy_metadata("streamlit", recursive=True)
datas += copy_metadata("supabase", recursive=True)

hiddenimports = (
    collect_submodules("streamlit")
    + collect_submodules("supabase")
    + collect_submodules("reportlab")
    # O código da app (app.py, ui/, data/, ...) entra como DADOS, então o PyInstaller
    # não enxerga os imports dele: módulos da stdlib usados só lá precisam ser listados.
    + [
        "email.mime.text",
        "email.mime.multipart",
        "email.mime.base",
        "smtplib",
        "ssl",
        "secrets",
        "zoneinfo",
        "reportlab.graphics.barcode",
        "bcrypt",
        "streamlit_cookies_controller",
    ]
)

a = Analysis(
    [str(Path(SPECPATH) / "launcher.py")],
    pathex=[str(RAIZ)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

# Módulos da própria aplicação (app.py, ui/, data/, calculadoras/, utils/)
# precisam ser copiados como dados (não como pacotes Python do bundle) porque
# o launcher os localiza via caminho relativo, não via import.
codigo_app = [
    "app.py",
    "ui",
    "data",
    "calculadoras",
    "utils",
]
for item in codigo_app:
    origem = RAIZ / item
    if origem.is_file():
        a.datas.append((item, str(origem), "DATA"))
    else:
        for arquivo in origem.rglob("*.py"):
            destino = str(arquivo.relative_to(RAIZ))
            a.datas.append((destino, str(arquivo), "DATA"))

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="CalculadoraVerbasFhemig",
    debug=False,
    strip=False,
    upx=False,
    console=True,  # mantenha True no começo p/ ver erros; troque p/ False quando estabilizar
    # PyInstaller exige .ico no Windows (não aceita .png) — converta antes do build,
    # ver docs/build_exe.md. Se o arquivo não existir, comente esta linha.
    icon=str(RAIZ / "desktop" / "icone.ico") if sys.platform == "win32" else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name="CalculadoraVerbasFhemig",
)
