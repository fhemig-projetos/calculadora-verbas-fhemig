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
            """
            Se ainda não tem ninguém logado pelo session_state, tenta descobrir se tinha
            alguém logado pelo cookie.
            """
            self._restaurar_sessao()

    def _restaurar_sessao(self):
        """Restaura o login a partir do cookie de sessão, se houver um válido.

        É isso que mantém o usuário logado após um F5 — por padrão, um refresh de página
        zera o st.session_state, então sem essa restauração o usuário cairia na tela de
        login de novo a cada F5.
        """
        # Delay proposital para carregar o cookie
        if not self._cookies.getAll() and not st.session_state.get("_aguardando_cookies"):
            st.session_state["_aguardando_cookies"] = True
            time.sleep(0.3)  # dá tempo do round-trip JS (ler cookie -> devolver pro Python) completar
            st.rerun()
        st.session_state["_aguardando_cookies"] = False

        # Busca o cookie
        token = self._cookies.get(CHAVE_COOKIE_SESSAO)
        if not token:
            return

        # Se achar o cookie, confere se tem usuário correspondente com sessão no banco
        usuario = ProvedorUsuarios.validar_sessao(token)
        if usuario:
            st.session_state["usuario_logado"] = usuario

    def autenticado(self) -> bool:
        """
        Retorna True se já existe um usuário guardado em session_state["usuario_logado"]
        , False se está vazio (None). 
        
        Em outras palavras, se tiver usuário logado no session_state retorna True, 
        senão False.
        """
        return st.session_state["usuario_logado"] is not None

    def render_formulario(self):
        token = st.query_params.get("token_reset")
        if token:
            self._render_nova_senha(token)
            return

        st.markdown("### Login")

        aba_login, aba_cadastro = st.tabs(["Entrar", "Criar conta"])

        with aba_login:
            self._render_login()

        with aba_cadastro:
            self._render_cadastro()

    def _render_login(self):
        """
        Grava no session_state, no banco e nos cookies do navegador o login do usuário.
        """
        with st.form("form_login"):
            email = st.text_input("E-mail", type="email", placeholder="exemplo@fhemig.mg.gov.br")
            senha = st.text_input("Senha", type="password")
            enviado = st.form_submit_button("Entrar")

        if enviado:
            # Confere no banco o e-mail e a senha informados
            usuario = ProvedorUsuarios.autenticar(email, senha)
            if usuario:
                # Autentica e grava a referência à sessão no banco e nos cookies do navegador
                st.session_state["usuario_logado"] = usuario
                token = ProvedorUsuarios.criar_sessao(usuario["id"], validade_horas=VALIDADE_SESSAO_HORAS)
                self._cookies.set(CHAVE_COOKIE_SESSAO, token, max_age=VALIDADE_SESSAO_HORAS * 60 * 60)
                time.sleep(0.3)  # dá tempo do JS gravar o cookie antes do rerun mudar de tela
                st.rerun()
            else:
                st.error("E-mail ou senha incorretos.")

        self._render_esqueci_senha()

    def _render_esqueci_senha(self):
        with st.expander("Esqueci minha senha"):
            with st.form("form_esqueci_senha"):
                email = st.text_input("E-mail cadastrado", type="email", placeholder="exemplo@fhemig.mg.gov.br", key="esqueci_email")
                enviado = st.form_submit_button("Enviar link de redefinição")
            if enviado:
                mensagem = ProvedorUsuarios.solicitar_redefinicao_senha(email)
                st.info(mensagem)

    def _render_nova_senha(self, token: str):
        st.markdown("### Definir nova senha")

        if not ProvedorUsuarios.validar_token_redefinicao(token):
            st.error("Este link é inválido ou expirou. Solicite uma nova redefinição de senha.")
            if st.button("Voltar para o login"):
                st.query_params.clear()
                st.rerun()
            return

        with st.form("form_nova_senha"):
            senha = st.text_input("Nova senha", type="password")
            confirmacao = st.text_input("Confirme a nova senha", type="password")
            enviado = st.form_submit_button("Redefinir senha")

        if not enviado:
            return

        if len(senha) < 8:
            st.error("A senha deve ter pelo menos 8 caracteres.")
            return
        if senha != confirmacao:
            st.error("As senhas não coincidem.")
            return

        if ProvedorUsuarios.redefinir_senha(token, senha):
            st.query_params.clear()
            st.success("Senha redefinida com sucesso! Faça login com a nova senha.")
            if st.button("Ir para o login"):
                st.rerun()
        else:
            st.error("Não foi possível redefinir a senha — o link pode ter expirado. Solicite um novo.")

    def _render_cadastro(self):
        with st.form("form_cadastro"):
            nome = st.text_input("Nome")
            email = st.text_input("E-mail", type="email", placeholder="exemplo@fhemig.mg.gov.br", key="cadastro_email")
            unidade = st.text_input("Unidade (opcional)")
            senha = st.text_input("Senha", type="password", key="cadastro_senha")
            confirmacao = st.text_input("Confirme a senha", type="password")
            enviado = st.form_submit_button("Criar conta")

        if not enviado:
            return

        if not nome.strip() or not email.strip():
            st.error("Preencha nome e e-mail.")
            return
        if len(senha) < 8:
            st.error("A senha deve ter pelo menos 8 caracteres.")
            return
        if senha != confirmacao:
            st.error("As senhas não coincidem.")
            return

        erro = ProvedorUsuarios.criar_usuario(email, senha, nome, unidade)
        if erro:
            st.error(erro)
        else:
            st.success('Conta criada com sucesso! Faça login na aba "Entrar".')

    def render_logout(self):
        usuario = st.session_state["usuario_logado"]
        col_nome, col_botao = st.columns([4, 1], vertical_alignment="center")
        col_nome.caption(f"Logado como **{usuario['nome']}**")
        if col_botao.button("Sair"):
            # Se logout, deleta a sessão do banco, remove dos cookies do navegador e limpa usuario_logado do state
            ProvedorUsuarios.encerrar_sessao(self._cookies.get(CHAVE_COOKIE_SESSAO))
            self._cookies.remove(CHAVE_COOKIE_SESSAO)
            time.sleep(0.3)  # dá tempo do JS remover o cookie antes do rerun mudar de tela
            st.session_state["usuario_logado"] = None
            # Limpa a análise em memória — sem isso, se outra pessoa logar na
            # mesma aba, o estado do usuário anterior seria carregado por cima
            # (analise_carregada continuaria True) e acabaria sobrescrevendo
            # a análise salva do novo usuário no próximo save.
            for chave in ("dados_servidor", "historico", "analise_carregada"):
                st.session_state.pop(chave, None)
            st.rerun()