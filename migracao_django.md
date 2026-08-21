# Migração: Streamlit → Django — Log de Progresso

> **Propósito:** Log de continuidade da migração da Calculadora de Verbas de Streamlit para Django (login por usuário + histórico persistente + MySQL). Complementa `contexto.md` (que documenta a versão Streamlit) e serve pra retomar o trabalho em qualquer sessão/computador.
> **Branch:** `feature/migracao-django`
> **Plano completo:** salvo em `/home/amsdo-pc/.claude/plans/estou-pensando-em-faz-lo-lexical-sedgewick.md` (local à máquina onde foi criado — este arquivo é o espelho que viaja com o repo)

---

## 1. Por que migrar

A versão Streamlit guarda todo o estado em `st.session_state` — não distingue usuários e perde tudo (histórico de verbas calculadas, dados do servidor) a cada F5/fechar navegador. Objetivos da migração:

- **Login por usuário** (cada analista com sua própria conta)
- **Histórico de cálculos persistente**, privado por usuário, sobrevivendo a refresh/fechar navegador/trocar de máquina
- **MySQL** como banco real (SQLite por enquanto, enquanto valida a lógica)

## 2. Decisões tomadas

| Decisão | Escolha | Por quê |
|---|---|---|
| Framework | **Django** | Auth pronto (`django.contrib.auth`), ORM + migrations nativas p/ MySQL, admin gratuito p/ inspecionar dados |
| Histórico | **Privado por usuário** | Cada login só vê o próprio histórico |
| Autenticação | **Login simples usuário/senha** | Auth padrão do Django; AD/LDAP fica pra depois, se necessário |
| Interatividade (trocar verba → campos mudam) | **HTMX** | Poucas linhas de JS, mantém a filosofia "tudo em Python/templates" |
| Banco (fase atual) | **SQLite** | Usuário ainda não tem MySQL disponível; troca pra MySQL Community no final, quando a lógica já estiver validada |
| Ritmo de execução | **Didático, passo a passo** | Usuário sem experiência prévia com Django/frameworks web — ver seção 6 |

### 2.1 Dados do servidor: dois models, papéis diferentes

Ponto importante esclarecido nesta sessão: os "dados do servidor" (cabeçalho) **não** deveriam ser um cadastro que o Django "possui" — existe (ou vai existir) uma base de referência real de servidores, indexada por MASP, de onde os dados devem ser autopreenchidos quando há correspondência (usuário confirmou que já tem essa fonte — planilha/export de RH). Por isso, o model foi dividido em dois:

- **`Servidor`** — dado mestre/referência, importado da fonte externa do usuário, indexado por `masp` (único). Só consulta, não editado pelo fluxo de cálculo.
- **`DadosServidor`** — o "rascunho de trabalho" de uma análise em andamento: autopreenchido a partir de `Servidor` quando o MASP bate, editável manualmente quando não bate. Persistido (é o que garante sobreviver ao F5), com FK pro usuário dono e FK opcional (`servidor_referencia`) rastreando de qual `Servidor` veio o autopreenchimento.

(O model se chamava inicialmente `SessaoServidor` — renomeado para `DadosServidor` porque "sessão" colidia com o conceito técnico de sessão de login do Django, o que gerava confusão.)

## 3. Progresso até agora

- [x] Projeto Django criado na raiz do mesmo repositório (`manage.py`, `config/` — settings/urls/wsgi/asgi)
- [x] App `verbas` criado e registrado em `INSTALLED_APPS`
- [x] Rodado `migrate` inicial (tabelas internas do Django — auth, sessions, etc.) + criado superusuário, login testado em `/admin/`
- [x] `verbas/models.py` com os 3 models: `Servidor`, `DadosServidor`, `ItemHistorico` (ver seção 2.1 e detalhes abaixo)
- [x] `verbas/admin.py` registra `DadosServidor` e `ItemHistorico` (`Servidor` ainda não registrado — decisão pendente, ver seção 4)
- [x] `.gitignore` atualizado (`db.sqlite3` incluído)
- [ ] **Ainda não rodado:** `makemigrations verbas` + `migrate` para os 3 models novos (models ainda em ajuste até a última sessão)

### 3.1 Estrutura atual dos models (`verbas/models.py`)

```python
class Servidor(models.Model):
    """Base de referência (dado mestre), indexada por MASP único."""
    masp = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=200)
    admissao = models.CharField(max_length=10, blank=True)
    dt_admissao = models.DateField(null=True, blank=True)
    cargo_classe = models.CharField(max_length=50, blank=True)
    cargo_nivel = models.CharField(max_length=10, blank=True)
    cargo_grau = models.CharField(max_length=5, blank=True)
    ch_semanal = models.IntegerField(default=40)

class DadosServidor(models.Model):
    """Rascunho de trabalho de uma análise em andamento (persiste pro F5)."""
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    servidor_referencia = models.ForeignKey(Servidor, on_delete=models.SET_NULL, null=True, blank=True)
    masp, nome, admissao, dt_admissao, dt_fim_efetiva,
    cargo_classe, cargo_nivel, cargo_grau,
    ch_semanal, ch_mensal, vencimento_basico,
    criado_em, atualizado_em  # (campos espelham ui/form_servidor.py)

class ItemHistorico(models.Model):
    """Uma verba calculada e adicionada à lista (equivale a st.session_state['historico'][i])."""
    dados_servidor = models.ForeignKey(DadosServidor, on_delete=models.CASCADE, related_name="itens")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome_verba, codigo, tipo (Vantagem/Desconto), valor,
    memoria (JSONField — lista de strings), competencia, observacao, criado_em
```

## 4. Próximos passos (em ordem)

1. Rodar `python manage.py makemigrations verbas` + `migrate`, conferir os 3 models no `/admin/`.
2. Decidir se registra `Servidor` no admin (útil pra inspecionar dados importados).
3. Definir o formato da fonte de dados do usuário (planilha/export de RH) e desenhar a importação pra popular `Servidor`.
4. Implementar a lógica de autopreenchimento por MASP (`DadosServidor` ← busca em `Servidor`).
5. Portar `calculadoras/` e `data/provedor_dados.py` pro fluxo Django (trocar `@st.cache_data` por `functools.lru_cache` — sem mudança de lógica, já que essas classes não dependem do Streamlit).
6. `DadosServidorForm` (ModelForm) + view.
7. Seleção de verba + campos dinâmicos via HTMX (a parte mais trabalhosa — replica a lógica de `ui/selecao_verba.py`).
8. Cálculo → salvar em `ItemHistorico`.
9. Tela de histórico (listar / remover / limpar / totais).
10. Portar `utils/exportador_pdf.py::GeradorPDF` pra uma view de download (a classe em si não muda).
11. Testes manuais ponta a ponta comparando com o app Streamlit atual.
12. Trocar SQLite → MySQL Community (última etapa, com a lógica já validada).

## 5. Verificação (quando a migração estiver mais avançada)

- Login/logout funcionando, sem vazamento de dados entre usuários
- Autopreenchimento por MASP funcionando (e fallback manual quando não encontra)
- Resultados de cálculo batendo com a versão Streamlit (rodar as duas em paralelo pra comparar)
- Histórico sobrevivendo a F5 / fechar navegador
- PDF gerado com o mesmo conteúdo/layout de hoje

## 6. Como trabalhar nesta migração (acordo com o usuário)

Usuário não tem experiência prévia com Django nem frameworks web — é a primeira exposição prática. Cada passo deve ser pequeno, com o conceito novo explicado em linguagem simples (o que é uma migration, uma view, um queryset, etc.), e o usuário roda/valida cada passo no próprio terminal antes de avançar. O usuário prefere rodar os comandos ele mesmo (não pelo Claude Code) e colar o resultado para validação.

---

*Este arquivo é atualizado conforme a migração avança — é o ponto de partida para retomar o trabalho em qualquer sessão.*
