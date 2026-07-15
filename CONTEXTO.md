# Contexto — Calculadora de Verbas FHEMIG

## Objetivo
Refatorar o `app.py` original para uma arquitetura modular, encapsulando
cada seção da interface em classes próprias dentro do pacote `ui/`.

## Arquitetura do Projeto

```
┌─────────────────────────────────────────────┐
│  ui/ (Streamlit — Renderização)             │
│  - cabecalho.py      → Cabeçalho            │
│  - form_servidor.py  → Dados do servidor    │
│  - selecao_verba.py  → Seleção e cálculo    │
│  - config.py         → CONFIG_CAMPOS        │
└──────────────────────┬──────────────────────┘
                       │ usa
┌──────────────────────▼──────────────────────┐
│  calculadoras/ (Lógica de negócio)          │
│  - base.py           → ABC + ResultadoCalculo│
│  - factory.py        → REGISTRO_CALCULADORAS│
│  - hora_extra.py     → CalculadoraHoraExtra │
│  - adicional_noturno.py → ...               │
│  - gratificacao_final_semana.py → ...       │
│  - inss_mensal.py    → CalculadoraINSS      │
│  - grs_dias.py       → CalculadoraGRSDias   │
│  - decimo_terceiro.py → CalculadoraDecimoTerceiro │
│  - (demais verbas a implementar)            │
└──────────────────────┬──────────────────────┘
                       │ usa
┌──────────────────────▼──────────────────────┐
│  data/ (Dados)                              │
│  - provedor_dados.py → ProvedorDadosFhemig  │
│  - tabelas.json      → Cargos, INSS, verbas, tabela_grs │
└──────────────────────┬──────────────────────┘
                       │ usa
┌──────────────────────▼──────────────────────┐
│  utils/ (Utilitários)                       │
│  - formatador_campos.py → FormatadorCampos  │
│  - ui_callbacks.py      → callbacks         │
│  - exportador_pdf.py    → PDF (pendente)    │
└─────────────────────────────────────────────┘
```

### Separação de responsabilidades

| Camada | Responsabilidade | Tecnologia |
|--------|-----------------|------------|
| `ui/` | Renderizar formulários, exibir resultados | Streamlit |
| `calculadoras/` | Validar parâmetros, aplicar fórmulas, gerar memória de cálculo | Python puro |
| `data/` | Acessar dados (JSON, cache) | Python + Streamlit cache |
| `utils/` | Formatação, configuração de campos, PDF | Python puro |

## Arquivos envolvidos
- `ui/form_servidor.py` → formulário de dados do servidor (✅ concluído)
- `ui/cabecalho.py` → cabeçalho da calculadora (✅ concluído)
- `ui/selecao_verba.py` → seleção e cálculo de verbas (✅ concluído)
- `ui/config.py` → `CONFIG_CAMPOS` com metadados dos campos (✅ concluído)
- `main.py` → entry point do app refatorado (✅ integrado)
- `app.py` → arquivo original (referência, será descontinuado)
- `data/provedor_dados.py` → classe `ProvedorDadosFhemig` com acesso a dados
- `data/tabelas.json` → base de cargos, INSS, metadados das verbas e tabela GRS
- `calculadoras/base.py` → classe abstrata `CalculadoraVerba` e dataclass `ResultadoCalculo`
- `calculadoras/factory.py` → `REGISTRO_CALCULADORAS` mapeando nome da verba → instância
- `calculadoras/hora_extra.py` → `CalculadoraHoraExtra` (✅ implementada)
- `calculadoras/adicional_noturno.py` → `CalculadoraAdicionalNoturno` (✅ implementada)
- `calculadoras/gratificacao_final_semana.py` → `CalculadoraGratificacaoFinalSemana` (✅ implementada)
- `calculadoras/inss_mensal.py` → `CalculadoraINSS` (✅ implementada)
- `calculadoras/grs_dias.py` → `CalculadoraGRSDias` (✅ implementada)
- `calculadoras/decimo_terceiro.py` → `CalculadoraDecimoTerceiro` (✅ implementada)
- `utils/formatador_campos.py` → `FormatadorCampos` com `brl()` e `masp()`
- `utils/ui_callbacks.py` → `on_change_masp` (callback opcional)
- `utils/exportador_pdf.py` → exportação PDF (⬜ pendente)

## Progresso

### ✅ Módulo `ui/cabecalho.py` — Concluído
Classe `Cabecalho` com método `render()` que exibe:
- Título "🏥 Calculadora de Verbas Remuneratórias"
- Subtítulo "FHEMIG · DIGEPE / CCPT — Resumos Funcionais"
- Divisor (`st.divider()`)

### ✅ Módulo `ui/form_servidor.py` — Concluído

#### `__init__`
Dicionário `dados_servidor` com todas as chaves:
- `nome`, `masp`, `admissao`, `dt_admissao` (None), `dt_fim_efetiva` (None)
- `cargo_classe`, `cargo_nivel`, `cargo_grau`
- `ch_semanal` (0), `ch_mensal` (0), `vencimento_basico` (0.0)

#### `render()` — Estrutura geral
1. CSS para ocultar setinhas dos `number_input`
2. `with st.expander("Dados do Servidor", expanded=True):`
3. `ds = st.session_state["dados_servidor"]`
4. 3 colunas com: Nome, MASP, Admissão
5. 2 colunas com: Data de Admissão, Data Fim Efetiva (`date_input`, preservam estado)

#### Campos de cargo
Linha 1 — 3 colunas: Cargo / Classe, Nível, Grau
Linha 2 — 2 colunas: C.H. Semanal (selectbox) + C.H. Mensal (disabled, calculado automaticamente)

#### Cálculo de C.H. Mensal
```python
if ds["ch_semanal"] != "- Selecione -":
    ds["ch_mensal"] = int(ds["ch_semanal"] / 5 * 30)
```
Fórmula: `ch_semanal ÷ 5 × 30`. Campo exibido como `disabled` ao lado do selectbox.

#### Busca automática de cargo
- Se todos os 4 campos preenchidos → busca via `ProvedorDadosFhemig.buscar_cargo()`
- Se encontrado → preenche `vencimento_basico` e exibe `st.success()`
- Se não encontrado → aviso + campo manual apenas para Vencimento Básico (C.H. Mensal já foi calculada)

### ✅ Módulo `ui/config.py` — Concluído
Arquivo `CONFIG_CAMPOS` movido de `utils/` para `ui/` para melhor organização.

Campos configurados (13 campos):
- `vencimento_basico`: `{"label": "Vencimento Básico (R$)", "tipo": "moeda"}`
- `ad_desempenho`: `{"label": "Adicional de Desempenho (R$)", "tipo": "moeda"}`
- `carga_horaria_mensal`: `{"label": "Carga Horária Mensal (h/mês)", "tipo": "hora_mensal"}`
- `horas_realizadas`: `{"label": "Horas Realizadas", "tipo": "horas_realizadas"}`
- `ano_referencia`: `{"label": "Ano de Referência", "tipo": "ano"}`
- `grs_risco`: `{"label": "Nível de Risco", "tipo": "select_risco"}`
- `dias_trabalhados`: `{"label": "Nº de Dias Trabalhados no Mês", "tipo": "dias"}`
- `abono_emergencia`: `{"label": "Abono de Emergência (R$)", "tipo": "moeda"}`
- `grat_final_semana`: `{"label": "Grat. Final de Semana (R$)", "tipo": "moeda"}`
- `adicional_noturno`: `{"label": "Adicional Noturno (R$)", "tipo": "moeda"}`
- `numero_meses`: `{"label": "Nº de Meses de Direito", "tipo": "meses"}`

**Nota:** Os campos `grat_final_semana` e `adicional_noturno` são preenchidos automaticamente com o último valor calculado no histórico (caso exista), servindo como dependências para a Calculadora de 13º Salário.

### ✅ Módulo `ui/selecao_verba.py` — Concluído
- `__init__()` com `historico` (lista), `ultimo_resultado` (`None`) e `ultima_verba_selecionada` (`None`)
- `render()` com selectbox de verbas, exibição de código + tag Vantagem/Desconto
- **Detecção de mudança de verba**: quando o usuário troca o selectbox, `ultimo_resultado` é limpo automaticamente, fazendo resultado + competência sumirem
- **Histórico sempre visível**: `_render_historico()` é chamado no final do `render()`, fora de qualquer condicional — a tabela persiste mesmo ao trocar de verba
- Roteamento para `_render_calculadora()` passando `nome_verba`
- `_render_calculadora()` com:
  - Exibição da fórmula via `st.caption()`
  - Geração dinâmica dos campos usando `CONFIG_CAMPOS`
  - Valores default especiais para cada campo:
    - `vencimento_basico` → busca do cabeçalho (`dados_servidor`)
    - `carga_horaria_mensal` → busca do cabeçalho (`ch_mensal`)
    - `ano_referencia` → ano atual como default (selectbox com 2024, 2025, 2026)
    - `grs_risco` → selectbox com opções "Risco Médio (R$ 160,20)" / "Risco Alto (R$ 320,40)"
    - `dias_trabalhados` → default 1, min 1, max 30
    - `numero_meses` → default 12, min 1, max 12
    - `grat_final_semana` → último valor de GFS no histórico (ou 0.0)
    - `adicional_noturno` → último valor de Adicional Noturno no histórico (ou 0.0)
    - `ad_desempenho` → 0.0
    - `abono_emergencia` → 0.0
    - demais → 0
  - Bug conhecido: `desabilitado = False` sobrescreve a lógica que desabilitaria `vencimento_basico` e `carga_horaria_mensal` (linhas 132-133)
  - Botão "Calcular" que chama `calculadora.calcular(**valores)` e salva em `ultimo_resultado`
- `_render_resultado()` (fora do `if`, persiste entre rerenders) com:
  - `st.metric()` mostrando o valor calculado
  - `st.expander("Ver memória de cálculo", expanded=True)` com `st.code()`
  - Campo **"📅 Competência"** (mês/ano) via `_render_competencia()` — default: mês anterior e ano corrente
  - Botão "➕ Adicionar à lista" que insere no histórico (com competência) e chama `st.rerun()`
- `_render_historico()` com:
  - `st.dataframe()` com colunas: Verba, Código, Tipo, Competência, Valor (R$)
  - Totais separados: Total Vantagens, Total Descontos, Líquido
  - Botão "🗑️ Remover último" (usa `pop()` na lista)
  - Botão "🗑️ Limpar lista" (zera a lista)

### ✅ Módulo `calculadoras/` — 6 calculadoras implementadas

| Verba | Classe | Arquivo | Status |
|-------|--------|---------|--------|
| Hora Extra | `CalculadoraHoraExtra` | `calculadoras/hora_extra.py` | ✅ |
| Adicional Noturno | `CalculadoraAdicionalNoturno` | `calculadoras/adicional_noturno.py` | ✅ |
| Gratificação de Final de Semana | `CalculadoraGratificacaoFinalSemana` | `calculadoras/gratificacao_final_semana.py` | ✅ |
| INSS Mensal | `CalculadoraINSS` | `calculadoras/inss_mensal.py` | ✅ |
| GRS — Dias | `CalculadoraGRSDias` | `calculadoras/grs_dias.py` | ✅ |
| 13º Salário | `CalculadoraDecimoTerceiro` | `calculadoras/decimo_terceiro.py` | ✅ |

Cada calculadora implementa:
- `descricao_formula` → texto explicativo da fórmula
- `campos_necessarios` → lista de nomes dos campos
- `calcular(**kwargs)` → retorna `ResultadoCalculo(valor, memoria_calculo)`

#### CalculadoraINSS — Detalhes
- **Campos:** `vencimento_basico` + `ano_referencia`
- **Fórmula:** `INSS = Vencimento Básico × Alíquota da faixa − Dedução da faixa`
- **Tabela progressiva:** Percorre faixas até encontrar o limite correspondente
- **Ano de referência:** Input do usuário (selectbox 2024, 2025, 2026)
- **Memória de cálculo:** Exibe vencimento, faixa, alíquota, dedução e resultado

#### CalculadoraGRSDias — Detalhes
- **Campos:** `grs_risco` (selectbox) + `dias_trabalhados` (1-30)
- **Fórmula:** `GRS Proporcional = Valor GRS ÷ 30 × Dias Trabalhados no Mês`
- **Valor GRS:** Buscado de `tabelas.json` → `tabela_grs`:
  - `risco_medio`: R$ 160,20
  - `risco_alto`: R$ 320,40
- **Memória de cálculo:** Exibe valor GRS, valor diário, dias trabalhados e resultado

#### CalculadoraDecimoTerceiro — Detalhes
- **Campos:** `vencimento_basico`, `ad_desempenho`, `abono_emergencia`, `grat_final_semana`, `adicional_noturno`, `grs_risco`, `numero_meses`
- **Fórmula:** `13º = (Venc + Ad.Desemp + Ab.Emerg + GFS + Ad.Noturno + GRS) ÷ 12 × Nº Meses`
- **GRS:** Busca valor de `tabelas.json` conforme nível selecionado (Médio/Alto)
- **Dependências:** Os campos `grat_final_semana` e `adicional_noturno` são preenchidos automaticamente com o último valor calculado no histórico (se existir)
- **Memória de cálculo:** Exibe cada parcela somada, a base total, divisão por 12 e multiplicação pelos meses

## Decisões de design

### Comportamento ao trocar de verba
- `ultimo_resultado` é limpo → resultado + competência + botão "Adicionar" somem
- `_render_historico()` está fora do `if calculadora:` → tabela do histórico **continua visível**
- A detecção usa `ultima_verba_selecionada` no `session_state` para distinguir troca intencional de rerenderização normal

### Competência (mês/ano)
- Implementado como dois `selectbox` lado a lado (mês 1-12, ano 2000-2030)
- Default: mês anterior ao corrente, ano corrente
- Salvo no histórico junto com os demais dados da verba
- Exibido como coluna na tabela do histórico

### Ano de referência no INSS
- A `CalculadoraINSS` tem `ano_referencia` como campo de input do usuário (selectbox com anos: 2024, 2025, 2026)
- O ano selecionado define qual tabela do `tabelas.json` será usada no cálculo progressivo
- As demais verbas não dependem de ano (percentuais fixos por lei)

### Campos com dependência do histórico (13º Salário)
- `grat_final_semana` e `adicional_noturno` são campos do tipo moeda que buscam automaticamente o último valor calculado no histórico para a respectiva verba
- Isso permite que o 13º Salário some valores já calculados de GFS e Adicional Noturno sem que o usuário precise redigitar
- Se não houver histórico, o default é 0.0

### GRS — Valor por nível de risco
- Armazenado em `data/tabelas.json` na seção `tabela_grs`
- Acessado via `ProvedorDadosFhemig.obter_valor_grs(nivel)`
- Dois níveis: risco_medio (R$ 160,20) e risco_alto (R$ 320,40)
- Usado tanto pela `CalculadoraGRSDias` quanto pela `CalculadoraDecimoTerceiro`

### Total na lista
- Exibidos 3 valores: Total Vantagens, Total Descontos, Líquido
- Líquido = Vantagens − Descontos

## Mudanças já aplicadas
- `data/tabelas.json`: `ch_semanal` alterado de string para int; `vencimento` renomeado para `vencimento_basico`; `ch_mensal` removido dos cargos (calculado por fórmula); `verbas_meta` renomeado para `verbas`; `grupos` removidos; `tabela_grs` adicionado com `risco_medio` e `risco_alto`
- `data/provedor_dados.py`: `buscar_cargo()` aceita 4º parâmetro `ch_semanal` (int); `obter_verbas()` adicionado; `obter_tabela_inss(ano)` implementado; `obter_valor_grs(nivel)` implementado
- `ui/form_servidor.py`: implementação completa com C.H. Mensal calculado automaticamente
- `ui/cabecalho.py`: criado com classe `Cabecalho`
- `ui/config.py`: `CONFIG_CAMPOS` movido de `utils/` para `ui/`; adicionados campos `ano_referencia`, `grs_risco`, `dias_trabalhados`, `abono_emergencia`, `grat_final_semana`, `adicional_noturno`, `numero_meses`
- `ui/selecao_verba.py`: renderização dinâmica de campos, botão calcular, resultado persistente, competência mês/ano, detecção de mudança de verba, histórico sempre visível com totais, remover último e limpar lista; valores default especiais para GRS, dias trabalhados, meses, dependências do histórico (GFS, Ad.Noturno)
- `calculadoras/inss_mensal.py`: implementado com lógica progressiva e campo `ano_referencia`
- `calculadoras/grs_dias.py`: implementada com lógica proporcional aos dias trabalhados
- `calculadoras/decimo_terceiro.py`: implementada com soma de múltiplas verbas e dependência do histórico
- `calculadoras/factory.py`: registradas 6 calculadoras (Hora Extra, Adicional Noturno, GFS, INSS, GRS Dias, 13º Salário)
- `calculadoras/__init__.py`: imports atualizados para incluir todas as calculadoras
- `main.py`: entry point do app refatorado

## Como testar
```bash
streamlit run main.py
```

## Pendências — Próximas etapas

### 🔴 Imediato — Correções pendentes
- [ ] Corrigir `desabilitado = False` na linha 133 de `ui/selecao_verba.py` (campos vinculados ao cabeçalho — `vencimento_basico`, `carga_horaria_mensal` — devem ficar disabled)

### Etapa 2 — Implementar calculadoras de desconto simples

Próximas calculadoras a implementar, baseado no `app.py`:

| # | Verba | Código | Fórmula | Arquivo |
|---|-------|--------|---------|---------|
| 1 | Desconto de IPSEMG (3,2%) | 7700 | `vencimento_basico * 0.032` | `calculadoras/ipsemg.py` |
| 2 | Desconto de Custeio (4%) | 9018 | `vencimento_basico * 0.04` | `calculadoras/custeio.py` |

São calculadoras de **percentual fixo**, sem tabelas progressivas. Cada uma terá:
- `descricao_formula`: texto da fórmula
- `campos_necessarios`: `["vencimento_basico"]`
- `calcular(vencimento_basico)`: multiplicação + memória de cálculo

### Etapa 3 — Implementar calculadoras restantes (~13 verbas)
Criar classes para as demais verbas (GIEFS, GRS, Férias, Faltas, etc.) — estimativa de 13 verbas restantes com base no `app.py`.

### Etapa 4 — Expandir `ui/config.py`
Adicionar todos os campos necessários ao `CONFIG_CAMPOS` conforme novas calculadoras forem implementadas.

### Etapa 5 — Implementar `utils/exportador_pdf.py`
Migrar função `gerar_pdf()` do `app.py`.

### Etapa 6 — Descontinuar `app.py`
Após todas as funcionalidades migradas, remover ou arquivar o `app.py` original.