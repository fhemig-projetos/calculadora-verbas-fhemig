"""Banco SQLite local (um arquivo por computador/usuário do Windows).

Substitui o Supabase: funciona sem rede, sem proxy e sem credenciais embutidas.
Guarda a base de servidores (importada de planilha) e a análise ativa do usuário.
"""
import os
import sqlite3
import sys
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

ESQUEMA = """
CREATE TABLE IF NOT EXISTS servidores (
    masp_admissao      TEXT PRIMARY KEY,
    nome               TEXT NOT NULL,
    masp               TEXT NOT NULL,
    numero_admissao    TEXT NOT NULL,
    data_inicio        TEXT,
    data_fim_efetiva   TEXT,
    cod_carreira       TEXT,
    simbolo_vencimento TEXT,
    nivel              TEXT,
    grau               TEXT,
    carga_horaria      REAL
);
CREATE INDEX IF NOT EXISTS idx_servidores_busca ON servidores (masp, numero_admissao);

-- Uma única análise ativa por computador (salvar sobrescreve a anterior).
CREATE TABLE IF NOT EXISTS analise_ativa (
    id             INTEGER PRIMARY KEY CHECK (id = 1),
    dados_servidor TEXT NOT NULL,
    historico      TEXT NOT NULL,
    atualizado_em  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS meta (
    chave TEXT PRIMARY KEY,
    valor TEXT
);
"""


def caminho_banco() -> Path:
    """Onde fica o calculadora.db.

    - CALCULADORA_DB, se definida, sobrescreve tudo (testes).
    - Rodando do código-fonte (desenvolvimento): data/calculadora.db, dentro do projeto,
      para ficar à vista (o *.db está no .gitignore: tem dados pessoais).
    - No executável: %LOCALAPPDATA%\\CalculadoraFhemig\\calculadora.db.
    """
    personalizado = os.environ.get("CALCULADORA_DB")
    if personalizado:
        caminho = Path(personalizado)
    elif not getattr(sys, "frozen", False):
        caminho = Path(__file__).resolve().parent / "calculadora.db"
    else:
        base = os.environ.get("LOCALAPPDATA") or str(Path.home() / ".local" / "share")
        caminho = Path(base) / "CalculadoraFhemig" / "calculadora.db"
    caminho.parent.mkdir(parents=True, exist_ok=True)
    return caminho


@contextmanager
def conexao() -> Generator[sqlite3.Connection, None, None]:
    """Abre o banco (criando o esquema se preciso); commit ao sair, rollback em caso de erro."""
    con = sqlite3.connect(caminho_banco(), timeout=10)
    con.row_factory = sqlite3.Row
    try:
        con.executescript(ESQUEMA)
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()
