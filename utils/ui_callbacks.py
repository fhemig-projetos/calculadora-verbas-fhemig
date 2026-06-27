import streamlit as st
from utils import FormatadorCampos

def on_change_masp(key: str):
    raw = st.session_state.get(key)
    st.session_state[key] = FormatadorCampos.masp(raw)

def on_change_moeda(key: str):
    raw = st.session_state.get(key)
    st.session_state[key] = FormatadorCampos.arredondar_moeda(raw)