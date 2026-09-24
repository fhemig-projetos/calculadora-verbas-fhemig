import base64
import os
import smtplib
import socket
import ssl
from typing import Optional
from urllib.parse import unquote, urlparse
import bcrypt
import secrets
import streamlit as st
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from supabase import create_client

@st.cache_resource
def _cliente():
    return create_client(
        st.secrets["supabase_admin"]["url"],
        st.secrets["supabase_admin"]["key"],
    )

def _conectar_smtp(host: str, port: int, timeout: float = 15) -> smtplib.SMTP_SSL:
    """Abre a conexão SMTP_SSL com o host informado.

    Em produção (sem proxy configurado no ambiente), conecta direto. Em
    dev local atrás do proxy corporativo (ex.: rede da PRODEMGE — variável
    de ambiente `https_proxy`), o `smtplib` não sabe atravessar proxy HTTP
    sozinho, então abrimos manualmente um túnel via `CONNECT` (mesmo
    mecanismo que o `curl` usa) antes de estabelecer o TLS.
    """
    proxy_url = os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY")
    if not proxy_url:
        return smtplib.SMTP_SSL(host, port, timeout=timeout)

    proxy = urlparse(proxy_url)
    sock = socket.create_connection((proxy.hostname, proxy.port), timeout=timeout)

    requisicao_connect = f"CONNECT {host}:{port} HTTP/1.1\r\nHost: {host}:{port}\r\n"
    if proxy.username:
        # urlparse não decodifica % da URL (ex.: senha com "@" vira "%40") — precisa de unquote
        usuario_proxy = unquote(proxy.username)
        senha_proxy = unquote(proxy.password or "")
        credenciais = base64.b64encode(f"{usuario_proxy}:{senha_proxy}".encode()).decode()
        requisicao_connect += f"Proxy-Authorization: Basic {credenciais}\r\n"
    requisicao_connect += "\r\n"
    sock.sendall(requisicao_connect.encode())

    resposta = sock.recv(4096)
    linha_status = resposta.split(b"\r\n", 1)[0]
    if b" 200 " not in linha_status:
        sock.close()
        raise ConnectionError(f"Proxy recusou o túnel até {host}:{port}: {linha_status!r}")

    sock_tls = ssl.create_default_context().wrap_socket(sock, server_hostname=host)

    cliente_smtp = smtplib.SMTP_SSL(timeout=timeout)
    cliente_smtp.sock = sock_tls
    cliente_smtp.file = None
    codigo, msg = cliente_smtp.getreply()
    if codigo != 220:
        raise smtplib.SMTPConnectError(codigo, msg)
    return cliente_smtp

def _enviar_email_redefinicao(email: str, token: str) -> None:
    """Envia o e-mail de redefinição de senha via SMTP (Gmail por ora).

    Isolada de propósito: trocar para SMTP institucional da FHEMIG ou uma
    API transacional no futuro é só reescrever esta função, sem tocar no
    resto do fluxo de redefinição.
    """
    url = f"{st.secrets['app']['url_base']}?token_reset={token}"
    corpo = (
        f"Recebemos uma solicitação para redefinir sua senha na Calculadora de Verbas FHEMIG.\n\n"
        f"Clique no link abaixo para criar uma nova senha (válido por 30 minutos):\n{url}\n\n"
        f"Se você não solicitou isso, ignore este e-mail."
    )
    mensagem = MIMEText(corpo, "plain", "utf-8")
    mensagem["Subject"] = "Redefinição de senha — Calculadora de Verbas FHEMIG"
    mensagem["From"] = st.secrets["smtp"]["remetente"]
    mensagem["To"] = email

    with _conectar_smtp(st.secrets["smtp"]["host"], st.secrets["smtp"]["port"]) as servidor:
        servidor.login(st.secrets["smtp"]["usuario"], st.secrets["smtp"]["senha"])
        servidor.send_message(mensagem)

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
    def criar_usuario(email: str, senha: str, nome: str, unidade: Optional[str] = None) -> Optional[str]:
        """Cria um novo usuário via autocadastro.

        Retorna None em caso de sucesso, ou uma mensagem de erro (ex: e-mail
        já cadastrado) para exibir ao usuário. A conta já entra ativa
        (`ativo=True`, default da tabela) — não há fluxo de aprovação.
        """
        email_normalizado = email.strip().lower()

        try:
            resposta = (
                _cliente()
                .table("usuarios")
                .select("id")
                .eq("email", email_normalizado)
                .limit(1)
                .execute()
            )
        except Exception:
            return "Não foi possível criar a conta agora. Tente novamente."

        if resposta.data:
            return "Já existe uma conta com esse e-mail."

        _cliente().table("usuarios").insert({
            "email": email_normalizado,
            "senha_hash": ProvedorUsuarios.gerar_hash(senha),
            "nome": nome.strip(),
            "unidade": unidade.strip() if unidade else None,
        }).execute()
        return None

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
    def solicitar_redefinicao_senha(email: str) -> str:
        """Gera um token de redefinição de senha e envia por e-mail (SMTP).

        Sempre retorna a mesma mensagem genérica, independente de o e-mail
        existir na base, de erro de conexão com o banco, ou de falha no
        envio do e-mail — evita que alguém descubra quais e-mails estão
        cadastrados (mesmo padrão de `autenticar`), e não expõe detalhes de
        infraestrutura (SMTP fora do ar etc.) para o usuário final. Falhas
        reais de envio ficam só no console (`print`), para depuração.
        """
        email_normalizado = email.strip().lower()
        mensagem_generica = "Se esse e-mail estiver cadastrado, você receberá um link para redefinir sua senha."

        try:
            resposta = (
                _cliente()
                .table("usuarios")
                .select("id")
                .eq("email", email_normalizado)
                .eq("ativo", True)
                .limit(1)
                .execute()
            )
        except Exception:
            return mensagem_generica

        if not resposta.data:
            return mensagem_generica

        usuario_id = resposta.data[0]["id"]
        token = secrets.token_urlsafe(32)
        expira_em = datetime.now(timezone.utc) + timedelta(minutes=30)

        _cliente().table("redefinicoes_senha").insert({
            "token": token,
            "usuario_id": usuario_id,
            "expira_em": expira_em.isoformat(),
        }).execute()

        try:
            _enviar_email_redefinicao(email_normalizado, token)
        except Exception:
            print(f"[ERRO] Falha ao enviar e-mail de redefinição para {email_normalizado}")

        return mensagem_generica

    @staticmethod
    def validar_token_redefinicao(token: str) -> Optional[dict]:
        """Confere se um token de redefinição existe, não expirou e não foi usado.

        Retorna o registro da redefinição (com usuario_id) se válido, ou
        None caso contrário.

        1. Busca na tabela redefinicoes_senha a linha com esse token
        2. Se não achar nada → None (token inválido/inexistente)
        3. Se achar mas usado=True → None (já foi consumido antes, não deixa reusar)
        4. Se achar e expira_em já passou → None (expirou)
        5. Só se passar por essas 3 checagens → retorna o registro (o "sim, pode prosseguir")
        """
        if not token:
            return None

        try:
            resposta = (
                _cliente()
                .table("redefinicoes_senha")
                .select("token, usuario_id, expira_em, usado")
                .eq("token", token)
                .limit(1)
                .execute()
            )
        except Exception:
            return None

        if not resposta.data:
            return None

        redefinicao = resposta.data[0]
        if redefinicao["usado"]:
            return None

        expira_em = datetime.fromisoformat(redefinicao["expira_em"])
        if expira_em < datetime.now(timezone.utc):
            return None

        return redefinicao

    @staticmethod
    def redefinir_senha(token: str, nova_senha: str) -> bool:
        """Revalida o token e, se válido, atualiza a senha do usuário associado.

        Marca o token como usado (impede reaproveitar o mesmo link). Retorna
        True em caso de sucesso, False se o token não for (mais) válido.
        """
        redefinicao = ProvedorUsuarios.validar_token_redefinicao(token)
        if not redefinicao:
            return False

        _cliente().table("usuarios").update({
            "senha_hash": ProvedorUsuarios.gerar_hash(nova_senha),
        }).eq("id", redefinicao["usuario_id"]).execute()

        _cliente().table("redefinicoes_senha").update({
            "usado": True,
        }).eq("token", token).execute()

        return True

    @staticmethod
    def encerrar_sessao(token: str) -> None:
        """Invalida um token de sessão — usado no logout, mata a sessão no
        banco (não só o cookie local, que sozinho não impediria reuso do token)."""
        if not token:
            return
        _cliente().table("sessoes").delete().eq("token", token).execute()
