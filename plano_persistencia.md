# Plano de Implementação — Persistência de Dados na Calculadora de Verbas Remuneratórias

## Contexto e problema a resolver

A aplicação (Streamlit, hospedada na Streamlit Community Cloud) perde o histórico de cálculos em memória (`st.session_state`) em três cenários distintos:

1. **Hibernação por inatividade (12h)** — a Community Cloud hiberna apps sem tráfego, reiniciando o processo do zero ao acordar.
2. **Desconexão de WebSocket por inatividade curta** (minutos) — o `disconnectedSessionTTL` padrão do Streamlit é de apenas 120 segundos; passado esse tempo, a sessão pode ser descartada mesmo sem reload.
3. **F5 / recarga manual da página** — reinicia a negociação de sessão no navegador; comportamento amplamente relatado como "esperado" pela comunidade Streamlit, não é um bug.
4. **Redeploy** (push no GitHub) — reinicia o processo inteiro.

**Causa raiz comum:** `st.session_state` só existe na memória do processo Python. Qualquer evento que reinicie o processo ou descarte a sessão apaga os dados, porque eles nunca foram persistidos fora dali.

**Solução de fundo:** desacoplar a persistência do ciclo de vida do processo/sessão, salvando cada cálculo em um banco de dados externo (Supabase/Postgres) no momento em que é adicionado, e reidratando o `session_state` a partir do banco sempre que necessário — em vez de depender de o dado "sobreviver" na memória.

---

## Decisão de arquitetura: Supabase (Postgres)

Avaliamos Google Sheets como alternativa mais simples, mas **Supabase foi a escolha final**, por causa do plano de expansão da ferramenta para todas as unidades da FHEMIG:

| Critério | Google Sheets | Supabase |
|---|---|---|
| Persistência real | Sim | Sim |
| Escala (múltiplas unidades simultâneas) | Limitado por cota de API (~60 req/min) e teto de 10M células | Banco relacional de verdade, escala bem melhor |
| Velocidade de consulta | Filtra em memória no app | Filtra no próprio banco (índices) |
| Complexidade de setup | Baixa | Moderada |
| Familiaridade da equipe não-técnica | Alta | Baixa (mitigar com telas no próprio app) |

---

## 1. Modelagem do banco de dados

**✅ Executado em 19/08 no Supabase** (schema final, revisado em relação à primeira versão deste documento — ver decisões abaixo):

```sql
-- Tabela de usuários (analistas)
create table usuarios (
    id uuid default gen_random_uuid() primary key,
    login text unique not null,          -- MASP do analista, normalizado (só dígitos)
    senha_hash text not null,
    nome text,
    unidade text,
    criado_em timestamptz default now()
);

-- Tabela de histórico de cálculos (estado de trabalho, não é o registro oficial de auditoria)
create table historico_calculos (
    id uuid default gen_random_uuid() primary key,
    usuario_id uuid references usuarios(id),   -- analista logado
    audit_id text,                             -- MASP do servidor sendo calculado (agrupa um Resumo Funcional)
    criado_em timestamptz default now(),
    nome_verba text,
    codigo text,
    tipo text,
    valor numeric,
    competencia text,
    observacao text,
    memoria jsonb
);

create index idx_usuario_audit on historico_calculos (usuario_id, audit_id);
```

**Decisões tomadas em relação à primeira versão deste documento:**
- Colunas renomeadas para bater exatamente com as chaves do dicionário já usado em `st.session_state["historico"]` hoje (`nome_verba`, `codigo`, `tipo`, `valor`, `competencia`, `observacao`) — evita ter nomenclatura diferente no banco e no código Python.
- `memoria` virou coluna própria (`jsonb`, guarda a lista de strings da memória de cálculo).
- **Removidos:** `dados_completos` (era uma cópia redundante de tudo, já que todas as colunas do dicionário viraram colunas próprias), `unidade` e `analista` (fora de escopo agora — `analista` é redundante com o `join` via `usuario_id`; `unidade` fica pra quando a expansão multi-unidade entrar em pauta), `verba`/`valor_calculado` (duplicavam `nome_verba`/`valor` com nomes diferentes).
- **Índice único composto** `(usuario_id, audit_id)` em vez de dois índices separados — reflete o padrão real de consulta do app (sempre filtra pelos dois juntos, ou só por `usuario_id`); um índice isolado em `audit_id` só valeria a pena se existisse uma consulta "todos os cálculos desse MASP, de qualquer analista", que não está no escopo.
- **Descartada a ideia de uma tabela `servidores`** no Supabase para pré-preenchimento do cabeçalho pelo MASP (pendência 4.8 do `contexto.md`) — essa busca vai usar um arquivo JSON no próprio repositório (mesmo padrão de `data/tabelas.json`), ainda não carregado pelo usuário. Não faz parte deste plano de persistência.

> **Nota:** `historico_calculos` é um "carrinho de trabalho em andamento", não o artefato oficial de auditoria (esse continua sendo o PDF exportado ao final). Por isso é seguro fazer limpeza periódica dela (ver seção 5).

---

## 2. Autenticação e persistência de sessão

**Biblioteca recomendada:** `streamlit-authenticator` (evita reimplementar hash de senha e gestão de cookie do zero).

**Decisão (19/08):** o campo `login` da tabela `usuarios` será o **MASP do analista**, normalizado para conter **apenas dígitos** (sem pontos/traços) — tanto no cadastro quanto na hora de logar. Essa normalização acontece **só na camada da aplicação** (Python), não no banco — decidido manter a tabela `usuarios` simples, sem `CHECK constraint` no SQL, para não duplicar a regra em dois lugares.

> **Pendência para implementar mais adiante:** criar `FormatadorCampos.normalizar_masp(masp_cru: str) -> str` em `utils/formatador_campos.py` (irmã da `masp()` já existente, que faz o formato de exibição — essa nova função faz o inverso: remove tudo que não for dígito). Usar essa função em dois pontos: (1) ao cadastrar um analista novo (antes de gravar `login` na tabela `usuarios`), e (2) ao processar o campo de login na tela de autenticação (antes de consultar o banco). Ainda não implementada — só a decisão está registrada aqui.

### Fluxo completo:

1. **Login:** usuário informa login (MASP ou e-mail institucional) + senha. A lib valida contra `senha_hash` da tabela `usuarios`.
2. **Persistência da sessão via cookie assinado:** ao autenticar com sucesso, um cookie é gravado no navegador com prazo de validade (sugestão: 8h, cobrindo um turno de trabalho). É esse cookie — não o `session_state` — que sobrevive a um F5.
3. **A cada carregamento do app:** antes de mostrar a tela de login, checar se existe cookie válido. Se sim, autenticar automaticamente e pular direto para a reidratação do histórico (passo 4). Se não, mostrar tela de login normalmente.
4. **Reidratação do histórico:** após autenticação (por login manual ou por cookie), consultar `historico_calculos where usuario_id = X` e popular `st.session_state.lista_calculos`.
5. **Fechar o navegador:** com cookie de validade fixa (não "cookie de sessão"), fechar a aba **não** desloga o usuário — ele retoma automaticamente dentro do prazo configurado.
6. **Deslogar e logar novamente:** histórico é resgatado normalmente, pois nunca dependeu do navegador — está atrelado ao `usuario_id` no banco.

### Checklist de implementação:
- [ ] Criar tabela `usuarios` e cadastrar analistas iniciais (login/senha/unidade)
- [ ] Integrar `streamlit-authenticator` (config de cookie: nome, chave de assinatura, prazo de expiração)
- [ ] Testar fluxo de login → F5 → confirmar que cookie mantém sessão sem pedir login de novo
- [ ] Testar fluxo de logout → login novamente → confirmar que histórico é resgatado

---

## 3. Persistência incremental do histórico

**Plano detalhado em 19/08** (revisado em relação à primeira versão — nomes de coluna e assinaturas de função atualizados pra bater com o schema real da seção 1, e todas as funções passam a filtrar por `usuario_id` **e** `audit_id`, não só `usuario_id`, já que `audit_id` é o que separa os cálculos por servidor/MASP):

```python
def adicionar_calculo(usuario_id, audit_id, novo_calculo: dict):
    supabase.table("historico_calculos").insert({
        "usuario_id": usuario_id,
        "audit_id": audit_id,
        "nome_verba": novo_calculo["nome_verba"],
        "codigo": novo_calculo["codigo"],
        "tipo": novo_calculo["tipo"],
        "valor": novo_calculo["valor"],
        "competencia": novo_calculo["competencia"],
        "observacao": novo_calculo["observacao"],
        "memoria": novo_calculo["memoria"],
    }).execute()

def remover_ultimo(usuario_id, audit_id):
    ultimo = supabase.table("historico_calculos") \
        .select("id").eq("usuario_id", usuario_id).eq("audit_id", audit_id) \
        .order("criado_em", desc=True).limit(1).execute()
    if ultimo.data:
        supabase.table("historico_calculos").delete().eq("id", ultimo.data[0]["id"]).execute()

def limpar_historico(usuario_id, audit_id):
    supabase.table("historico_calculos").delete() \
        .eq("usuario_id", usuario_id).eq("audit_id", audit_id).execute()

def carregar_historico(usuario_id, audit_id) -> list[dict]:
    resposta = supabase.table("historico_calculos") \
        .select("*").eq("usuario_id", usuario_id).eq("audit_id", audit_id) \
        .order("criado_em").execute()
    return resposta.data
```

`st.session_state["historico"]` continua existindo como já existe hoje — funciona como *cache de exibição* pro rerender do Streamlit, mas o banco é a fonte de verdade: toda mutação (`adicionar`/`remover`/`limpar`) grava no Supabase, e o `session_state` é espelhado logo em seguida (ou reidratado do zero via `carregar_historico`).

### Segredos: local vs. produção
- **Local (desenvolvimento):** `.streamlit/secrets.toml` (arquivo próprio, **no `.gitignore`**, nunca commitado) com `SUPABASE_URL` e `SUPABASE_KEY`. Existe um `.streamlit/secrets.toml.example` versionado só como referência de formato (sem valores reais).
- **Produção (Streamlit Community Cloud):** não é upload de arquivo — cada app publicado tem sua própria tela **Settings → Secrets** no painel do Streamlit Cloud, onde se cola o mesmo conteúdo TOML. Isso é por-app: como vamos testar numa segunda instância do app apontando pro branch `feature/persistencia-supabase` (separada da instância de produção em `main`), os secrets dessa instância de teste são configurados só nela, independente da instância de produção (que, por ora, nem usa Supabase). Ao promover a feature pra `main`, os mesmos secrets precisam ser replicados na tela de Secrets do app de produção.
- Sem custo/restrição adicional no tier gratuito do Streamlit Cloud para uso de Secrets.

### `usuario_id` de teste (temporário, até a autenticação real)
Como `historico_calculos.usuario_id` tem uma foreign key pra `usuarios(id)`, o valor fixo usado nesta fase precisa existir de verdade na tabela. Inserir um usuário de teste e usar o `id` retornado:
```sql
insert into usuarios (login, senha_hash, nome)
values ('00000000', 'temp', 'Usuário de Teste')
returning id;
```

### Checklist de implementação:
- [ ] Adicionar `supabase` ao `requirements.txt`
- [ ] Criar `.streamlit/secrets.toml.example` (versionado) e adicionar `.streamlit/secrets.toml` ao `.gitignore`
- [ ] Implementar `FormatadorCampos.normalizar_masp()` (ver seção 2) — necessária agora pra montar o `audit_id` de forma consistente a partir do MASP do cabeçalho
- [ ] Criar módulo `utils/persistencia.py`: cliente Supabase (`@st.cache_resource`), `USUARIO_ID_FAKE` (constante temporária, com `# TODO` marcando a substituição futura pelo usuário autenticado), e as 4 funções acima
- [ ] Integrar `adicionar_calculo` ao botão "➕ Adicionar à lista" (`_render_resultado`, `ui/selecao_verba.py`)
- [ ] Integrar `remover_ultimo` / `limpar_historico` aos botões "🗑️ Remover último" / "🗑️ Limpar lista" (`_render_historico`)
- [ ] Chamar `carregar_historico` na entrada (reidratação), usando `audit_id` = MASP normalizado de `dados_servidor`
- [ ] Testar: adicionar cálculo → F5 → confirmar que o histórico volta do Supabase (prova de que a persistência funciona antes de acoplar autenticação)

---

## 4. Ajuste complementar (barato, vale fazer de qualquer forma)

Aumentar o TTL de sessão desconectada do Streamlit — não resolve hibernação nem F5, mas reduz a chance de perda em desconexões curtas de WebSocket (ex: aba em segundo plano):

```toml
# .streamlit/config.toml
[server]
disconnectedSessionTTL = 3600  # 1 hora, em segundos (padrão é 120s)
```

---

## 5. Limpeza periódica da tabela de histórico

Como `historico_calculos` é só estado de trabalho (não o registro oficial de auditoria), não há necessidade de retenção indefinida. Usar `pg_cron` (nativo no Supabase, inclusive no tier gratuito):

```sql
select cron.schedule(
  'limpeza-historico-diaria',
  '0 3 * * *',  -- todo dia às 3h da manhã
  $$ delete from historico_calculos where criado_em < now() - interval '3 days' $$
);
```

> **Importante:** apagar por janela de dias (ex: 3 dias), não a tabela inteira de uma vez — um analista pode iniciar uma auditoria à tarde e retomar na manhã seguinte.

### Efeito colateral positivo a explorar
O tier gratuito do Supabase pausa projetos sem nenhuma atividade de banco por 7 dias consecutivos (podendo levar a exclusão em pausas muito prolongadas). Como o job de limpeza diária já gera atividade no banco regularmente, ele também previne essa pausa por inatividade — sem necessidade de um mecanismo de "keep-alive" separado.

### Checklist de implementação:
- [ ] Criar o job de `pg_cron` no SQL Editor do Supabase
- [ ] Confirmar que o job está rodando (`cron.job_run_details`)

---

## 6. Fora de escopo imediato, mas mapeado para o futuro

- **Migração de hospedagem** (Community Cloud → VM Azure ou VM corporativa da FHEMIG): não exige reescrever a aplicação, pois a persistência já está desacoplada da hospedagem via Supabase. Envolve: reverse proxy (nginx/Caddy) + HTTPS, gestão de processo (systemd/Docker), secrets locais, e possivelmente múltiplas réplicas atrás de um load balancer se o volume de unidades simultâneas crescer muito.
- **LGPD:** a introdução de login implica armazenar dados pessoais dos analistas (login, nome, unidade) — revisar a análise de LGPD já feita anteriormente para o projeto, que partia da premissa de não armazenar dados pessoais.
- **Exportação manual de backup (JSON/PDF):** pode continuar existindo como conveniência opcional para o analista, mas não deve ser o mecanismo primário de recuperação — essa responsabilidade é do Supabase + login.

---

## Ordem de implementação (redefinida em 19/08)

**Mudança em relação à ordem original:** decidimos validar a persistência isoladamente antes de acoplar a autenticação, usando um `usuario_id` fixo/fake enquanto o login de verdade não existe. Isso separa dois riscos que a ordem original acoplava (Supabase + auth ao mesmo tempo).

1. ✅ Criar branch de trabalho `feature/persistencia-supabase` (não mexer em `main`, que está deployado ao vivo)
2. ✅ Criar projeto no Supabase
3. ✅ Criar tabela `usuarios` (decisão: `login` = MASP, só dígitos — ver seção 2 acima)
4. ✅ Criar tabela `historico_calculos` + índice composto (`usuario_id`, `audit_id`) — schema final na seção 1
5. 🔲 Implementar módulo `utils/persistencia.py` (CRUD do histórico) usando um `usuario_id` fixo/fake para teste — plano detalhado na seção 3
6. 🔲 Integrar persistência aos botões existentes (adicionar / remover último / limpar) em `ui/selecao_verba.py`
7. 🔲 Testar a persistência isolada (sem login ainda): fechar/reabrir o app, F5, confirmar que o histórico volta do Supabase
8. 🔲 Cadastrar usuários de teste (analistas reais, com `login` = MASP normalizado, senha em hash)
9. 🔲 Integrar `streamlit-authenticator` (login + cookie)
10. 🔲 Trocar o `usuario_id` fixo pelo `usuario_id` real da sessão autenticada
11. 🔲 Ajustar `disconnectedSessionTTL` no `.streamlit/config.toml`
12. 🔲 Configurar `pg_cron` para limpeza periódica
13. 🔲 Testar os cenários completos: F5, fechar navegador, logout/login, múltiplos usuários simultâneos

> Item 14 original (`normalizar_masp`) foi antecipado — ver checklist da seção 3, já que virou pré-requisito do `audit_id`, não só do login.