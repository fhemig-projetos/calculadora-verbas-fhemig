# PyInstaller spec — build no Windows com:
#   pyinstaller desktop/calculadora.spec --clean
#
# Gera dist/CalculadoraVerbasFhemig/CalculadoraVerbasFhemig.exe (modo --onedir,
# recomendado: --onefile funciona mas fica mais lento para abrir, pois
# descompacta tudo a cada execução).
#
# IMPORTANTE: secrets.toml NÃO entra aqui de propósito (ver ../docs/build_exe.md).
# O usuário final recebe/monta esse arquivo separadamente, ao lado do .exe.

import sys
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

RAIZ = Path(__file__).resolve().parent.parent

datas = [
    (str(RAIZ / "assets"), "assets"),
    (str(RAIZ / "data" / "tabelas.json"), "data"),
    (str(RAIZ / ".streamlit" / "config.toml"), ".streamlit"),
]
# streamlit e supabase carregam vários arquivos estáticos/metadados via importlib;
# sem isso o exe sobe mas quebra na primeira tela com "module not found" silencioso.
datas += collect_data_files("streamlit")
datas += collect_data_files("supabase")

hiddenimports = (
    collect_submodules("streamlit")
    + collect_submodules("supabase")
    + [
        "reportlab.graphics.barcode",
        "bcrypt",
        "streamlit_cookies_controller",
    ]
)

a = Analysis(
    [str(Path(__file__).parent / "launcher.py")],
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
