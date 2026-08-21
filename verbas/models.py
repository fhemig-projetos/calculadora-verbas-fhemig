from django.conf import settings
from django.db import models


class Servidor(models.Model):
    """Base de referência de servidores públicos (dado mestre, importado de
    fonte externa — planilha/export de RH), indexada por MASP.

    Usada apenas para consulta/autopreenchimento: quando o analista digita um
    MASP em DadosServidor e há correspondência aqui, os campos são copiados
    automaticamente. Não é editada pelo fluxo de cálculo.
    """

    masp = models.CharField("MASP", max_length=20, unique=True)
    nome = models.CharField("Nome Completo", max_length=200)
    admissao = models.CharField("Nº de Admissão", max_length=10, blank=True)
    dt_admissao = models.DateField("Data de Admissão", null=True, blank=True)
    dt_fim_efetiva = models.DateField("Data Fim Efetiva", null=True, blank=True)
    cargo_classe = models.CharField("Cargo", max_length=50, blank=True)
    cargo_nivel = models.CharField("Nível", max_length=10, blank=True)
    cargo_grau = models.CharField("Grau", max_length=5, blank=True)
    ch_semanal = models.IntegerField("Carga Horária Semanal", default=40)

    def __str__(self):
        return f"{self.nome} (MASP {self.masp})"


class DadosServidor(models.Model):
    """Rascunho de trabalho de UMA análise em andamento (equivalente a
    'dados_servidor' no Streamlit) — não tem relação com o conceito de
    'sessão de login' do Django.

    Autopreenchido a partir de Servidor quando o MASP tem correspondência;
    editável manualmente quando não tem. Persistido para sobreviver a um F5
    junto com o histórico de verbas (ItemHistorico) da mesma análise. Um
    mesmo usuário logado pode ter vários DadosServidor ao longo do tempo (um
    por servidor público analisado); o mais recente é o que aparece na tela
    ao logar de novo.
    """

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    servidor_referencia = models.ForeignKey(
        Servidor, on_delete=models.SET_NULL, null=True, blank=True,
        help_text="Registro de Servidor usado para autopreencher estes dados, se encontrado por MASP.",
    )
    masp = models.CharField("MASP", max_length=20, blank=True)
    nome = models.CharField("Nome Completo do Servidor", max_length=200, blank=True)
    admissao = models.CharField("Nº de Admissão", max_length=10, blank=True)
    dt_admissao = models.DateField("Data de Admissão", null=True, blank=True)
    dt_fim_efetiva = models.DateField("Data Fim Efetiva", null=True, blank=True)
    cargo_classe = models.CharField("Cargo", max_length=50, blank=True)
    cargo_nivel = models.CharField("Nível", max_length=10, blank=True)
    cargo_grau = models.CharField("Grau", max_length=5, blank=True)
    ch_semanal = models.IntegerField("Carga Horária Semanal", default=40)
    ch_mensal = models.IntegerField("Carga Horária Mensal", default=0)
    vencimento_basico = models.DecimalField(
        "Vencimento Básico", max_digits=12, decimal_places=2, default=0
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome or 'Sem nome'} ({self.masp or 'sem MASP'})"


class ItemHistorico(models.Model):
    """Uma verba calculada e adicionada à lista (equivalente a cada entrada
    de st.session_state['historico'] no app atual)."""

    TIPO_VANTAGEM = "Vantagem"
    TIPO_DESCONTO = "Desconto"
    TIPO_CHOICES = [(TIPO_VANTAGEM, "Vantagem"), (TIPO_DESCONTO, "Desconto")]

    dados_servidor = models.ForeignKey(DadosServidor, on_delete=models.CASCADE, related_name="itens")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome_verba = models.CharField(max_length=200)
    codigo = models.CharField(max_length=20)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    memoria = models.JSONField()
    competencia = models.CharField(max_length=10)
    observacao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome_verba} - R$ {self.valor}"