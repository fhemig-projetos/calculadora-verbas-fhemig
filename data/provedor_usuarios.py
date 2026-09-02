from typing import Optional
import bcrypt
import secrets
import streamlit as st
from datetime import datetime, timedelta, timezone
from supabase import create_client

@st.cache_resource
def _cliente():
    return create_client(
        st.secrets["supabase_admin"]["url"],
        st.secrets["supabase_admin"]["key"],
    )

class ProvedorUsuarios:
    @staticmethod
    def gerar_hash(senha: str) -> str:
        """Gera o hash bcrypt de uma senha em texto puro.

        Uso: só na criação/reset de usuários (ex: um script administrativo),
        nunca no fluxo de login — lá a senha digitada é comparada direto
        contra o hash salvo, via `autenticar`.
        """
        return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def autenticar(email: str, senha: str) -> Optional[dict]:
        """Autentica um usuário por e-mail e senha.

        Retorna os dados do usuário (sem a senha) se as credenciais forem
        válidas e o usuário estiver ativo, ou None caso contrário. Não usa
        st.cache_data (usado em outros provedores) porque cachear resultado
        de autenticação permitiria login com senha antiga/revogada até o
        cache expirar.
        """
        email_normalizado = email.strip().lower()

        try:
            resposta = (
                _cliente()
                .table("usuarios")
                .select("*")
                .eq("email", email_normalizado)
                .eq("ativo", True)
                .limit(1)
                .execute()
            )
        except Exception:
            st.error("⚠️ Não foi possível consultar a base de usuários agora. Tente novamente.")
            return None

        if not resposta.data:
            return None

        usuario = resposta.data[0]
        try:
            senha_valida = bcrypt.checkpw(senha.encode("utf-8"), usuario["senha_hash"].encode("utf-8"))
        except ValueError:
            # Hash salvo em formato inválido/corrompido
            return None

        if not senha_valida:
            return None

        usuario.pop("senha_hash")
        return usuario

    @staticmethod
    def criar_sessao(usuario_id, validade_horas: float = 1) -> str:
        """Cria uma sessão persistente (mantém o login após F5/fechar o navegador).

        Gera um token aleatório e opaco (imprevisível, diferente de um id
        sequencial), salva na tabela `sessoes` com prazo de validade e
        retorna o token — quem chama é responsável por gravá-lo num cookie.
        """
        token = secrets.token_urlsafe(32)
        expira_em = datetime.now(timezone.utc) + timedelta(hours=validade_horas)

        _cliente().table("sessoes").insert({
            "token": token,
            "usuario_id": usuario_id,
            "expira_em": expira_em.isoformat(),
        }).execute()

        return token

    @staticmethod
    def validar_sessao(token: str) -> Optional[dict]:
        """Confere se um token de sessão ainda é válido e retorna o usuário associado.

        Retorna None se o token não existir, já tiver expirado, ou o usuário
        associado não estiver mais ativo.
        """
        if not token:
            return None

        try:
            resposta = (
                _cliente()
                .table("sessoes")
                .select("expira_em, usuarios(id, email, nome, unidade, ativo)")
                .eq("token", token)
                .limit(1)
                .execute()
            )
        except Exception:
            return None

        if not resposta.data:
            return None

        sessao = resposta.data[0]
        expira_em = datetime.fromisoformat(sessao["expira_em"])
        # O momento em que a sessão expira já ficou no passado?
        if expira_em < datetime.now(timezone.utc):
            _cliente().table("sessoes").delete().eq("token", token).execute()
            return None

        usuario = sessao["usuarios"]
        if not usuario or not usuario.get("ativo"):
            return None

        return usuario

    @staticmethod
    def encerrar_sessao(token: str) -> None:
        """Invalida um token de sessão — usado no logout, mata a sessão no
        banco (não só o cookie local, que sozinho não impediria reuso do token)."""
        if not token:
            return
        _cliente().table("sessoes").delete().eq("token", token).execute()
