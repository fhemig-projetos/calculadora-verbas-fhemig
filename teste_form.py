import streamlit as st
from ui import FormularioServidor

st.set_page_config(page_title="Teste Formulário", layout="centered")

form = FormularioServidor()
form.render()
