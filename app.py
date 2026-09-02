import streamlit as st
from ui import Cabecalho, FormularioServidor, SelecaoVerba, Login

st.set_page_config(page_title="Calculadora de Verbas - Fhemig", page_icon="assets/icone.png", layout="centered")

cabecalho = Cabecalho()
login = Login()

if not login.autenticado():
    cabecalho.render()
    login.render_formulario()
    st.stop()

form_servidor = FormularioServidor()
sv = SelecaoVerba()

cabecalho.render()
login.render_logout()
form_servidor.render()
sv.render()