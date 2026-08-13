# Contexto do Projeto — Calculadora de Verbas FHEMIG

> **Propósito:** Refatoração do `app.py` (monolítico) para arquitetura modular com pacotes e OOP.
> **Stack:** Python + Streamlit + ReportLab (PDF) + Pandas
> **Entrypoint atual:** `main.py` (novo) | `app.py` (legado, sendo substituído)

---

## 1. Arquitetura do Projeto

```
calculadora-verbas-fhemig/
├── main.py                    # Entrypoint da versão modular
├── app.py                     # Versão monolítica legada (a ser substituída)
├── contexto.md                # Este arquivo
├── dúvidas.md                 # Dúvidas em aberto sobre regras de negócio
├── requirements.txt           # streamlit, reportlab, pandas
│
├── calculadoras/              # Pacote de classes de cálculo (OOP)
│   ├── __init__.py            # Exporta classes + factory
│   ├── base.py                # Classe abstrata CalculadoraVerba + ResultadoCalculo
│   ├── factory.py             # REGISTRO_CALCULADORAS (conecta UI às classes)
│   ├── hora_extra.py          # ✅ Implementada
│   ├── adicional_noturno.py   # ✅ Implementada
│   ├── gratificacao_final_semana.py  # ✅ Implementada
│   ├── grs_dias.py            # ✅ Implementada
│   ├── inss_mensal.py         # ✅ Implementada
│   ├── decimo_terceiro.py     # ✅ Implementada
│   ├── giefs_13.py            # ✅ Implementada
│   ├── piso_enfermagem_13.py  # ✅ Implementada
│   ├── giefs_dias.py          # ✅ Implementada
│   ├── giefs_meses.py         # ✅ Implementada
│   ├── giefs_terco_ferias.py  # ✅ Implementada (renomeado de giefs_ferias.py)
│   ├── inss_decimo_terceiro.py# ✅ Implementada
│   ├── grs_meses.py           # ✅ Implementada
│   ├── grs_13.py              # ✅ Implementada (nova)
│   ├── grs_desconto_horas.py  # ✅ Implementada
│   ├── ferias_terco.py        # ✅ Implementada (renomeado de terco_ferias.py)
│   ├── ferias_indenizadas.py  # ✅ Implementada
│   ├── faltas_horas.py        # ✅ Implementada
│   ├── faltas_dias.py         # ✅ Implementada
│   ├── ajuda_custo.py         # ✅ Implementada
│   ├── ajuda_custo_desconto.py# ✅ Implementada
│   ├── aumento_salarial.py    # ✅ Implementada
│   └── ipsemg.py              # ✅ Implementada
│
├── data/                      # Dados externos
│   ├── __init__.py
│   ├── provedor_dados.py      # ProvedorDadosFhemig (cache + acesso JSON)
│   └── tabelas.json           # Cargos, INSS, verbas, GRS, reajustes
│
├── ui/                        # Componentes de interface Streamlit
│   ├── __init__.py
│   ├── cabecalho.py           # Cabeçalho institucional
│   ├── config.py              # CONFIG_CAMPOS (labels dos campos dinâmicos)
│   ├── form_servidor.py       # Formulário de dados do servidor
│   └── selecao_verba.py       # Seleção + cálculo + histórico
│
└── utils/                     # Utilitários
    ├── __init__.py
    ├── formatador_campos.py   # FormatadorCampos (brl, masp, arredondar)
    ├── ui_callbacks.py        # on_change_masp, on_change_moeda
    └── exportador_pdf.py      # 🔴 VAZIO — aguardando implementação
```

---

## 2. O que já foi implementado (versão modular)

### 2.1 Calculadoras (23 de 23 — completa)

| Verba | Arquivo | Status |
|---|---|---|
| Hora Extra | `calculadoras/hora_extra.py` | ✅ |
| Adicional Noturno | `calculadoras/adicional_noturno.py` | ✅ |
| Gratificação de Final de Semana | `calculadoras/gratificacao_final_semana.py` | ✅ |
| GRS — Dias | `calculadoras/grs_dias.py` | ✅ |
| 13º Salário | `calculadoras/decimo_terceiro.py` | ✅ |
| GIEFS — 13º Salário | `calculadoras/giefs_13.py` | ✅ |
| Piso Enfermagem — 13º Salário | `calculadoras/piso_enfermagem_13.py` | ✅ |
| INSS Mensal (tabela progressiva) | `calculadoras/inss_mensal.py` | ✅ |
| INSS sobre 13º Salário | `calculadoras/inss_decimo_terceiro.py` | ✅ |
| GIEFS — Dias | `calculadoras/giefs_dias.py` | ✅ |
| GIEFS — Meses | `calculadoras/giefs_meses.py` | ✅ |
| GIEFS — 1/3 de Férias | `calculadoras/giefs_terco_ferias.py` | ✅ |
| GRS — Meses | `calculadoras/grs_meses.py` | ✅ |
| GRS — 13º Salário | `calculadoras/grs_13.py` | ✅ |
| GRS — Desconto de Horas | `calculadoras/grs_desconto_horas.py` | ✅ |
| 1/3 de Férias | `calculadoras/ferias_terco.py` | ✅ |
| Férias Indenizadas | `calculadoras/ferias_indenizadas.py` | ✅ |
| Faltas — Horas | `calculadoras/faltas_horas.py` | ✅ |
| Faltas — Dias | `calculadoras/faltas_dias.py` | ✅ |
| Ajuda de Custo Mensal | `calculadoras/ajuda_custo.py` | ✅ |
| Desconto de Ajuda de Custo | `calculadoras/ajuda_custo_desconto.py` | ✅ |
| Aumento Salarial | `calculadoras/aumento_salarial.py` | ✅ |
| Desconto de IPSEMG (3,2%) | `calculadoras/ipsemg.py` | ✅ |

### 2.2 Interface

- **Cabeçalho** com identidade visual FHEMIG/DIGEPE/CCPT
- **Formulário do servidor** com:
  - Nome, MASP, Admissão, Datas
  - Cargo (Classe/Nível/Grau) com busca automática no JSON
  - CH Semanal (select: 20/30/40/44, default 40) → CH Mensal calculada (÷5×30)
  - Vencimento básico preenchido automaticamente se cargo encontrado
- **Seleção de verba** com:
  - Selectbox carregado do JSON
  - Campos gerados dinamicamente via `CONFIG_CAMPOS`
  - Valores default vindos do formulário do servidor ou do histórico
  - CH Mensal como selectbox [120, 180, 240, 264] com default do formulário
  - GRS com opções dinâmicas (3 opções para verbas remuneratórias, 2 para GRS Dias)
- **Resultado** com memória de cálculo em expander
- **Competência** (mês/ano; apenas **ano** para todas as verbas de 13º: 13º Salário, GIEFS 13º, Piso 13º, GRS 13º e INSS sobre 13º)
- **Observação** (opcional, até 200 caracteres)
- **Histórico** em dataframe com totais (vantagens, descontos, líquido)
- Botões: "Remover último", "Limpar lista"

### 2.3 Dados

- `data/tabelas.json` com:
  - `tabela_cargos`: 4 registros (PENF, TOS, AGAS)
  - `tabela_inss`: 2024, 2025, 2026
  - `verbas`: 23 metadados (código + tipo)
  - `tabela_grs`: `nao_faz_jus: 0.0`, `risco_medio: 160.20`, `risco_alto: 320.40`
  - `tabela_reajustes`: `2024: 0.0462`, `2026: 0.0540`

### 2.4 Decisões de implementação recentes

- **GRS**: Parser **centralizado** em `ProvedorDadosFhemig.obter_valor_grs(grs_risco)` — recebe a string da UI e mapeia para a chave do JSON (`risco_medio`, `risco_alto`, `nao_faz_jus`). Eliminou os `_parser_nivel_grs` locais e parsers inline. UI dinâmica: verbas GRS (Dias, Meses, 13º, Desconto de Horas) exibem apenas "Risco Médio" e "Risco Alto"; demais verbas exibem as 3 opções.
- **CH Mensal**: Mudou de `number_input` para `selectbox` com opções [120, 180, 240, 264]. Default vem do formulário do servidor (CH Semanal ÷ 5 × 30). Se valor default não estiver nas opções, fallback para índice 2 (240).
- **CH Semanal**: Selectbox sem opção "Selecione", default = 40 (index 2).
- **Aumento Salarial**: Multi-alíquotas via `tabela_reajustes` no JSON. Usa o campo único `ano_referencia` (selectbox 2024/2026, sem 2025 por não haver reajuste nesse ano). No histórico, o nome vira "Aumento Salarial (2024)" / "Aumento Salarial (2026)" para diferenciar.
- **Campo unificado `ano_referencia`**: os antigos campos `ano_referencia` e `ano_reajuste` foram unificados em um só (`ano_referencia`). As chaves em `tabelas.json` continuam **string** (JSON não tem chave numérica); os provedores convertem na borda com `str(ano)` (`obter_tabela_inss` e `obter_aliquota_reajuste`). Opções por verba: Aumento Salarial → [2024, 2026]; demais → [2024, 2025, 2026].
- **Faltas — Dias e Faltas — Horas**: Fórmulas revisadas para incluir **Piso Enfermagem** na base. Faltas — Dias divide por 30; Faltas — Horas divide pela carga horária.
- **GRS — 13º Salário**: Nova verba (código 3171, Vantagem). Fórmula `Valor GRS ÷ 12 × Nº de Meses`. Usa `grs_risco` (selectbox) + `numero_meses`. Competência exibe apenas **ano** (como 13º Salário).
- **Parser GRS migrado**: `grs_desconto_horas.py`, `ferias_indenizadas.py` e `ferias_terco.py` tiveram o `_parser_nivel_grs` local removido, passando a chamar `ProvedorDadosFhemig.obter_valor_grs(grs_risco)` diretamente. Isso corrigiu um bug onde o valor da GRS sempre resultava em 0.0.
- **GRS — Desconto de Horas**: Campo `horas_realizadas` → `faltas_horas` (semântica correta para desconto por faltas). `descricao_formula` atualizada.
- **Férias Indenizadas**: **GIEFS removida** da regra de cálculo (confirmado que não entra). Fórmula agora `(Venc + Ab. Emergência + GRS + Ad. Noturno) ÷ 30 × Dias`.
- **Campo `valor_base` → `valor_giefs`**: Renomeado em `giefs_dias.py` e `giefs_meses.py` para clareza. **Removida a busca no histórico** — o valor da GIEFS é informado manualmente pelo usuário (default 0.0).
- **Campo `valor_base_desconto` → `valor_ajuda_custo`**: Renomeado no Desconto de Ajuda de Custo. **Adicionado pré-preenchimento** do histórico (última "Ajuda de Custo Mensal").
- **Arquivo `terco_ferias.py` → `ferias_terco.py`**: Renomeado (classe `CalculadoraTercoFerias` mantida).
- **GIEFS — Meses**: Simplificada para **campo único de valor** — fórmula `Valor GIEFS ÷ 6 × Parcelas` → `Valor total da GIEFS para o período`. O campo órfão `numero_parcelas` foi removido de `ui/config.py` e `ui/selecao_verba.py`.
- **Correção de renderização GIEFS — Meses**: Renomeada a verba `"GIEFS — Meses (parcelas)"` → `"GIEFS — Meses"` no `data/tabelas.json`, alinhando com o registro do `factory.py` (resolvia o bug de verba não renderizada).
- **Arquivo `giefs_ferias.py` → `giefs_terco_ferias.py`**: Renomeado, classe `CalculadoraGIEFSFerias` → `CalculadoraGIEFSTercoFerias` (arquivo + `factory.py` + `__init__.py`).
- **Revisão verbas de 13º**: Usuário revisou 13º Salário, GIEFS 13º, Piso 13º e GRS 13º — **validadas** (fórmulas corretas conforme área).
- **Competência das verbas de 13º**: todas as verbas de 13º (13º Salário, GIEFS 13º, Piso 13º, GRS 13º e INSS sobre 13º) usam competência **somente por ano** em `_render_competencia`.
- **Refactor render/defaults**: a decisão de `opcoes` e valor/índice default de `ano_referencia` e `grs_risco` foi movida para o bloco de defaults; o bloco de render passou a só renderizar (padrão do `carga_horaria_mensal`).

---

## 3. Novas calculadoras implementadas

### 3.1 ✅ INSS sobre 13º Salário

**Arquivo:** `calculadoras/inss_decimo_terceiro.py` — classe `CalculadoraINSSDecimoTerceiro`

**Fórmula:** `INSS s/ 13º = (13º + GIEFS 13º) × Alíquota − Dedução (tabela progressiva)`

**Campos:** `valor_13_salario` (moeda, busca no histórico), `giefs_13_salario` (moeda, busca no histórico), `ano_referencia` (selectbox 2024-2026)

**Detalhes:**
- Reaproveita `ProvedorDadosFhemig.obter_tabela_inss(ano)` — mesma tabela progressiva do INSS Mensal
- Base é a **soma** do 13º Salário com a GIEFS do 13º
- Registrada como `"INSS sobre 13º Salário"` (código 7708, Desconto)

### 3.2 ✅ GIEFS — Dias

**Arquivo:** `calculadoras/giefs_dias.py` — classe `CalculadoraGIEFSDias`

**Fórmula:** `Valor GIEFS ÷ 30 × Dias`

**Campos:** `valor_giefs` (moeda, default 0.0 — informado manualmente), `dias_trabalhados` (reaproveitado, 1-30)

**Detalhes:**
- Registrada como `"GIEFS — Dias"` (código 2417, Vantagem)

### 3.3 ✅ GIEFS — Meses

**Arquivo:** `calculadoras/giefs_meses.py` — classe `CalculadoraGIEFSMeses`

**Fórmula:** `Valor GIEFS ÷ 6 × Parcelas`

**Campos:** `valor_giefs` (moeda, default 0.0 — informado manualmente), `numero_parcelas` (novo, 1-12)

**Detalhes:**
- Registrada como `"GIEFS — Meses"` (código 2417, Vantagem)

### 3.4 ✅ GIEFS — 1/3 de Férias

**Arquivo:** `calculadoras/giefs_terco_ferias.py` — classe `CalculadoraGIEFSTercoFerias`

**Fórmula:** `Valor GIEFS ÷ 3`

**Campos:** `valor_giefs` (moeda, default 0.0)

**Detalhes:**
- Registrada como `"GIEFS — 1/3 de Férias"` (código 3242, Vantagem)

### 3.5 ✅ GRS — Meses

**Arquivo:** `calculadoras/grs_meses.py` — classe `CalculadoraGRSMeses`

**Fórmula:** `GRS × Meses`

**Campos:** `grs_risco` (select), `numero_meses` (1-12)

**Detalhes:**
- Reaproveita `ProvedorDadosFhemig.obter_valor_grs()`
- Registrada como `"GRS — Meses"` (código 2420, Vantagem)

### 3.6 ✅ GRS — Desconto de Horas

**Arquivo:** `calculadoras/grs_desconto_horas.py` — classe `CalculadoraGRSDescontoHoras`

**Fórmula:** `GRS ÷ CH × Horas de Falta`

**Campos:** `grs_risco` (select), `carga_horaria_mensal` (selectbox 120-264), `faltas_horas` (inteiro)

**Detalhes:**
- Reaproveita `ProvedorDadosFhemig.obter_valor_grs()`
- Possui proteção contra divisão por zero (CH = 0 → fallback 1)
- Campo `faltas_horas` (semântica correta para desconto por faltas)
- Registrada como `"GRS — Desconto de Horas"` (código 7820, Desconto)

### 3.7 ✅ 1/3 de Férias

**Arquivo:** `calculadoras/ferias_terco.py` — classe `CalculadoraTercoFerias`

**Fórmula:** `(Venc + Ad.Desemp + Ab.Emerg + Ad.Noturno + GRS) ÷ 3`

**Campos:** `vencimento_basico` (do cabeçalho), `ad_desempenho` (default 0), `abono_emergencia` (default 0), `adicional_noturno` (busca no histórico), `grs_risco` (select)

**Detalhes:**
- Reaproveita `ProvedorDadosFhemig.obter_valor_grs()`
- Registrada como `"1/3 de Férias"` (código 2431, Vantagem)

### 3.8 ✅ Férias Indenizadas

**Arquivo:** `calculadoras/ferias_indenizadas.py` — classe `CalculadoraFeriasIndenizadas`

**Fórmula:** `(Venc. Básico + Ab. Emergência + GRS + Ad. Noturno) ÷ 30 × Nº de Dias`

**Campos:** `vencimento_basico` (do cabeçalho), `abono_emergencia` (moeda), `grs_risco` (select), `adicional_noturno` (busca no histórico), `dias_ferias_indenizadas` (1-30, default 30)

**Detalhes:**
- Reaproveita `ProvedorDadosFhemig.obter_valor_grs()`
- **GIEFS NÃO entra** na regra de cálculo (confirmado)
- Registrada como `"Férias Indenizadas"` (código 2432, Vantagem)

### 3.9 ✅ Faltas — Horas

**Arquivo:** `calculadoras/faltas_horas.py` — classe `CalculadoraFaltasHoras`

**Fórmula:** `(Venc + Ad. Desempenho + Ab. Emergência + GRS + Piso Enf.) ÷ CH × Horas de Falta`

**Campos:** `vencimento_basico` (do cabeçalho), `ad_desempenho` (moeda), `abono_emergencia` (moeda), `grs_risco` (select), `valor_piso` (moeda), `carga_horaria_mensal` (selectbox 120-264), `faltas_horas` (inteiro)

**Detalhes:**
- Reaproveita `ProvedorDadosFhemig.obter_valor_grs()`
- Inclui **Piso Enfermagem** na base (default 0.0, editável)
- Registrada como `"Faltas — Horas"` (código 7810, Desconto)

### 3.10 ✅ Faltas — Dias

**Arquivo:** `calculadoras/faltas_dias.py` — classe `CalculadoraFaltasDias`

**Fórmula:** `(Venc + Ad. Desempenho + Ab. Emergência + GRS + Piso Enf.) ÷ 30 × Dias de Falta`

**Campos:** `vencimento_basico` (do cabeçalho), `ad_desempenho` (moeda), `abono_emergencia` (moeda), `grs_risco` (select), `valor_piso` (moeda), `faltas_dias` (1-30)

**Detalhes:**
- Reaproveita `ProvedorDadosFhemig.obter_valor_grs()`
- Inclui **Piso Enfermagem** na base (default 0.0, editável)
- Divisor é **30** (dias)
- Registrada como `"Faltas — Dias"` (código 7811, Desconto)

### 3.11 ✅ Ajuda de Custo Mensal

**Arquivo:** `calculadoras/ajuda_custo.py` — classe `CalculadoraAjudaCusto`

**Fórmula:** `Valor Diário × Dias Trabalhados`

**Campos:** `ajuda_custo_diario` (moeda, 0-75), `dias_trabalhados` (1-30)

**Detalhes:**
- Registrada como `"Ajuda de Custo Mensal"` (código 2070, Vantagem)

### 3.12 ✅ Desconto de Ajuda de Custo

**Arquivo:** `calculadoras/ajuda_custo_desconto.py` — classe `CalculadoraDescontoAjudaCusto`

**Fórmula:** `Valor da Ajuda de Custo × 4%`

**Campos:** `valor_ajuda_custo` (moeda, busca no histórico — última "Ajuda de Custo Mensal")

**Detalhes:**
- Registrada como `"Desconto de Ajuda de Custo"` (código 9018, Desconto)
- Campo `valor_ajuda_custo` pré-preenchido com a última "Ajuda de Custo Mensal" do histórico

### 3.13 ✅ Aumento Salarial (multi-alíquotas)

**Arquivo:** `calculadoras/aumento_salarial.py` — classe `CalculadoraAumentoSalarial`

**Fórmula:** `Venc. Básico × alíquota do reajuste`

**Campos:** `ano_referencia` (selectbox 2024/2026), `vencimento_basico` (do cabeçalho)

**Detalhes:**
- Alíquotas vêm de `tabela_reajustes` no JSON (2024: 4,62%, 2026: 5,4%)
- No histórico, o nome vira "Aumento Salarial (2024)" / "Aumento Salarial (2026)"
- Registrada como `"Aumento Salarial"` (código ----, Vantagem)
- **Pendência:** cálculo combinado "2024 + 2026" (composto) aguardando confirmação da área

### 3.14 ✅ GRS — 13º Salário

**Arquivo:** `calculadoras/grs_13.py` — classe `CalculadoraGRS13`

**Fórmula:** `Valor GRS ÷ 12 × Nº de Meses` (confirmado: 151,99 ÷ 12 × 6 = 75,99)

**Campos:** `grs_risco` (selectbox, 2 opções — sem "Não faz jus"), `numero_meses` (1-12)

**Detalhes:**
- Usa `ProvedorDadosFhemig.obter_valor_grs(grs_risco)` (parser centralizado)
- Registrada como `"GRS — 13º Salário"` (código 3171, Vantagem) em `data/tabelas.json`
- Registrada no `factory.py` como `"GRS — 13º Salário"`
- **Competência** exibe apenas **ano** (não mês/ano) — tratada em `_render_competencia` junto com "13º Salário"
- Incluída na condição que exibe apenas 2 opções no selectbox GRS (Risco Médio e Risco Alto)

### 3.15 ✅ Desconto de IPSEMG (3,2%)

**Arquivo:** `calculadoras/ipsemg.py` — classe `CalculadoraIPSEMG`

**Fórmula:** `(Venc. Básico + Grat. Fim Semana + Ab. Emergência + GIEFS + Ad. Noturno + GRS + Ad. Desempenho + 13º) × 3,2%`

**Campos:** `vencimento_basico` (cabeçalho), `grat_final_semana` (histórico), `abono_emergencia` (default 0), `valor_giefs` (manual), `adicional_noturno` (histórico), `grs_risco` (select), `ad_desempenho` (default 0), `valor_13_salario` (histórico)

**Detalhes:**
- Base montada pela soma dos componentes; aplica alíquota fixa de 3,2%
- **GIEFS e GRS** ficam com tratamento padrão (manual/select), **sem pré-preenchimento**; os demais campos vêm pré-preenchidos de cabeçalho/histórico
- Registrada como `"Desconto de IPSEMG (3,2%)"` (código 7700, Desconto)
- Exemplo confirmado: 20,55 × 0,032 = 0,66

---

## 4. Pendências (a fazer)

### 4.1 ✅ Desconto de IPSEMG (3,2%) — implementado

| Verba | Código | Tipo | Fórmula | Arquivo |
|---|---|---|---|---|
| Desconto de IPSEMG (3,2%) | 7700 | Desconto | (base de incidência) × 3,2% | `calculadoras/ipsemg.py` |

### 4.2 Exportação PDF

- `utils/exportador_pdf.py` está **vazio**
- A função `gerar_pdf()` completa existe no `app.py` (linhas 141-273)
- Precisa ser extraída para o módulo e integrada à UI modular

### 4.3 Remover duplicação de dados

- `app.py` tem `TABELA_CARGOS`, `TABELA_INSS`, `VERBAS_META` duplicados
- Versão modular usa `data/tabelas.json`
- Quando `app.py` for descontinuado, remover as duplicatas

### 4.4 ✅ Concluído — Migração dos parsers GRS

Todos os `_parser_nivel_grs` locais foram eliminados; todas as calculadoras usam `ProvedorDadosFhemig.obter_valor_grs(grs_risco)` diretamente (ver 10.2). Confirmado por busca: **nenhuma ocorrência restante**.

### 4.5 ✅ Resolvido — renomeação Desconto de Ajuda de Custo

- Arquivo `ajuda_custo_desconto.py` em uso (`calculadora_modelo.py` não existe mais)
- Renomeações e ajustes já registrados nos commits anteriores

---

## 5. Observações sobre regras de negócio

- **Gratificação de Final de Semana**: fator de cálculo é **0,5** (confirmado como correto)
- **Condição obsoleta no form_servidor.py**: já corrigida — a condição `!= "- Selecione -"` foi removida junto com a opção obsoleta
- **INSS sobre 13º**: a base de cálculo é a **soma** do 13º Salário com a GIEFS do 13º (confirmado com exemplo: 1010,95 + 64,04 = 1074,99)
- **GIEFS 13º**: campo `valor_giefs`, reutiliza `numero_meses` existente
- **Piso Enfermagem 13º**: novo campo `valor_piso`, reutiliza `numero_meses` existente
- **GIEFS — Dias, GIEFS — Meses, GIEFS — 1/3 de Férias**: usam o mesmo campo `valor_giefs` (informado manualmente pelo usuário)
- **GIEFS — 13º**: usa `valor_giefs` + `numero_meses`
- **Campo `numero_parcelas`**: removido — a GIEFS — Meses foi simplificada para **campo único de valor** (ver 2.4/10.4)
- **INSS sobre 13º**: `valor_13_salario` e `giefs_13_salario` são preenchidos automaticamente via busca no histórico
- **Faltas — Dias e Faltas — Horas**: base inclui **Piso Enfermagem** (CPE — Lei 14434/22). Faltas — Dias divide por 30; Faltas — Horas divide pela carga horária.
- **Férias Indenizadas**: **GIEFS NÃO entra** na base de cálculo (confirmado)
- **GRS — Desconto de Horas**: usa campo `faltas_horas` (horas de falta), não `horas_realizadas`
- **Desconto de Ajuda de Custo**: campo `valor_ajuda_custo` pré-preenchido do histórico (última "Ajuda de Custo Mensal")
- **Arquivo `terco_ferias.py` → `ferias_terco.py`**: renomeado (classe `CalculadoraTercoFerias` mantida)

---

## 6. Dúvidas em aberto (ver `dúvidas.md`)

- Abono Emergência é valor fixo (R$ 150)?
- **INSS Mensal**: a base atualmente usa **apenas o `vencimento_basico`**. O legado (`app.py`) tinha um campo único "Base de cálculo (R$)". Confirmar se a base deve incluir outras rubricas (Grat. Fim Semana, Ad. Noturno, GRS, etc.) ou se mantém só o vencimento básico.
- ~~GIEFS 13º: o valor a sofrer incidência é o próprio valor da GIEFS?~~ ✅ Esclarecido — a base do INSS sobre 13º é a soma (13º + GIEFS 13º)
- Aumento Salarial: cálculo combinado "2024 + 2026" será **composto** (`base × 1,0462 × 1,054`)? Aguardando confirmação da área.

---

## 7. Como rodar

```bash
# Versão modular (nova)
streamlit run main.py

# Versão legada (monolítica)
streamlit run app.py
```

Dependências: `streamlit`, `reportlab`, `pandas` (ver `requirements.txt`)

---

## 8. Histórico de commits (resumo)

Os commits mais recentes mostram a evolução da refatoração:
- `d4c6674` — Refatoração inicial para arquitetura modular
- `7a2e329` a `ee184f0` — Implementação incremental das calculadoras, formulário, histórico, competência, observação
- `3a48aa9` — "feat: implementa GRS dinâmico, CH Mensal como selectbox e contexto.md"
- `ee184f0` — "feat: implementa competencia por ano para cálculo de 13o e campo de observação"
- `9bc2c2d` — "feat: implementa calculadoras de GRS Dias e 13º Salário"
- `f955347` — "feat: implementa aumento salarial com diferentes alíquotas e revisa cálculo de faltas de dias e horas"
- Implementações recentes: Férias Indenizadas, Faltas — Horas, Faltas — Dias, Ajuda de Custo Mensal, Desconto de Ajuda de Custo, Aumento Salarial (multi-alíquotas)
- **Trabalho da sessão atual (ainda NÃO commitado):** unificação `ano_reajuste` → `ano_referencia`; competência por ano nas verbas de 13º; refactor render/defaults (`ano_referencia` e `grs_risco`); implementação do **Desconto de IPSEMG**; validação do INSS sobre 13º; `data/tabelas.json` reorganizado e `duvidas.md` renomeado (acento removido).

---

## 9. Padrão para criar novas calculadoras

1. Criar classe em `calculadoras/` estendendo `CalculadoraVerba`
2. Implementar `descricao_formula`, `campos_necessarios`, `calcular()`
3. Importar em `calculadoras/__init__.py`
4. Registrar em `calculadoras/factory.py`
5. Adicionar campos em `ui/config.py` (se forem novos)
6. Adicionar defaults e renderização em `ui/selecao_verba.py`

---

## 10. Plano de desenvolvimento — próxima sessão

> **Data:** 07/03/2026
> **Objetivo:** Revisar o cálculo do INSS sobre o 13º Salário e commitar pendências.

### 10.1 ✅ Concluído em 05/03 — Nova verba GRS — 13º Salário

- `calculadoras/grs_13.py` criada
- Registrada em `factory.py`, `__init__.py` e `data/tabelas.json` (código 3171)
- Competência exibe apenas ano

### 10.2 ✅ Concluído em 05/03 — Migração dos parsers GRS

- `grs_desconto_horas.py`, `ferias_indenizadas.py`, `ferias_terco.py`: `_parser_nivel_grs` local removido, agora usam `ProvedorDadosFhemig.obter_valor_grs(grs_risco)` diretamente
- ✅ Todos os `_parser_nivel_grs` foram eliminados do projeto

### 10.3 ✅ Concluído em 05/03 — Renomeações de campos

- `valor_base` → `valor_giefs` (GIEFS — Dias e GIEFS — Meses); busca no histórico removida
- `valor_base_desconto` → `valor_ajuda_custo` (Desconto de Ajuda de Custo) + pré-preenchimento do histórico

### 10.4 ✅ Concluído em 06/03 — Revisão verbas de GIEFS

- **GIEFS — Meses**: simplificada para **campo único de valor** (fórmula `Valor GIEFS ÷ 6 × Parcelas` → `Valor total da GIEFS para o período`)
- **Correção de renderização**: verba renomeada `"GIEFS — Meses (parcelas)"` → `"GIEFS — Meses"` no JSON
- **Arquivo `giefs_ferias.py` → `giefs_terco_ferias.py`**: renomeado, classe `CalculadoraGIEFSTercoFerias`

### 10.5 ✅ Concluído em 06/03 — Revisão das verbas de 13º

Usuário revisou as fórmulas de:
- **13º Salário** ✓
- **GIEFS — 13º Salário** ✓
- **Piso Enfermagem — 13º Salário** ✓
- **GRS — 13º Salário** ✓

Todas **validadas** conforme a área competente.

### 10.6 ✅ Concluído — INSS sobre o 13º Salário (validado)

**Fórmula confirmada:** `(13º + GIEFS 13º) × Alíquota − Dedução (tabela progressiva)`

**Decisão:** a base é **somente** `13º + GIEFS 13º`. **GRS 13º e Piso 13º NÃO entram** na base (conforme spec da área).

**Campos:** `valor_13_salario` e `giefs_13_salario` (pré-preenchidos via histórico), `ano_referencia` (selectbox 2024-2026).

**Exemplo validado:** `1010,95 + 64,04 = 1074,99` → faixa 7,5% → **80,62** (tabela progressiva; `ano_referencia: int`, convertido com `str()` na borda).

### 10.7 🟡 Aumento Salarial — cálculo combinado "2024 + 2026"

- Aguardando confirmação da área se será **composto** (`base × 1,0462 × 1,054`)
- Se confirmado, adicionar opção "2024 + 2026" no selectbox e lógica de múltiplas alíquotas

### 10.8 ✅ Concluído — Desconto de IPSEMG (3,2%)

| Verba | Código | Tipo | Fórmula |
|---|---|---|---|
| Desconto de IPSEMG (3,2%) | 7700 | Desconto | (Venc + Grat. Fim Sem. + Ab. Emerg. + GIEFS + Ad. Noturno + GRS + Ad. Desemp. + 13º) × 3,2% |

Base de incidência montada a partir dos campos dos componentes (com pré-preenchimento do histórico/cabeçalho para os campos exceto GIEFS e GRS, que ficam com default/manual). Exemplo confirmado: 20,55 × 0,032 = 0,66.

---

## 11. Próximos passos (pendências em aberto)

> Consolidação do que segue em aberto, com referência às seções detalhadas. Itens em `🟡` dependem de confirmação da área.

### 11.1 Desenvolvimento

1. **Exportação PDF (ver 4.2)** — Implementar `utils/exportador_pdf.py`, extraindo o `gerar_pdf()` do `app.py` (linhas 141-273) e integrar à UI modular (exportar resultado/histórico).
2. **Remover duplicação de dados (ver 4.3)** — Quando `app.py` for descontinuado, remover `TABELA_CARGOS`, `TABELA_INSS`, `VERBAS_META` duplicados e passar a usar exclusivamente `data/tabelas.json`.
3. **Aumento Salarial combinado (ver 10.7 🟡)** — Aguardando confirmação da área se o cálculo "2024 + 2026" será **composto** (`base × 1,0462 × 1,054`). Se confirmado, adicionar opção "2024 + 2026" no selectbox de `ano_referencia` e a lógica de múltiplas alíquotas.

### 11.2 Decisões de regra de negócio em aberto (ver `duvidas.md` e seção 6)

- **Abono Emergência**: é valor fixo (R$ 150)?
- **INSS Mensal**: base atualmente usa **apenas o `vencimento_basico`**; definir se deve usar a base completa de remuneração (como no legado)
- **Piso Enfermagem**: o valor é fixo? faz sentido puxar o valor automaticamente (carreira PENF) ou manter campo aberto?
- **Desconto de Ajuda de Custo**: confirmar se é do **"Custeio Alimentação"**
- **Faltas/atrasos**: o atraso (horas/dias) afeta o campo GRS considerado na fórmula?
- **GIEFS — Meses**: confirmar a fórmula (não localizada na planilha)

### 11.3 Encerramento da sessão

- **Commit do trabalho da sessão atual** (ainda não commitado — ver seção 8)
- **Revisão final** da versão modular em relação ao `app.py` legado antes de descontinuá-lo
