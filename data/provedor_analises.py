import json
from datetime import date, datetime
from typing import Optional

from .armazenamento_local import conexao

CAMPOS_DATA = ("dt_admissao", "dt_fim_efetiva")

class ProvedorAnalises:
    """Persiste, no SQLite local, a análise ativa (dados do servidor + histórico de cálculos).

    Só existe uma análise ativa por computador — a tabela tem uma única linha
    (id = 1), então salvar sempre sobrescreve a anterior (não há conceito de
    "várias análises salvas" por decisão do usuário).
    """

    @staticmethod
    def carregar() -> Optional[dict]:
        """Busca a análise salva. Retorna None se nunca salvou nada (ou se o arquivo estiver ilegível)."""
        try:
            with conexao() as con:
                linha = con.execute(
                    "SELECT dados_servidor, historico FROM analise_ativa WHERE id = 1"
                ).fetchone()
            if linha is None:
                return None
            return {
                "dados_servidor": json.loads(linha["dados_servidor"]),
                "historico": json.loads(linha["historico"]),
            }
        except Exception:
            return None

    @staticmethod
    def salvar(dados_servidor: dict, historico: list) -> None:
        """Grava (upsert) a análise ativa.

        Falha silenciosa: um erro de disco aqui não deve travar a aplicação,
        já que a análise ainda está íntegra em st.session_state.
        """
        try:
            with conexao() as con:
                con.execute(
                    "INSERT INTO analise_ativa (id, dados_servidor, historico, atualizado_em) "
                    "VALUES (1, ?, ?, ?) "
                    "ON CONFLICT(id) DO UPDATE SET dados_servidor = excluded.dados_servidor, "
                    "historico = excluded.historico, atualizado_em = excluded.atualizado_em",
                    (
                        json.dumps(ProvedorAnalises.serializar_dados_servidor(dados_servidor)),
                        json.dumps(historico),
                        datetime.now().isoformat(timespec="seconds"),
                    ),
                )
        except Exception:
            pass

    @staticmethod
    def serializar_dados_servidor(ds: dict) -> dict:
        """Converte os campos de data (datetime.date) para string ISO, serializável em JSON."""
        serializado = dict(ds)
        for campo in CAMPOS_DATA:
            valor = serializado.get(campo)
            serializado[campo] = valor.isoformat() if valor else None
        return serializado

    @staticmethod
    def desserializar_dados_servidor(ds: dict) -> dict:
        """Converte os campos de data (string ISO, vindos do banco) de volta para datetime.date."""
        desserializado = dict(ds)
        for campo in CAMPOS_DATA:
            valor = desserializado.get(campo)
            desserializado[campo] = date.fromisoformat(valor) if valor else None
        return desserializado
