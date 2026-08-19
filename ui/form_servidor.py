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
                "dt_admissao": None,
                "dt_fim_efetiva": None,
                "cargo_classe": "",
                "cargo_nivel": "",
                "cargo_grau": "",
                "ch_semanal": 0,
                "ch_mensal": 0,
                "vencimento_basico": 0.0,
            }

    def render(self):
        with st.expander("Dados do Servidor", expanded=True):
            ds = st.session_state["dados_servidor"]
            c1, c2, c3 = st.columns(3)
            c4, c5 = st.columns(2)

            ds["nome"] = c1.text_input("Nome Completo do Servidor", value=ds["nome"])
            ds["masp"]     = c2.text_input("MASP", value=ds["masp"])
            ds["admissao"] = c3.text_input("Nº de Admissão", value=ds["admissao"], help="Ex: 1, 2")
            ds["dt_admissao"] = c4.date_input("Data de Admissão", value=ds["dt_admissao"], format="DD/MM/YYYY")
            ds["dt_fim_efetiva"] = c5.date_input("Data Fim Efetiva", value=ds["dt_fim_efetiva"], format="DD/MM/YYYY")

            st.divider()

            st.caption("**Cargo** — preencha para busca automática do vencimento básico e carga horária mensal")
            c6, c7, c8 = st.columns(3)
            ds["cargo_classe"] = c6.text_input("Cargo", value=ds["cargo_classe"], placeholder="Ex: PENF").upper().strip()
            ds["cargo_nivel"]  = c7.text_input("Nível",          value=ds["cargo_nivel"],  placeholder="Ex: 2").strip()
            ds["cargo_grau"]   = c8.text_input("Grau",           value=ds["cargo_grau"],   placeholder="Ex: A").upper().strip()
            
            c9, c10 = st.columns(2)
            ds["ch_semanal"]   = c9.selectbox(
                "Carga Horária Semanal",
                options=[20, 30, 40, 44],
                index=2
            )

            # Calcula a ch mensal com base na ch semanal selecionada (por default ch_semanal == 40h) 
            ds["ch_mensal"] = int(ds["ch_semanal"] / 5 * 30)
            c10.number_input("Carga Horária Mensal", value=ds["ch_mensal"], disabled=True)

            cargo_encontrado = None
            # Se campos preenchidos
            if ds["cargo_classe"] and ds["cargo_nivel"] and ds["cargo_grau"] and ds["ch_semanal"] != "- Selecione -":
                # Busca o cargo
                cargo_encontrado = ProvedorDadosFhemig.buscar_cargo(ds["cargo_classe"], ds["cargo_nivel"], ds["cargo_grau"], ds["ch_semanal"])

                # Se cargo encontrado retorna valores
                if cargo_encontrado:
                    ds["vencimento_basico"] = cargo_encontrado["vencimento_basico"]
                    st.success(
                        f"✅ Cargo encontrado\n\n"
                        f"Vencimento: **R$ {cargo_encontrado['vencimento_basico']:,.2f}** · "
                        f"Vigência: **{cargo_encontrado['dt_inicio']}**"
                    )
                # Se cargo não encontrado abre campos para preenchimento
                else:
                    st.warning("⚠️ Cargo não encontrado na tabela. Preencha o vencimento básico manualmente abaixo.")
                    ds["vencimento_basico"] = st.number_input("Vencimento Básico (R$)", value=0.0, format="%.2f")
