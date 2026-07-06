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
- `ui/selecao_verba.py` → seleção e cálculo de verbas (⬜ em andamento — ver bugs abaixo)
- `main.py` → entry point do app refatorado (✅ integrado com SelecaoVerba)
- `app.py` → arquivo original (referência, será descontinuado)
- `data/provedor_dados.py` → classe `ProvedorDadosFhemig` com acesso a dados
- `data/tabelas.json` → base de cargos, INSS e metadados das verbas
- `calculadoras/base.py` → classe abstrata `CalculadoraVerba` e dataclass `ResultadoCalculo`
- `calculadoras/factory.py` → `REGISTRO_CALCULADORAS` mapeando nome da verba → instância
- `calculadoras/hora_extra.py` → `CalculadoraHoraExtra` (✅ implementada)
- `calculadoras/adicional_noturno.py` → `CalculadoraAdicionalNoturno` (✅ implementada)
- `calculadoras/gratificacao_final_semana.py` → `CalculadoraGratificacaoFinalSemana` (✅ implementada)
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

#### Passo 1 — `__init__`
Dicionário `dados_servidor` com todas as chaves:
- `nome`, `masp`, `admissao`, `dt_admissao` (None), `dt_fim_efetiva` (None)
- `cargo_classe`, `cargo_nivel`, `cargo_grau`
- `ch_semanal` (0), `ch_mensal` (0), `vencimento_basico` (0.0)

#### Passo 2 — Estrutura do `render()`
1. CSS para ocultar setinhas dos `number_input`
2. `with st.expander("Dados do Servidor", expanded=True):`
3. `ds = st.session_state["dados_servidor"]`
4. 3 colunas com: Nome, MASP, Admissão

#### Passo 3 — Datas
- `st.date_input` (formato DD/MM/YYYY) vinculado ao `ds` (preserva estado)
- `dt_admissao` → "Data de Admissão"
- `dt_fim_efetiva` → "Data Fim Efetiva"

#### Passo 4 — Campos de cargo
4 colunas, todos salvos em `ds[...]`:
- Cargo / Classe (text_input, `.upper().strip()`)
- Nível (text_input, `.strip()`)
- Grau (text_input, `.upper().strip()`)
- C.H. Semanal (selectbox: "- Selecione -", 20, 30, 40, 44)

#### Passo 5 — Busca automática de cargo
```python
cargo_encontrado = ProvedorDadosFhemig.buscar_cargo(
    ds["cargo_classe"], ds["cargo_nivel"], ds["cargo_grau"], ds["ch_semanal"]
)
if cargo_encontrado:
    ds["ch_mensal"] = cargo_encontrado["ch_mensal"]
    ds["vencimento_basico"] = cargo_encontrado["vencimento_basico"]
    st.success(...)
```

#### Passo 6 — Fallback manual
Se cargo não encontrado:
- Aviso `st.warning("⚠️ Cargo não encontrado...")`
- Selectbox para C.H. Mensal (120, 180, 240, 264)
- `number_input` para Vencimento Básico

### ✅ Módulo `calculadoras/` — 3 calculadoras implementadas

| Verba | Classe | Arquivo |
|-------|--------|---------|
| Hora Extra | `CalculadoraHoraExtra` | `calculadoras/hora_extra.py` |
| Adicional Noturno | `CalculadoraAdicionalNoturno` | `calculadoras/adicional_noturno.py` |
| Gratificação de Final de Semana | `CalculadoraGratificacaoFinalSemana` | `calculadoras/gratificacao_final_semana.py` |

Cada calculadora implementa:
- `descricao_formula` → texto explicativo da fórmula
- `campos_necessarios` → lista de nomes dos campos que precisa
- `calcular(**kwargs)` → retorna `ResultadoCalculo(valor, memoria_calculo)`

### ⬜ Módulo `ui/selecao_verba.py` — Em andamento

#### Implementado
- `__init__()` com inicialização de `historico` (lista) e `ultimo_resultado` (lista — precisa ser `None`)
- `render()` com selectbox de verbas, exibição de código + tag Vantagem/Desconto, e roteamento para `_render_calculadora()`
- `_render_calculadora()` com geração dinâmica de campos via `CONFIG_CAMPOS`, selectbox para carga horária, e `st.caption()` para fórmula

#### Bugs conhecidos (a corrigir)
1. `ultimo_resultado` inicializado como `[]` em vez de `None`
2. Nomes dos campos no `CONFIG_CAMPOS` (`"vencimento_basico"`, `"carga_horaria_mensal"`) não correspondem aos nomes usados pelas calculadoras (`"vencimento"`, `"carga_horaria"`) — precisa de um `MAPEAMENTO_CAMPOS` ou alinhar os nomes
3. Condições `if campo ==` usam nomes do CONFIG_CAMPOS em vez dos nomes reais das calculadoras
4. Selectbox de carga horária sem `index` e com `"- Selecione -"` nas opções (pode causar crash)
5. `_render_fallback()` não foi implementado — verbas sem calculadora não mostram nada
6. `_exibir_resultado()` não foi implementado — resultado nunca é exibido

## Mudanças já aplicadas
- `data/tabelas.json`: `ch_semanal` alterado de string para int; `vencimento` renomeado para `vencimento_basico`; `verbas_meta` renomeado para `verbas`; `grupos` removido (não era utilizado)
- `data/provedor_dados.py`: `buscar_cargo()` aceita 4º parâmetro `ch_semanal` (int) e filtra por ele; `obter_metadados_verbas()` e `obter_grupos_verbas()` removidos; `obter_verbas()` adicionado
- `ui/form_servidor.py`: implementação completa dos Passos 1 a 6
- `ui/cabecalho.py`: criado com classe `Cabecalho`
- `ui/selecao_verba.py`: criado com classe `SelecaoVerba` com `__init__`, `render()`, `_render_calculadora()`
- `main.py`: entry point do app refatorado com `SelecaoVerba` integrado
- `utils/ui_config.py`: `CONFIG_CAMPOS` com 4 campos (nomes pendentes de alinhamento com as calculadoras)

## Como testar
```bash
streamlit run main.py
```

## Pendências — Plano de Implementação

### 🔴 Corrigir bugs no `ui/selecao_verba.py`
- [ ] `ultimo_resultado` = `[]` → `None`
- [ ] Adicionar `MAPEAMENTO_CAMPOS` para traduzir nomes das calculadoras para nomes do `CONFIG_CAMPOS`
- [ ] Corrigir condições `if campo ==` para usar nomes reais das calculadoras
- [ ] Remover `"- Selecione -"` do selectbox de carga horária e adicionar `index`
- [ ] Adicionar `_render_fallback()` e `else` no `render()`
- [ ] Adicionar `_exibir_resultado()` com resultado, memória, adicionar à lista e conferência

### Etapa 1 — Implementar calculadoras restantes (18 verbas)
Criar classes no pacote `calculadoras/` para as verbas que ainda não têm implementação.

### Etapa 2 — Expandir `utils/ui_config.py`
Adicionar todos os campos necessários ao `CONFIG_CAMPOS`.

### Etapa 3 — Atualizar `calculadoras/factory.py`
Adicionar as 18 novas calculadoras ao `REGISTRO_CALCULADORAS`.

### Etapa 4 — Finalizar `ui/selecao_verba.py`
Completar implementação após correção dos bugs.

### Etapa 5 — Atualizar `main.py`
Adicionar seção "Lista de cálculos realizados" com tabela, totais e botão de limpar.

### Etapa 6 — Implementar `utils/exportador_pdf.py`
Migrar função `gerar_pdf()` do `app.py`.

### Etapa 7 — Descontinuar `app.py`
Após todas as funcionalidades migradas, remover ou arquivar o `app.py` original.