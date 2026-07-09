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
└──────────────────────┬──────────────────────┘
                       │ usa
┌──────────────────────▼──────────────────────┐
│  calculadoras/ (Lógica de negócio)          │
│  - base.py           → ABC + ResultadoCalculo│
│  - factory.py        → REGISTRO_CALCULADORAS│
│  - hora_extra.py     → CalculadoraHoraExtra │
│  - adicional_noturno.py → ...               │
│  - gratificacao_final_semana.py → ...       │
│  - inss_mensal.py    → CalculadoraINSS (esboço)│
│  - (demais verbas a implementar)            │
└──────────────────────┬──────────────────────┘
                       │ usa
┌──────────────────────▼──────────────────────┐
│  data/ (Dados)                              │
│  - provedor_dados.py → ProvedorDadosFhemig  │
│  - tabelas.json      → Cargos, INSS, verbas │
└──────────────────────┬──────────────────────┘
                       │ usa
┌──────────────────────▼──────────────────────┐
│  utils/ (Utilitários)                       │
│  - formatador_campos.py → FormatadorCampos  │
│  - ui_config.py         → CONFIG_CAMPOS     │
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
- `ui/selecao_verba.py` → seleção e cálculo de verbas (⬜ em andamento)
- `main.py` → entry point do app refatorado (✅ integrado)
- `app.py` → arquivo original (referência, será descontinuado)
- `data/provedor_dados.py` → classe `ProvedorDadosFhemig` com acesso a dados
- `data/tabelas.json` → base de cargos, INSS e metadados das verbas
- `calculadoras/base.py` → classe abstrata `CalculadoraVerba` e dataclass `ResultadoCalculo`
- `calculadoras/factory.py` → `REGISTRO_CALCULADORAS` mapeando nome da verba → instância
- `calculadoras/hora_extra.py` → `CalculadoraHoraExtra` (✅ implementada)
- `calculadoras/adicional_noturno.py` → `CalculadoraAdicionalNoturno` (✅ implementada)
- `calculadoras/gratificacao_final_semana.py` → `CalculadoraGratificacaoFinalSemana` (✅ implementada)
- `calculadoras/inss_mensal.py` → `CalculadoraINSS` (⬜ esboço, lógica de cálculo pendente)
- `utils/formatador_campos.py` → `FormatadorCampos` com `brl()` e `masp()`
- `utils/ui_config.py` → `CONFIG_CAMPOS` com metadados dos campos (label, tipo)
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

### ✅ Módulo `calculadoras/` — 3 calculadoras implementadas + 1 esboço

| Verba | Classe | Arquivo | Status |
|-------|--------|---------|--------|
| Hora Extra | `CalculadoraHoraExtra` | `calculadoras/hora_extra.py` | ✅ |
| Adicional Noturno | `CalculadoraAdicionalNoturno` | `calculadoras/adicional_noturno.py` | ✅ |
| Gratificação de Final de Semana | `CalculadoraGratificacaoFinalSemana` | `calculadoras/gratificacao_final_semana.py` | ✅ |
| INSS Mensal | `CalculadoraINSS` | `calculadoras/inss_mensal.py` | ⬜ esboço |

Cada calculadora implementa:
- `descricao_formula` → texto explicativo da fórmula
- `campos_necessarios` → lista de nomes dos campos
- `calcular(**kwargs)` → retorna `ResultadoCalculo(valor, memoria_calculo)`

### ⬜ Módulo `ui/selecao_verba.py` — Em andamento

#### ✅ Implementado
- `__init__()` com `historico` (lista), `ultimo_resultado` (`None`) e `ultima_verba_selecionada` (`None`)
- `render()` com selectbox de verbas, exibição de código + tag Vantagem/Desconto
- **Detecção de mudança de verba**: quando o usuário troca o selectbox, `ultimo_resultado` é limpo automaticamente, fazendo resultado + competência sumirem
- **Histórico sempre visível**: `_render_historico()` é chamado no final do `render()`, fora de qualquer condicional — a tabela persiste mesmo ao trocar de verba
- Roteamento para `_render_calculadora()` passando `nome_verba`
- `_render_calculadora()` com:
  - Exibição da fórmula via `st.caption()`
  - Geração dinâmica dos campos usando `CONFIG_CAMPOS`
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

#### ⬜ Falta implementar
- [ ] `_exibir_conferencia()` — campo para comparar valor calculado com valor informado pela unidade
- [ ] `_render_fallback()` — para verbas sem calculadora registrada (mostrar campos manuais)
- [ ] Corrigir linha 81: `desabilitado = False` sobrescreve `disabled` dos campos vinculados ao cabeçalho

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
- A `CalculadoraINSS` terá `ano_referencia` como campo de input do usuário (selectbox com anos: 2024, 2025, 2026)
- O ano selecionado define qual tabela do `tabelas.json` será usada no cálculo progressivo
- As demais verbas não dependem de ano (percentuais fixos por lei)

### Total na lista
- Exibidos 3 valores: Total Vantagens, Total Descontos, Líquido
- Líquido = Vantagens − Descontos

## Mudanças já aplicadas
- `data/tabelas.json`: `ch_semanal` alterado de string para int; `vencimento` renomeado para `vencimento_basico`; `ch_mensal` removido dos cargos (calculado por fórmula); `verbas_meta` renomeado para `verbas`; `grupos` removido
- `data/provedor_dados.py`: `buscar_cargo()` aceita 4º parâmetro `ch_semanal` (int); `obter_verbas()` adicionado
- `ui/form_servidor.py`: implementação completa com C.H. Mensal calculado automaticamente
- `ui/cabecalho.py`: criado com classe `Cabecalho`
- `ui/selecao_verba.py`: renderização dinâmica de campos, botão calcular, resultado persistente, competência mês/ano, detecção de mudança de verba, histórico sempre visível com totais, remover último e limpar lista
- `calculadoras/`: 3 calculadoras implementadas (Hora Extra, Adicional Noturno, Gratificação de Final de Semana); `inss_mensal.py` como esboço
- `main.py`: entry point do app refatorado

## Como testar
```bash
streamlit run main.py
```

## Pendências — Próximas etapas

### 🔴 Imediato — Finalizar `ui/selecao_verba.py`
- [ ] `_exibir_conferencia()` com campo de valor da unidade e comparação (calculado vs unidade vs diferença)
- [ ] `_render_fallback()` para verbas sem calculadora registrada
- [ ] Corrigir `desabilitado = False` na linha 81 (campos vinculados ao cabeçalho devem ficar disabled)

### Etapa 1 — Finalizar `CalculadoraINSS` e registrá-la

Arquivos envolvidos: `calculadoras/inss_mensal.py`, `utils/ui_config.py`, `ui/selecao_verba.py`, `calculadoras/factory.py`, `calculadoras/__init__.py`

- [ ] `calculadoras/inss_mensal.py`: adicionar `ano_referencia` em `campos_necessarios` e nos parâmetros de `calcular()`
- [ ] `calculadoras/inss_mensal.py`: implementar lógica progressiva com `ProvedorDadosFhemig.obter_tabela_inss(ano_referencia)`
- [ ] `utils/ui_config.py`: adicionar `"ano_referencia": {"label": "Ano de Referência", "tipo": "ano"}` ao `CONFIG_CAMPOS`
- [ ] `ui/selecao_verba.py`: adicionar tratamento para `config.get("tipo") == "ano"` no loop da `_render_calculadora()` — renderizar `st.selectbox` com `options=[2024, 2025, 2026]`, `index=2`
- [ ] `calculadoras/factory.py`: adicionar `CalculadoraINSS()` ao `REGISTRO_CALCULADORAS`
- [ ] `calculadoras/__init__.py`: importar `CalculadoraINSS`

### Etapa 2 — Implementar calculadoras de desconto simples
- [ ] `CalculadoraIPSEMG` — `vencimento_basico * 0.032`
- [ ] `CalculadoraCusteio` — `vencimento_basico * 0.04`

### Etapa 3 — Implementar calculadoras restantes (~15 verbas)
Criar classes para as demais verbas (13º Salário, GIEFS, GRS, Férias, Faltas, etc.)

### Etapa 4 — Expandir `utils/ui_config.py`
Adicionar todos os campos necessários ao `CONFIG_CAMPOS`.

### Etapa 5 — Implementar `utils/exportador_pdf.py`
Migrar função `gerar_pdf()` do `app.py`.

### Etapa 6 — Descontinuar `app.py`
Após todas as funcionalidades migradas, remover ou arquivar o `app.py` original.