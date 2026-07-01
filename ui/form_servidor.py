import streamlit as st
from data import ProvedorDadosFhemig
from utils import FormatadorCampos, on_change_masp
from datetime import date

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
            c4, c5 = st.columns(2)

            ds["nome"] = c1.text_input("Nome Completo do Servidor", value=ds["nome"])
            ds["masp"]     = c2.text_input("MASP", value=ds["masp"])
            ds["admissao"] = c3.text_input("Admissão", value=ds["admissao"], help="Ex: 1, 2")
            ds["dt_admissao"] = c4.date_input("Data de Admissão", value=None, format="DD/MM/YYYY")
            ds["dt_fim"] = c5.date_input("Data Fim Efetiva", value=None, format="DD/MM/YYYY")

            st.divider()

            st.caption("**Cargo** — preencha para busca automática do vencimento e carga horária")
            c6, c7, c8, c9 = st.columns(4)
            cargo_classe = c6.text_input("Cargo / Classe", value=ds["cargo_classe"], placeholder="Ex: PENF").upper().strip()
            cargo_nivel  = c7.text_input("Nível",          value=ds["cargo_nivel"],  placeholder="Ex: 2").strip()
            cargo_grau   = c8.text_input("Grau",           value=ds["cargo_grau"],   placeholder="Ex: A").upper().strip()
            ch_semanal   = c9.selectbox(
                "C.H. Semanal",
                options=["- Selecione -", "20 Horas Semanais", "30 Horas Semanais", "40 Horas Semanais", "44 Horas Semanais"],
                key="ch_semanal_select"
            )

            cargo_encontrado = None
            if cargo_classe and cargo_nivel and cargo_grau and ch_semanal != "- Selecione -":
                cargo_encontrado = ProvedorDadosFhemig.buscar_cargo(cargo_classe, cargo_nivel, cargo_grau, ch_semanal)

            if cargo_encontrado:
                pass






