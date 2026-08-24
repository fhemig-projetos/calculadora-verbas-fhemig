import csv
import tomllib
from datetime import datetime
from supabase import create_client

with open(".streamlit/secrets.toml", "rb") as f:
    secrets = tomllib.load(f)

supabase = create_client(
    secrets["supabase_admin"]["url"],
    secrets["supabase_admin"]["key"],
)

def parse_data(raw):
    if not raw or not raw.strip():
        return None
    return datetime.strptime(raw.split(" ")[0], "%Y/%m/%d").date().isoformat()

with open("data/dados_funcionais_calculadora_verbas.csv", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    registros = [{
        "nome": r["Nome Servidor"].strip(),
        "masp": r["MASP"].strip(),
        "numero_admissao": r["Nº Admissão"].strip(),
        "masp_admissao": r["Masp/Admissão"].strip(),
        "data_inicio": parse_data(r["Data Inicio"]),
        "data_fim_efetiva": parse_data(r["Data Fim Efetiva"]),
        "cod_carreira": r["Cod Carreira"].strip(),
        "simbolo_vencimento": r["Símbolo Vencimento"].strip(),
        "nivel": r["Nivel"].strip(),
        "grau": r["Grau"].strip(),
        "carga_horaria": float(r["Carga Horária Pagamento"] or 0),
    } for r in reader]

registros_unicos = {r["masp_admissao"]: r for r in registros}
registros = list(registros_unicos.values())

print(f"Preparando {len(registros)} registros...")

for i in range(0, len(registros), 500):
    lote = registros[i:i+500]
    supabase.table("servidores").upsert(lote, on_conflict="masp_admissao").execute()
    print(f"Lote {i//500 + 1} enviado ({len(lote)} registros)")

print("Importação concluída.")