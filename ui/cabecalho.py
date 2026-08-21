import streamlit as st


class Cabecalho:

    def render(cls):
        col_logo, col_titulo = st.columns([1, 5], vertical_alignment="center")
        with col_logo:
            st.image("assets/LogoFhemig.png", width=200)
        with col_titulo:
            st.markdown("### Calculadora de Verbas Remuneratórias")
            st.markdown("**FHEMIG · DIGEPE / CCPT** — Resumos Funcionais")
        st.divider()
