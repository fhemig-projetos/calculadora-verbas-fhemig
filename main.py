import streamlit as st
from ui import Cabecalho, FormularioServidor, SelecaoVerba

st.set_page_config(page_title="Teste Formulário", layout="centered")

cabecalho = Cabecalho()
form_servidor = FormularioServidor()
sv = SelecaoVerba()

cabecalho.render()
form_servidor.render()
sv.render()