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

# session_state["usuario_logado"] é populado quando a classe Login é instanciada
# Puxa o id do usuário na tabela correspondente do banco 
usuario_id = st.session_state["usuario_logado"]["id"]

# Restaura a análise salva no banco (cabeçalho + histórico) 
# Aciona o if e cria o session_state["analise_carregada"] uma única vez a cada nova sessão ou atualização da página (F5) 
# Essa lógica evita de fazer consulta no banco a cada clique ou troca de botão 
# (lógica do streamlit de executar o script da página todo de novo)
if not st.session_state.get("analise_carregada"):
    # Carrega do banco se tiver análise salva 
    analise = ProvedorAnalises.carregar(usuario_id)
    if analise:
        # Carrega o session_state com os dados salvos no banco 
        ds_restaurado = ProvedorAnalises.desserializar_dados_servidor(analise["dados_servidor"])
        st.session_state["dados_servidor"] = ds_restaurado # utilizado em form_servidor.py
        st.session_state["historico"] = analise["historico"] # utilizado em selecao_verba.py

        # Restaura o session_state["ultima_busca_servidor"] usado em form_servidor.py #55
        # Dessa forma MASP/Admissão são restaurados como "já buscados" 
        # Sem isso, aciona uma busca nova a cada F5 (ultima_busca_servidor zerado) e limpa o cabeçalho se não achar correspondência
        if ds_restaurado.get("masp") and ds_restaurado.get("admissao"):
            st.session_state["ultima_busca_servidor"] = (ds_restaurado["masp"], ds_restaurado["admissao"])
    st.session_state["analise_carregada"] = True

form_servidor = FormularioServidor()
sv = SelecaoVerba()

cabecalho.render()
login.render_logout()
form_servidor.render()
sv.render()

# Salva a cada rerun - à cada interação na página passa por aqui (lógica do streamlit) 
# Assim a analise sobrevive a F5/fechar o navegador
ProvedorAnalises.salvar(usuario_id, st.session_state["dados_servidor"], st.session_state["historico"])