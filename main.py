import streamlit as st
from ui import Cabecalho, FormularioServidor

st.set_page_config(page_title="Teste Formulário", layout="centered")

cabecalho = Cabecalho()
form = FormularioServidor()

cabecalho.render()
form.render()
