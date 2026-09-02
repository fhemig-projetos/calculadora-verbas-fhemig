import time
import streamlit as st
from data import ProvedorUsuarios
from streamlit_cookies_controller import CookieController

CHAVE_COOKIE_SESSAO = "token_sessao"
VALIDADE_SESSAO_HORAS = 1

class Login:
    """Tela de login e controle de sessão do usuário autenticado."""

    def __init__(self):
        self._cookies = CookieController()

        if "usuario_logado" not in st.session_state:
            st.session_state["usuario_logado"] = None

        if not self.autenticado():
            self._restaurar_sessao()

    def _restaurar_sessao(self):
        """Restaura o login a partir do cookie de sessão, se houver um válido.

        É isso que mantém o usuário logado após um F5 — por padrão, um
        refresh de página zera o st.session_state, então sem essa restauração
        o usuário cairia na tela de login de novo a cada F5.

        Logo após um F5, o CookieController ainda não teve tempo de receber
        os cookies de volta do navegador (é assíncrono) — a 1ª leitura vem
        vazia mesmo com o cookie existindo de verdade. Por isso, se ainda não
        temos nenhum cookie carregado, forçamos um único rerun (guardado por
        uma flag, pra não entrar em loop) pra dar tempo do valor chegar.
        """
        if not self._cookies.getAll() and not st.session_state.get("_aguardando_cookies"):
            st.session_state["_aguardando_cookies"] = True
            time.sleep(0.3)  # dá tempo do round-trip JS (ler cookie -> devolver pro Python) completar
            st.rerun()
        st.session_state["_aguardando_cookies"] = False

        token = self._cookies.get(CHAVE_COOKIE_SESSAO)
        if not token:
            return

        usuario = ProvedorUsuarios.validar_sessao(token)
        if usuario:
            st.session_state["usuario_logado"] = usuario

    def autenticado(self) -> bool:
        # Retorna True se usuario logou com sucesso, senão retorna False
        return st.session_state["usuario_logado"] is not None

    def render_formulario(self):
        st.markdown("### Login")

        with st.form("form_login"):
            email = st.text_input("E-mail", type="email")
            senha = st.text_input("Senha", type="password")
            enviado = st.form_submit_button("Entrar")

        if enviado:
            usuario = ProvedorUsuarios.autenticar(email, senha)
            if usuario:
                st.session_state["usuario_logado"] = usuario
                token = ProvedorUsuarios.criar_sessao(usuario["id"], validade_horas=VALIDADE_SESSAO_HORAS)
                self._cookies.set(CHAVE_COOKIE_SESSAO, token, max_age=VALIDADE_SESSAO_HORAS * 60 * 60)
                time.sleep(0.3)  # dá tempo do JS gravar o cookie antes do rerun mudar de tela
                st.rerun()
            else:
                st.error("E-mail ou senha incorretos.")

    def render_logout(self):
        usuario = st.session_state["usuario_logado"]
        col_nome, col_botao = st.columns([4, 1], vertical_alignment="center")
        col_nome.caption(f"Logado como **{usuario['nome']}**")
        if col_botao.button("Sair"):
            ProvedorUsuarios.encerrar_sessao(self._cookies.get(CHAVE_COOKIE_SESSAO))
            self._cookies.remove(CHAVE_COOKIE_SESSAO)
            time.sleep(0.3)  # dá tempo do JS remover o cookie antes do rerun mudar de tela
            st.session_state["usuario_logado"] = None
            st.rerun()