import streamlit as st
from ui import Cabecalho, FormularioServidor, SelecaoVerba

st.set_page_config(page_title="Calculadora de Verbas - Fhemig", page_icon="assets/icone.png", layout="centered")

cabecalho = Cabecalho()
form_servidor = FormularioServidor()
sv = SelecaoVerba()

cabecalho.render()
form_servidor.render()
sv.render()
