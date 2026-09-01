from typing import Optional
import bcrypt
import streamlit as st
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
