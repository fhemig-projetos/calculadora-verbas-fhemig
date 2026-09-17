import streamlit as st
from ui import Cabecalho, FormularioServidor, SelecaoVerba, Login
from data import ProvedorAnalises

st.set_page_config(page_title="Calculadora de Verbas - Fhemig", page_icon="assets/icone.png", layout="centered")

cabecalho = Cabecalho()

# Dispara tentativa de restaurar sessão no init
login = Login()

# Se realmente não tem usuário logado renderiza o formulário de login
if not login.autenticado():
    cabecalho.render()
    login.render_formulario()
    st.stop()

# Após validar o login do usuário, busca o id associado a ele
usuario_id = st.session_state["usuario_logado"]["id"]

if "analise_carregada" not in st.session_state:
    # Carregar análise salva na última sessão do usuário.

    # A checagem dessa flag no session_state é p/ garantir que a busca no banco só acontece
    # uma vez após login ou F5 (já que o streamlit roda inteiro a cada interação).

    # Carrega do banco se tiver análise salva 
    analise = ProvedorAnalises.carregar(usuario_id)
    if analise:
        # Carrega o session_state com os dados salvos no banco 
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

cabecalho.render()
login.render_logout()
form_servidor.render()
sv.render()

# Salva os dados no banco a cada rerun (é o que persiste os dados)
ProvedorAnalises.salvar(usuario_id, st.session_state["dados_servidor"], st.session_state["historico"])