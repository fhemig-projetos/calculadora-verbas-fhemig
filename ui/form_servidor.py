import streamlit as st
from data import ProvedorDadosFhemig, ProvedorServidoresSupabase
from utils import FormatadorCampos, on_change_masp
import datetime

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
                "admissao": "",
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

            ds["masp"]     = c1.text_input("MASP", value=ds["masp"], help="Somente números, sem pontos ou traços." , placeholder="Ex: 12345678", key="masp")
            ds["admissao"] = c2.text_input("Nº de Admissão", value=ds["admissao"], help="Somente números.", placeholder="Ex: 1, 2", key="admissao")

            servidor_encontrado = None
            if ds["masp"] and ds["admissao"]:
                servidor_encontrado = ProvedorServidoresSupabase.buscar_servidor(ds["masp"], ds["admissao"])
                if servidor_encontrado:
                    st.success("✅ Servidor encontrado na base — dados preenchidos automaticamente")
                    ds["nome"] = servidor_encontrado["nome"]
                    if servidor_encontrado["data_inicio"]:
                        ds["dt_admissao"] = datetime.date.fromisoformat(servidor_encontrado["data_inicio"])
                    if servidor_encontrado["data_fim_efetiva"]:
                        ds["dt_fim_efetiva"] = datetime.date.fromisoformat(servidor_encontrado["data_fim_efetiva"])
                    ds["cargo_classe"] = servidor_encontrado["cod_carreira"]
                    ds["cargo_nivel"] = servidor_encontrado["nivel"]
                    ds["cargo_grau"] = servidor_encontrado["grau"]
                    ds["ch_semanal"] = int(servidor_encontrado["carga_horaria"])
                else:
                    st.info("ℹ️ Servidor não encontrado na base. Preencha os dados manualmente.")

            ds["nome"] = c3.text_input("Nome Completo do Servidor", value=ds["nome"], key="nome")

            # Define padrão de data explicitamente
            ds["dt_admissao"] = c4.date_input(
                "Data de Admissão", value=ds["dt_admissao"], format="DD/MM/YYYY",
                min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today(),
            )
            ds["dt_fim_efetiva"] = c5.date_input(
                "Data Fim Efetiva", value=ds["dt_fim_efetiva"], format="DD/MM/YYYY",
                min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today(),
            )

            st.divider()

            st.caption("**Cargo** — preencha para busca automática do vencimento básico e carga horária mensal")
            c6, c7, c8 = st.columns(3)
            ds["cargo_classe"] = c6.text_input("Cargo", value=ds["cargo_classe"], placeholder="Ex: PENF", key="cargo_classe").upper().strip()
            ds["cargo_nivel"]  = c7.text_input("Nível",          value=ds["cargo_nivel"],  placeholder="Ex: 2", key="cargo_nivel").strip()
            ds["cargo_grau"]   = c8.text_input("Grau",           value=ds["cargo_grau"],   placeholder="Ex: A", key="cargo_grau").upper().strip()
            
            c9, c10 = st.columns(2)
            ds["ch_semanal"] = c9.number_input(
                "Carga Horária Semanal", value=ds["ch_semanal"], min_value=0, step=1, key="ch_semanal",
            )

            # Calcula a ch mensal com base na ch semanal informada
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
