import streamlit as st
from data import ProvedorDadosFhemig
from utils import FormatadorCampos, on_change_masp


class FormularioServidor:
    """Formulário de Dados do Servidor.

    Encapsula o estado e a renderização do cabeçalho com dados funcionais
    do servidor (nome, MASP, cargo, vencimento, carga horária, etc.).
    """

    def __init__(self):
        if "dados_servidor" not in st.session_state:
            st.session_state["dados_servidor"] = {
                "nome": "",
                "masp": "",
                "admissao": "1",
                "dt_admissao": "",
                "dt_fim_efetiva": "",
                "cargo_classe": "",
                "cargo_nivel": "",
                "cargo_grau": "",
                "ch_semanal": "",
                "ch_mensal": 0.0,
                "vencimento": 0.0,
            }
            
    def render(self):
        with st.expander("Dados do Servidor", expanded=True):
            ds = st.session_state["dados_servidor"]
            c1, c2, c3 = st.columns(3)

            ds["nome"] = c1.text_input("Nome Completo do Servidor", value=ds["nome"])
            ds["masp"]     = c2.text_input("MASP", value=ds["masp"])
            ds["admissao"] = c3.text_input("Admissão", value=ds["admissao"], help="Ex: 1, 2")



