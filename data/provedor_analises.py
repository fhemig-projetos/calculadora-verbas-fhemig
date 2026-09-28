from datetime import date
from typing import Optional
import streamlit as st
from supabase import create_client

@st.cache_resource
def _cliente():
    return create_client(
        st.secrets["supabase_admin"]["url"],
        st.secrets["supabase_admin"]["key"],
    )

CAMPOS_DATA = ("dt_admissao", "dt_fim_efetiva")

class ProvedorAnalises:
    """Persiste a análise ativa (dados do servidor + histórico de cálculos) de cada usuário.

    Só existe uma análise ativa por usuário — `usuario_id` é a chave primária
    da tabela, então salvar sempre sobrescreve a análise anterior (não há
    conceito de "várias análises salvas" por decisão do usuário).
    """

    @staticmethod
    def carregar(usuario_id) -> Optional[dict]:
        """Busca a análise salva de um usuário. Retorna None se nunca salvou nada."""
        try:
            resposta = (
                _cliente()
                .table("analises")
                .select("dados_servidor, historico")
                .eq("usuario_id", usuario_id)
                .limit(1)
                .execute()
            )
        except Exception:
            return None

        return resposta.data[0] if resposta.data else None

    @staticmethod
    def salvar(usuario_id, dados_servidor: dict, historico: list) -> None:
        """Grava (upsert) a análise ativa do usuário.

        Falha silenciosa: um erro de rede aqui não deve travar a aplicação,
        já que a análise ainda está íntegra em st.session_state.
        """
        try:
            _cliente().table("analises").upsert({
                "usuario_id": usuario_id,
                "dados_servidor": ProvedorAnalises.serializar_dados_servidor(dados_servidor),
                "historico": historico,
            }, on_conflict="usuario_id").execute()
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
