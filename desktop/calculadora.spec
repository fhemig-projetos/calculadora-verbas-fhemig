# PyInstaller spec — build no Windows com:
#   pyinstaller desktop/calculadora.spec --clean
#
# Gera dist/CalculadoraVerbasFhemig/CalculadoraVerbasFhemig.exe (modo --onedir,
# recomendado: --onefile funciona mas fica mais lento para abrir, pois
# descompacta tudo a cada execução).
#
# O app não embute credenciais: histórico e base de servidores ficam num SQLite local
# (%LOCALAPPDATA%/CalculadoraFhemig/calculadora.db). Ver desktop/build_exe.md.

import sys
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_submodules, copy_metadata

# __file__ não existe em .spec (o PyInstaller usa exec); SPECPATH é a pasta do spec.
RAIZ = Path(SPECPATH).resolve().parent

datas = [
    (str(RAIZ / "assets"), "assets"),
    (str(RAIZ / "data" / "tabelas.json"), "data"),
]
# config.toml é opcional (o projeto pode não ter; o launcher já passa as opções por CLI).
_config_toml = RAIZ / ".streamlit" / "config.toml"
if _config_toml.is_file():
    datas.append((str(_config_toml), ".streamlit"))
# streamlit carrega vários arquivos estáticos/metadados via importlib;
# sem isso o exe sobe mas quebra na primeira tela com "module not found" silencioso.
datas += collect_data_files("streamlit")
# zoneinfo no Windows depende dos dados do pacote tzdata (usado em utils/exportador_pdf.py).
datas += collect_data_files("tzdata")
# streamlit lê a própria versão (e a de dependências) via importlib.metadata; sem os
# *.dist-info no bundle dá PackageNotFoundError na importação.
datas += copy_metadata("streamlit", recursive=True)

hiddenimports = (
    collect_submodules("streamlit")
    + collect_submodules("reportlab")
    # pandas.read_excel carrega o openpyxl dinamicamente (importação da base de servidores).
    + collect_submodules("openpyxl")
    # O código da app (app.py, ui/, data/, ...) entra como DADOS, então o PyInstaller
    # não enxerga os imports dele: módulos da stdlib usados só lá precisam ser listados.
    + [
        "sqlite3",
        "zoneinfo",
        "reportlab.graphics.barcode",
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
    console=True,  # sem janela de console; logs vão p/ %LOCALAPPDATA%\CalculadoraFhemig\app.log (ver launcher.py)
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
