import streamlit as st
from data import ProvedorDadosFhemig, ProvedorServidoresSupabase
from utils import FormatadorCampos, on_change_masp, on_change_maiusculo_strip, on_change_strip
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
        if "servidor_nonce" not in st.session_state:
            st.session_state["servidor_nonce"] = 0

        if "ultima_busca_servidor" not in st.session_state:
            st.session_state["ultima_busca_servidor"] = None

    def render(self):
        with st.expander("Dados do Servidor", expanded=True):
            ds = st.session_state["dados_servidor"]

            c1, c2, c3 = st.columns(3)
            c4, c5 = st.columns(2)

            ds["masp"]     = c1.text_input("MASP", value=ds["masp"], help="Somente números, sem pontos ou traços." , placeholder="Ex: 12345678", key="masp")
            ds["admissao"] = c2.text_input("Nº de Admissão", value=ds["admissao"], help="Somente números.", placeholder="Ex: 1, 2", key="admissao")

            servidor_encontrado = None
            if ds["masp"] and ds["admissao"]:
                busca_atual = (ds["masp"], ds["admissao"])

                # Pula a lógica de busca caso os campos masp e admissão não tiverem sido alterados
                # Sem isso, buscaria a cada rerun
                # Evita consultas no banco desnecessárias
                if busca_atual != st.session_state["ultima_busca_servidor"]:
                    st.session_state["ultima_busca_servidor"] = busca_atual
                    servidor_encontrado = ProvedorServidoresSupabase.buscar_servidor(ds["masp"], ds["admissao"])
                    st.session_state["servidor_nonce"] += 1

                if servidor_encontrado:
                    st.success("✅ Servidor encontrado na base — dados preenchidos automaticamente")
                    ds["nome"] = servidor_encontrado["nome"]
                    ds["dt_admissao"] = (
                        datetime.date.fromisoformat(servidor_encontrado["data_inicio"])
                        if servidor_encontrado["data_inicio"] else None
                    )
                    ds["dt_fim_efetiva"] = (
                        datetime.date.fromisoformat(servidor_encontrado["data_fim_efetiva"])
                        if servidor_encontrado["data_fim_efetiva"] else None
                    )

                    ds["cargo_classe"] = servidor_encontrado["cod_carreira"]
                    ds["cargo_nivel"] = servidor_encontrado["nivel"]
                    ds["cargo_grau"] = servidor_encontrado["grau"]
                    ds["ch_semanal"] = int(servidor_encontrado["carga_horaria"])
                else:
                    # Não encontrado: limpa os dados da busca anterior, para não deixar
                    # dados de outro servidor associados ao MASP/Admissão atual
                    st.info("ℹ️ Servidor não encontrado na base. Preencha os dados manualmente.")
                    ds["nome"] = ""
                    ds["dt_admissao"] = None
                    ds["dt_fim_efetiva"] = None
                    ds["cargo_classe"] = ""
                    ds["cargo_nivel"] = ""
                    ds["cargo_grau"] = ""
                    ds["ch_semanal"] = 0

            # Lido só após o bloco de busca, já com o nonce incrementado nesta
            # rodada (se houve busca nova) — os campos abaixo nascem com key
            # nova e aceitam o value= atualizado sem esperar mais um rerun.
            nonce = st.session_state.get("servidor_nonce")
            ds["nome"] = c3.text_input("Nome Completo do Servidor", value=ds["nome"], key=f"{nonce}::nome")

            # Define padrão de data explicitamente
            ds["dt_admissao"] = c4.date_input(
                "Data de Admissão", value=ds["dt_admissao"], format="DD/MM/YYYY",
                min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today(), 
                key=f"{nonce}::dt_admissao"
            )
            ds["dt_fim_efetiva"] = c5.date_input(
                "Data Fim Efetiva", value=ds["dt_fim_efetiva"], format="DD/MM/YYYY",
                min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today(),
                key=f"{nonce}::dt_fim_efetiva"
            )

            st.divider()

            st.caption("**Cargo** — preencha para busca automática do vencimento básico e carga horária mensal")
            c6, c7, c8 = st.columns(3)

            # Campos com on_change não podem receber value= (Streamlit acusa
            # warning de conflito entre os dois). A semente do valor é escrita
            # direto em session_state[key], só na primeira vez que a key existe
            # (ou seja, só quando o nonce muda) — por isso a guarda abaixo.
            key_cargo_classe = f"{nonce}::cargo_classe"
            key_cargo_nivel = f"{nonce}::cargo_nivel"
            key_cargo_grau = f"{nonce}::cargo_grau"

            if key_cargo_classe not in st.session_state:
                st.session_state[key_cargo_classe] = ds["cargo_classe"]

            if key_cargo_nivel not in st.session_state:
                st.session_state[key_cargo_nivel] = ds["cargo_nivel"]

            if key_cargo_grau not in st.session_state:
                st.session_state[key_cargo_grau] = ds["cargo_grau"]

            ds["cargo_classe"] = c6.text_input("Cargo", placeholder="Ex: PENF", key=key_cargo_classe, on_change=on_change_maiusculo_strip, args=(key_cargo_classe,))
            ds["cargo_nivel"]  = c7.text_input("Nível",          placeholder="Ex: 2", key=key_cargo_nivel, on_change=on_change_strip, args=(key_cargo_nivel,))
            ds["cargo_grau"]   = c8.text_input("Grau",           placeholder="Ex: A", key=key_cargo_grau, on_change=on_change_maiusculo_strip, args=(key_cargo_grau,))

            c9, c10 = st.columns(2)
            ds["ch_semanal"] = c9.number_input(
                "Carga Horária Semanal", value=ds["ch_semanal"], min_value=0, step=1,
                key=f"{nonce}::ch_semanal")

            # Calcula a ch mensal com base na ch semanal informada
            ds["ch_mensal"] = int(ds["ch_semanal"] / 5 * 30)
            c10.number_input("Carga Horária Mensal", value=ds["ch_mensal"], disabled=True, key=f"{nonce}::ch_mensal")

            cargo_encontrado = None
            # Se campos preenchidos
            if ds["cargo_classe"] and ds["cargo_nivel"] and ds["cargo_grau"] and ds["ch_semanal"]:
                # Busca o cargo
                cargo_encontrado = ProvedorDadosFhemig.buscar_cargo(ds["cargo_classe"], ds["cargo_nivel"], ds["cargo_grau"], ds["ch_semanal"])
                # Se cargo encontrado retorna valor do vencimento básico e deixa o campo editável
                if cargo_encontrado:
                    st.success(
                        f"✅ Cargo encontrado. Vencimento básico pré-preenchido!\n\n"
                    )
                    ds["vencimento_basico"] = st.number_input("Vencimento Básico (R$)", value=cargo_encontrado["vencimento_basico"], format="%.2f", key=f"{nonce}::vencimento_basico")
                # Se cargo não encontrado abre campos para preenchimento
                else:
                    st.warning("⚠️ Cargo não encontrado na tabela. Preencha o vencimento básico manualmente abaixo.")
                    ds["vencimento_basico"] = st.number_input("Vencimento Básico (R$)", value=0.0, format="%.2f", key=f"{nonce}::vencimento_basico")