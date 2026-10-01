import json
import streamlit as st
from ui import Cabecalho, FormularioServidor, SelecaoVerba, BaseServidores
from data import ProvedorAnalises

st.set_page_config(page_title="Calculadora de Verbas - Fhemig", page_icon="assets/icone.png", layout="centered")

cabecalho = Cabecalho()

if "analise_carregada" not in st.session_state:
    # Carrega a análise salva na última sessão (SQLite local deste computador).

    # A checagem dessa flag no session_state é p/ garantir que a leitura só acontece
    # uma vez após abrir o app ou F5 (já que o streamlit roda inteiro a cada interação).
    analise = ProvedorAnalises.carregar()
    if analise:
        # Carrega o session_state com os dados salvos
        ds_restaurado = ProvedorAnalises.desserializar_dados_servidor(analise["dados_servidor"])

        # Carrega os session_state c/ os dados de cada formulário
        st.session_state["dados_servidor"] = ds_restaurado # usado em form_servidor.py
        st.session_state["historico"] = analise["historico"] # usado em selecao_verba.py

        # Correção de bug que limpa o cabeçalho recém-restaurado
        if ds_restaurado.get("masp") and ds_restaurado.get("admissao"):
            st.session_state["ultima_busca_servidor"] = (ds_restaurado["masp"], ds_restaurado["admissao"])

    # Trava consultas futuras nesta mesma sessão
    st.session_state["analise_carregada"] = True

# Renderização dos formulários
form_servidor = FormularioServidor()
sv = SelecaoVerba()
bs = BaseServidores()

cabecalho.render()
bs.render()
form_servidor.render()
sv.render()

# Salva a análise a cada rerun (é o que persiste os dados), mas só grava no disco se mudou
instantaneo = json.dumps(
    [ProvedorAnalises.serializar_dados_servidor(st.session_state["dados_servidor"]), st.session_state["historico"]],
    default=str,
)
if instantaneo != st.session_state.get("_analise_salva"):
    ProvedorAnalises.salvar(st.session_state["dados_servidor"], st.session_state["historico"])
    st.session_state["_analise_salva"] = instantaneo
