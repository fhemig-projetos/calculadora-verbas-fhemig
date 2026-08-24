from typing import Optional
import streamlit as st
from supabase import create_client

NIVEL_ROMANO_PARA_ARABICO = {"I": "1", "II": "2", "III": "3", "IV": "4", "V": "5", "VI": "6"}

@st.cache_resource
def _cliente():
    return create_client(
        st.secrets["supabase_admin"]["url"],
        st.secrets["supabase_admin"]["key"],
    )

class ProvedorServidoresSupabase:
    @staticmethod
    @st.cache_data(show_spinner="Buscando servidor...")
    def buscar_servidor(masp: str, numero_admissao: str) -> Optional[dict]:
        """Busca um servidor no Supabase pelo MASP e Nº de Admissão.

        O campo `nivel` vem em algarismo romano na base (ex: "II"), enquanto
        `tabela_cargos` (data/tabelas.json) usa algarismo arábico — convertido
        aqui para que a busca de cargo (ProvedorDadosFhemig.buscar_cargo) funcione.
        """
        try:
            resposta = (
                _cliente()
                .table("servidores")
                .select("*")
                .eq("masp", masp)
                .eq("numero_admissao", numero_admissao)
                .limit(1)
                .execute()
            )
        except Exception:
            st.warning("⚠️ Não foi possível consultar a base de servidores agora. Preencha os dados manualmente.")
            return None
        if not resposta.data:
            return None
        servidor = resposta.data[0]
        servidor["nivel"] = NIVEL_ROMANO_PARA_ARABICO.get(servidor["nivel"], servidor["nivel"])
        return servidor
