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
- `calculadoras/inss_mensal.py` → `CalculadoraINSS` (⬜ esboço, implementar lógica depois)
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

#### Implementado
- `__init__()` com inicialização de `historico` (lista) e `ultimo_resultado` (dict)
- `render()` com selectbox de verbas, exibição de código + tag Vantagem/Desconto
- Roteamento para `_render_calculadora()` quando existe calculadora registrada
- `_render_calculadora()` com:
  - Exibição da fórmula via `st.caption()`
  - Geração dinâmica dos campos usando `CONFIG_CAMPOS`
  - Botão "Calcular" que chama `calculadora.calcular(**valores)` e salva em `ultimo_resultado`
- `_exibir_resultado()` com:
  - `st.metric()` mostrando o valor calculado
  - `st.expander("Ver memória de cálculo")` com `st.code()` para exibir a memória

#### ⚠️ Bugs conhecidos (não prioritários)
- Linha 81: `desabilitado = False` sobrescreve a atribuição anterior (linha 80) — campos disabled não funcionam
- `_exibir_resultado()` é chamado **dentro** do `if st.button`, então só aparece imediatamente após o clique, não persiste entre rerenders
- `ultimo_resultado` inicializado como `{}` (dict vazio) em vez de `None` — na rerenderização, `_exibir_resultado()` vai tentar acessar `ur["valor"]` e quebrar porque o dict está vazio
- Selectbox de carga horária sem `index` — não está sendo usado no momento (carga_horaria_mensal usa `number_input`)

> **Decisão:** Os bugs acima serão ignorados por enquanto. Se causarem problemas no futuro, voltamos e corrigimos.

#### Falta implementar
- [ ] Passar `verba_input` (nome da verba) para `_render_calculadora()` e salvar no `ultimo_resultado`
- [ ] Botão "Adicionar à lista" dentro de `_exibir_resultado()` (sem campo de referência)
- [ ] Método `_exibir_historico()` com:
  - Tabela (`st.dataframe`) com colunas: Verba, Código, Valor (R$)
  - Totais separados: Total Vantagens, Total Descontos, Líquido
  - Botão "Remover último" (usa `pop()` na lista)
  - Botão "Limpar lista"
- [ ] Método `_exibir_conferencia()` com campo de valor da unidade e comparação (calculado vs unidade vs diferença)
- [ ] Implementar `_render_fallback()` para verbas sem calculadora registrada

## Decisões de design

### Ano de referência
- O ano **não** será implementado como campo de cálculo por enquanto
- A calculadora de INSS usará a tabela de 2026 fixa (lógica básica)
- As demais verbas não dependem de ano (percentuais fixos por lei)
- O ano de referência como metadado da lista fica para uma etapa futura

### Funcionalidade "Adicionar à lista"
- Não terá campo de referência (mês/ano) por enquanto
- Apenas botão "Adicionar" que insere o item no histórico
- Os itens aparecem na tabela com nome da verba, código e valor

### Total na lista
- Serão exibidos 3 valores: Total Vantagens, Total Descontos, Líquido
- Descontos são subtraídos do total (multiplicados por -1 no cálculo do líquido)

## Mudanças já aplicadas
- `data/tabelas.json`: `ch_semanal` alterado de string para int; `vencimento` renomeado para `vencimento_basico`; `ch_mensal` removido dos cargos (calculado por fórmula); `verbas_meta` renomeado para `verbas`; `grupos` removido
- `data/provedor_dados.py`: `buscar_cargo()` aceita 4º parâmetro `ch_semanal` (int); `obter_verbas()` adicionado
- `ui/form_servidor.py`: implementação completa com C.H. Mensal calculado automaticamente
- `ui/cabecalho.py`: criado com classe `Cabecalho`
- `ui/selecao_verba.py`: renderização dinâmica de campos, botão calcular, exibição de resultado e memória de cálculo
- `calculadoras/`: nomes dos campos alinhados com `CONFIG_CAMPOS`
- `main.py`: entry point do app refatorado
- `calculadoras/inss_mensal.py`: criado esboço da calculadora (lógica de negócio pendente)

## Como testar
```bash
streamlit run main.py
```

## Pendências — Próximas etapas

### 🔴 Imediato — Finalizar `ui/selecao_verba.py`
- [ ] Passar nome da verba para `_render_calculadora()` e salvar no resultado
- [ ] Botão "Adicionar à lista" (sem referência)
- [ ] `_exibir_historico()` com tabela + totais (Vantagens/Descontos/Líquido) + Remover último + Limpar
- [ ] `_exibir_conferencia()` com campo de valor da unidade
- [ ] `_render_fallback()` para verbas sem calculadora

### Etapa 1 — Implementar calculadoras de desconto (3 verbas)
- [ ] `CalculadoraINSS` — lógica básica com tabela 2026 fixa
- [ ] `CalculadoraIPSEMG` — `vencimento_basico * 0.032`
- [ ] `CalculadoraCusteio` — `vencimento_basico * 0.04`
- [ ] Registrar as 3 no `REGISTRO_CALCULADORAS` em `factory.py`

### Etapa 2 — Implementar calculadoras restantes (~15 verbas)
Criar classes no pacote `calculadoras/` para as verbas que ainda não têm implementação.

### Etapa 3 — Expandir `utils/ui_config.py`
Adicionar todos os campos necessários ao `CONFIG_CAMPOS`.

### Etapa 4 — Implementar `utils/exportador_pdf.py`
Migrar função `gerar_pdf()` do `app.py`.

### Etapa 5 — Descontinuar `app.py`
Após todas as funcionalidades migradas, remover ou arquivar o `app.py` original.