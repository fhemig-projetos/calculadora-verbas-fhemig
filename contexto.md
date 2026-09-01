# Contexto do Projeto — Calculadora de Verbas FHEMIG

> **Propósito:** Refatoração do `app.py` (monolítico) para arquitetura modular com pacotes e OOP.
> **Stack:** Python + Streamlit + ReportLab (PDF) + Pandas
> **Entrypoint atual:** `app.py` (renomeado de `main.py` no commit `f4bf15f`, para viabilizar deploy de múltiplos apps no mesmo repo no Streamlit Cloud — ver pendência 4.13). A pasta `old/` (arquivo legado monolítico) não existe mais no repositório.

---

## 1. Arquitetura do Projeto

```
calculadora-verbas-fhemig/
├── app.py                     # Entrypoint da versão modular (renomeado de main.py — ver 4.13)
├── app_hem.py                 # App de teste p/ deploy de múltiplos apps no mesmo repo (avaliar remoção — ver 15.4)
├── contexto.md                # Este arquivo
├── dúvidas.md                 # Dúvidas em aberto sobre regras de negócio
├── requirements.txt           # streamlit, reportlab, pandas, supabase
│
├── assets/                    # Identidade visual
│   ├── icone.png               # Favicon (page_icon em app.py)
│   ├── LogoFhemig.png           # Logo institucional no cabeçalho (ui/cabecalho.py)
│   └── cabecalho_pdf.png       # Logo usado no PDF exportado (utils/exportador_pdf.py)
│
├── scripts/                   # Scripts utilitários (fora do pacote da aplicação)
│   └── populate_servidores.py # Importa data/dados_funcionais_calculadora_verbas.csv p/ tabela `servidores` no Supabase (ver 15.1)
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
│   ├── ipsemg.py              # ✅ Implementada
│   └── licenca_maternidade.py # ✅ Implementada (17/08)
│
├── data/                      # Dados externos
│   ├── __init__.py
│   ├── provedor_dados.py      # ProvedorDadosFhemig (cache + acesso JSON)
│   ├── provedor_servidores.py # ProvedorServidoresSupabase (busca servidor por MASP+Admissão — ver 15.2)
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
    └── exportador_pdf.py      # ✅ GeradorPDF — PDF do histórico (layout FHEMIG)
```

---

## 2. O que já foi implementado (versão modular)

### 2.1 Calculadoras (24 de 24 — completa)

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
| Licença Maternidade | `calculadoras/licenca_maternidade.py` | ✅ |

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
- Botões: "Remover último", "Limpar lista", "📄 Gerar PDF"

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
- **Persistência de campos "genéricos" (17/08)**: no `else` final do bloco de defaults (`horas_realizadas`, `abono_emergencia`, `valor_giefs`, `valor_piso`, etc.), o fallback de `persistidos.get(campo, ...)` passou a checar `CONFIG_CAMPOS[campo]["tipo"]`: se for `"moeda"`, o default é `0.0` (float); senão, `0` (int) — como já era.
- **Cabeçalho volta a "irradiar" para vencimento/CH/valor_base_aumento (17/08)**: `persistidos[campo] = valores[campo]` passou a gravar **todos** os campos (removida a exclusão anterior de `vencimento_basico`, `carga_horaria_mensal`, `valor_base_aumento`). Para não deixar esses 3 campos "grudados" no primeiro valor digitado e ignorando trocas de servidor no cabeçalho, foi adicionado `st.session_state["ultima_referencia_cabecalho"]`: ao detectar mudança em `(vencimento_basico, ch_mensal)` do `dados_servidor`, `_render_calculadora` limpa esses 3 campos de `persistidos` e incrementa `verba_nonce` (força o Streamlit a recriar a `key` dos widgets). Resultado: o cabeçalho sempre prevalece quando muda, mas o usuário pode editar livremente os 3 campos até a próxima troca de servidor.
- **Correção de 2 bugs de comparação em `ui/selecao_verba.py` (17/08)**:
  - `elif campo == ("dias_trabalhados", "dias_ferias_indenizadas", "faltas_dias"):` (string comparada com tupla, sempre `False`) → corrigido para `campo in (...)`. Antes do fix, esses 3 campos caíam no `else` genérico sem `min_value=1, max_value=30`, permitindo valores inválidos (0, negativos, >30).
  - `desabilitado = campo in ("ad_desempenho")` (sem vírgula = string, testava substring) → corrigido para `campo in ("ad_desempenho",)` (tupla de fato).
- **Licença Maternidade (17/08)**: nova verba implementada — ver seção 3.16.

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

### 3.16 ✅ Licença Maternidade (17/08)

**Arquivo:** `calculadoras/licenca_maternidade.py` — classe `CalculadoraLicencaMaternidade`

**Fórmula:** `Venc. Básico + Valor GIEFS + Ab. Emergência + GRS` (confirmado: 4232,07 + 371,91 + 180,00 + 0,00 = 4783,98)

**Campos:** `vencimento_basico` (cabeçalho), `valor_giefs` (manual), `abono_emergencia` (manual), `grs_risco` (select, 3 opções)

**Detalhes:**
- Verba identificada na planilha da área e implementada nesta sessão (antes ausente do app)
- Reaproveita `ProvedorDadosFhemig.obter_valor_grs()`
- Nenhum campo novo em `CONFIG_CAMPOS` — os 4 campos usados já existiam
- Registrada como `"Licença Maternidade"` (código 1200, Vantagem) em `data/tabelas.json`, `factory.py` e `__init__.py`
- Competência segue o padrão mês/ano (não é verba de 13º)

---

## 4. Pendências (a fazer)

### 4.1 ✅ Desconto de IPSEMG (3,2%) — implementado

| Verba | Código | Tipo | Fórmula | Arquivo |
|---|---|---|---|---|
| Desconto de IPSEMG (3,2%) | 7700 | Desconto | (base de incidência) × 3,2% | `calculadoras/ipsemg.py` |

### 4.2 ✅ Exportação PDF — implementada (14/08)

- `utils/exportador_pdf.py` com a classe **`GeradorPDF`** (layout do `PDFGenerator` de outra aplicação).
- Estrutura: `BaseDocTemplate` + templates de página (1ª com logo, demais sem), cor `#108da5`, seções "Dados do Servidor", "Verbas Calculadas" (com totais), "Memória de Cálculo", "Observações" e rodapé.
- Integrado à UI: botão **"📄 Gerar PDF"** em `_render_historico` (via `st.download_button`).
- Logo institucional: `assets/cabecalho_pdf.png` (desenhado só se o arquivo existir).
- Detalhes no plano de sessão (seção 12.2).

### 4.3 ✅ Resolvido (18/08) — Remover duplicação de dados

- `app.py` (que tinha `TABELA_CARGOS`, `TABELA_INSS`, `VERBAS_META` duplicados) foi **removido da raiz**, arquivado em `old/app_old.py`.
- Versão modular usa exclusivamente `data/tabelas.json` — sem duplicidade restante.
- `main.py` agora é o único entrypoint da aplicação.

### 4.4 ✅ Concluído — Migração dos parsers GRS

Todos os `_parser_nivel_grs` locais foram eliminados; todas as calculadoras usam `ProvedorDadosFhemig.obter_valor_grs(grs_risco)` diretamente (ver 10.2). Confirmado por busca: **nenhuma ocorrência restante**.

### 4.5 ✅ Resolvido — renomeação Desconto de Ajuda de Custo

- Arquivo `ajuda_custo_desconto.py` em uso (`calculadora_modelo.py` não existe mais)
- Renomeações e ajustes já registrados nos commits anteriores

### 4.6 🟡 Pendente — expandir base do INSS sobre 13º Salário

- Hoje (`calculadoras/inss_decimo_terceiro.py`) a base é só `valor_13_salario + giefs_13_salario`.
- Pelo mesmo raciocínio aplicado ao INSS Mensal nesta sessão (ver seção 14): **Piso Enfermagem — 13º Salário** e **GRS — 13º Salário** também deveriam entrar na base.
- Ao implementar, avaliar se vale a mesma abordagem residual (soma automática das 4 verbas de 13º do histórico, com um campo tipo `valor_outras_vantagens_13`) em vez de campos individuais — replicando o padrão criado em 14.

### 4.7 🟡 Parcialmente resolvido (19/08) — substituir códigos das verbas pelos códigos corretos

- Vários registros em `data/tabelas.json` têm código placeholder ou a confirmar (ex.: "Aumento Salarial" com código `----`; GIEFS 13º e GRS 13º compartilhando o mesmo código `3171`, provavelmente por engano/placeholder).
- Levantar com a área a tabela oficial de códigos de cada verba e atualizar `data/tabelas.json` (campo `codigo` de cada entrada em `verbas`).

**Aplicado em 19/08**, a partir do documento "Levantamento de Dados — Cálculo de Rescisão" (RH/CCPT), que traz os códigos oficiais de rubrica separados por **Contrato** vs **Efetivo**. Como a calculadora é só para **contratados**, foi usada sempre a variante Contrato. Confirmado pelo usuário que os códigos de 3 dígitos do documento são os corretos (não truncados) — **já atualizado em `data/tabelas.json`**:

| Verba (`tabelas.json`) | Código anterior | Código atual (Contrato) |
|---|---|---|
| Gratificação de Final de Semana | `2416` | ✅ `416` |
| Adicional Noturno | `2411` | ✅ `773` |
| 13º Salário | `2491` | ✅ `491` |
| GIEFS — Dias | `2417` | ✅ `417` |
| GIEFS — Meses | `2417` | ✅ `417` |
| GIEFS — 13º Salário | `3171` | ✅ `417` |
| GRS — Dias | `2420` | ✅ `774` |
| GRS — Meses | `2420` | ✅ `774` |
| GRS — 13º Salário | `3171` (bug — copiado do GIEFS) | ✅ `774` |
| 1/3 de Férias | `2431` | ✅ `492` |

Observações do levantamento:
- O documento **não distingue código por periodicidade** para GIEFS e GRS — o mesmo código (`417` e `774`, respectivamente) vale pra Dias, Meses e 13º. Isso confirma que `GRS — 13º Salário` estava com código errado (herdado do GIEFS por engano).
- **Sem código encontrado no documento** para: Hora Extra, GIEFS — 1/3 de Férias, Férias Indenizadas, Faltas — Horas/Dias, GRS — Desconto de Horas, INSS Mensal, INSS sobre 13º, IPSEMG, Ajuda de Custo (Mensal/Desconto), Aumento Salarial, Licença Maternidade, Piso Enfermagem — 13º Salário. O documento só lista os códigos dos **componentes da base de cálculo**, não o código de pagamento dessas verbas — continuam pendentes de confirmação com a área.
- **Achado à parte (não tratado nesta pendência):** o documento indica que o **Adicional de Desempenho (ADE, código 537) é "SOMENTE EFETIVO"**. Como a calculadora é só para contratados, isso pode significar que o campo `ad_desempenho` (usado hoje em `ferias_terco.py`, `faltas_horas.py`, `faltas_dias.py`, `ipsemg.py`) não deveria compor essas fórmulas. Fica registrado como **nova dúvida em aberto** (ver seção 6) — decidido explicitamente **não tratar** nesta pendência, escopo restrito à troca de códigos.

### 4.8 🟡 Pendente — preenchimento automático dos dados do servidor pelo MASP

- Já registrado como melhoria na seção 13.2, item 4 — reforçado como pendência aqui.
- Hoje `ui/form_servidor.py` não faz nenhuma busca a partir do MASP digitado; usuário preenche tudo manualmente.
- Avaliar fonte de dados disponível (nova tabela em `tabelas.json`? integração externa?) antes de implementar.

### 4.9 ✅ Resolvido (19/08) — Data Fim Efetiva não aparece na tabela "Dados do Servidor" do PDF

- `utils/exportador_pdf.py` (`_adicionar_dados_servidor`): adicionada a linha `linha("Data Fim Efetiva", data_fim_efetiva)`, logo após "Data de Admissão", formatada do mesmo jeito (`%d/%m/%Y`, ou "—" se vazia).

### 4.10 ✅ Resolvido (19/08) — ampliar intervalo de anos em Data de Admissão e Data Fim Efetiva

- `ui/form_servidor.py`: os dois `st.date_input` (Data de Admissão e Data Fim Efetiva) passaram a receber `min_value=date(1950, 1, 1)` e `max_value=date.today()` explícitos.
- Antes, sem esses parâmetros, o Streamlit usava um intervalo padrão de ±10 anos a partir de hoje (já que `value` começa como `None`), limitando a seleção aos últimos ~10 anos e, de quebra, permitindo datas futuras (que não fazem sentido pra admissão/fim efetiva) — ambos os problemas corrigidos.

### 4.11 🟡 Pendente — confirmar unicidade de `masp_admissao` na extração de dados

- Ao popular a tabela `servidores` (`scripts/populate_servidores.py`) a partir de `data/dados_funcionais_calculadora_verbas.csv`, o `upsert` com `on_conflict="masp_admissao"` falhava com o erro do Postgres `ON CONFLICT DO UPDATE command cannot affect row a second time` — havia **45 valores duplicados** de `Masp/Admissão` no CSV (de 2904 linhas, só 2859 valores únicos).
- Investigação (24/08): **42 grupos** eram linhas 100% idênticas repetidas (ruído de exportação). **3 grupos** tinham o mesmo `masp_admissao`, mas divergiam só na `Carga Horária Pagamento` (ex.: 30h e 40h) — podendo indicar dois vínculos/cargos reais da mesma pessoa, e não necessariamente ruído.
- **Decisão temporária do usuário:** por ora, partir do pressuposto de que `masp/admissão` é suficiente como chave única para os dados e tratar todos os 45 casos (incluindo os 3 com carga horária diferente) como ruído — resolvidos deduplicando no script antes do upsert.
- **Fica como pendência:** checar com a área de extração de dados se `masp_admissao` é de fato garantidamente único por vínculo, ou se os 3 casos de carga horária diferente representam acúmulo de cargo real (o que exigiria incluir mais alguma coluna, ex. `carga_horaria`, na chave de conflito/unicidade).

### 4.12 🟡 Pendente — ampliar opções de Carga Horária Semanal/Mensal + pendência de confirmação

- **Achado:** ao implementar o pré-preenchimento via Supabase (ver seção 15), constatou-se que a coluna `carga_horaria` da tabela `servidores` tem 5 valores distintos na base real (2861 registros): **12h (3,7%), 24h (6,0%), 30h (14,7%), 40h (60,4%), 60h (15,2%)** — ou seja, ~25% dos servidores têm carga horária fora do `selectbox` de "Carga Horária Semanal", que só aceitava `[20, 30, 40, 44]` (20h e 44h, por sua vez, **não aparecem nenhuma vez** na base real).
- Esse valor vem da coluna `Carga Horária Pagamento` do CSV original (não necessariamente "carga horária semanal" no sentido estrito — pode representar regime de plantão de 12h, acúmulo de cargos somando 60h, etc.).
- **Bug relacionado encontrado:** quando o valor de CH não batia com as opções fixas, tanto o `selectbox` de Carga Horária Semanal (`ui/form_servidor.py`) quanto o de Carga Horária Mensal (`ui/selecao_verba.py`) caíam **silenciosamente** para um valor default (40h / 120h respectivamente) — sem qualquer aviso ao usuário, mascarando o valor real do servidor.
- **Resolvido:** opções ampliadas para incluir os 5 valores encontrados na base:
  - `ui/form_servidor.py`: `opcoes_ch_semanal = [12, 20, 24, 30, 40, 44, 60]` (linha ~81); filtro de aceitação do valor vindo do Supabase (linha ~51) ampliado de `(20, 30, 40, 44)` para `(12, 20, 24, 30, 40, 44, 60)`.
  - `ui/selecao_verba.py`: `opcoes_ch = [72, 120, 144, 180, 240, 264, 360]` (CH Mensal = CH Semanal × 6), usado tanto no cálculo do índice default quanto no `selectbox` do campo `carga_horaria_mensal`.
  - Fallback de índice em ambos os selectbox ajustado para apontar para 40h/240h (antes eram índices fixos que, por coincidência, apontavam pros valores errados após a ampliação da lista).
- **🟡 Pendência (decisão do usuário):** avaliar se **20h e 44h devem ser removidas** das opções, já que não há nenhum registro na base real com esses valores — usuário pediu para não excluir agora e primeiro **confirmar com a área de extração de dados se há (ou pode haver no futuro) servidores com 20h ou 44h semanais** que hoje simplesmente não estão nos 2861 registros já importados.
- **Impacto nas calculadoras:** nenhuma mudança de fórmula necessária — `adicional_noturno.py`, `faltas_horas.py`, `gratificacao_final_semana.py`, `grs_desconto_horas.py` e `hora_extra.py` usam `carga_horaria_mensal` apenas como divisor numérico puro (valor-hora = base ÷ CH), então os novos valores (72, 144, 360) funcionam sem alteração de lógica.
- **Achado à parte, não tratado:** `calculadoras/faltas_horas.py` é a única das 5 calculadoras que usa `carga_horaria_mensal` **sem proteção contra divisão por zero** (as outras 4 têm guarda `if carga_horaria_mensal <= 0`). Fica registrado como possível bug a corrigir em sessão futura.
- Confirmar os valores possíveis de carga horária com a taxação.

**Atualização (24/08) — solução dos selectbox substituída por campos livres:** a abordagem acima (ampliar as listas fixas) foi **superada** por uma solução mais simples, decidida na mesma sessão: em vez de listar valores possíveis de CH num `selectbox`, os campos viraram `number_input` livres.
  - `ui/form_servidor.py`: "Carga Horária Semanal" agora é `st.number_input` (`min_value=0, step=1`), sem lista de opções fixa; o pré-preenchimento via Supabase (`ds["ch_semanal"] = int(servidor_encontrado["carga_horaria"])`) passou a aceitar qualquer valor, sem filtro. Isso também corrigiu de quebra um `NameError` (variável `ch_encontrada` referenciada sem estar definida, introduzido numa edição manual entre sessões).
  - `ui/selecao_verba.py`: bloco especial de `carga_horaria_mensal` (antes um `selectbox` com `opcoes_ch`/`indice_default` próprios) foi removido; o campo agora cai naturalmente no `number_input` genérico já usado por `vencimento_basico` — o próprio comentário do código já antecipava esse caminho ("vencimento_basico, ad_desempenho, carga_horaria_mensal, horas_realizadas, etc.").
  - **Efeito:** a pendência de "20h/44h devem sair da lista?" fica **resolvida por construção** — não há mais lista fixa para incluir/excluir valores. A confirmação com a área sobre quais cargas horárias são válidas de fato continua útil como checagem de sanidade dos dados, mas não bloqueia mais a UI.
  - Testado end-to-end com servidor real de 60h/semana (MASP 15434251): CH Semanal exibe 60, CH Mensal (cabeçalho) exibe 360, e ao selecionar a verba "Hora Extra" o campo Carga Horária Mensal já vem pré-preenchido com 360.

### 4.13 🟡 Pendente — configurar secrets do Supabase no deploy do Streamlit Cloud

- O pré-preenchimento via Supabase (ver seção 15) só funciona hoje **localmente**, porque `.streamlit/secrets.toml` (com a seção `[supabase_admin]`) existe apenas na máquina de desenvolvimento — **não foi configurado no app publicado** em [share.streamlit.io](https://share.streamlit.io).
- **Antes de fazer merge/deploy dessa funcionalidade:** adicionar a seção `[supabase_admin]` (com `url` e `key`) nos "Secrets" do app no painel do Streamlit Cloud (Settings → Secrets), senão `ProvedorServidoresSupabase.buscar_servidor` vai lançar exceção em produção — hoje isso é capturado (`try/except` em `data/provedor_servidores.py`, mostra aviso e retorna `None`), mas o pré-preenchimento simplesmente não vai funcionar pra ninguém em produção até essa configuração ser feita.
- **Achado à parte:** o entrypoint do app foi renomeado de `main.py` para `app.py` num commit anterior (`f4bf15f`), aparentemente para viabilizar deploy de múltiplos apps a partir do mesmo repositório (existe também um `app_hem.py` de teste na raiz). O cabeçalho deste `contexto.md` ainda citava `main.py` como entrypoint — **corrigido nesta sessão** (ver topo do arquivo). Vale confirmar se `app_hem.py` ainda é necessário ou se pode ser removido.

### 4.14 🟡 Pendente — confirmar correção do bug de reset de campos do cabeçalho (digitação)

- Usuário relatou (24/08): ao digitar um novo MASP/Nº de Admissão para fazer uma **segunda** busca de servidor (após já ter feito uma primeira busca), o campo às vezes volta pro valor anterior e exige digitar de novo.
- **Causa provável:** `MASP` e `Nº de Admissão` não tinham `key=` explícita — mesma classe de bug já documentada e corrigida antes neste projeto para outros campos (ver seção 12.1: sem `key`, o Streamlit pode "remontar" o widget quando o `value` muda entre execuções, descartando o que o usuário digitou).
- **Corrigido:** adicionada `key="masp"` / `key="admissao"` só nesses dois campos em `ui/form_servidor.py`.
- **Regressão nº 1 (encontrada e corrigida na mesma sessão):** a primeira tentativa de correção também adicionou `key=` fixa em `Nome`, `Cargo`, `Nível`, `Grau` e `Carga Horária Semanal` — o que **quebrou o pré-preenchimento automático** desses campos (a busca no Supabase continuava funcionando e a mensagem "Servidor encontrado" aparecia, mas os campos não eram mais atualizados na tela). Causa: com `key=` explícita, o Streamlit ignora o parâmetro `value=` em toda rodada após a primeira, usando só o valor já guardado sob aquela chave — um espaço de armazenamento **diferente** de `ds["nome"]` etc. (o dicionário `dados_servidor`), então a atualização feita pela busca nunca chegava ao widget.
- **Regressão nº 2 (usuário relatou em seguida):** ao remover a `key=` desses 5 campos pra corrigir a regressão nº 1, o **mesmo bug original de digitação voltou** — mas agora nos campos Cargo/Nível/Grau/CH Semanal (que o usuário também edita manualmente quando o cargo não é encontrado automaticamente). Ou seja: `key=` fixa quebra o pré-preenchimento; nenhuma `key=` traz de volta o bug de digitação. As duas necessidades (aceitar sobrescrita programática da busca **e** permitir edição manual confiável) são incompatíveis com uma única `key=` estática.
- **Solução final:** padrão de **nonce**, já usado em `ui/selecao_verba.py` (`campo_key = f"{nonce}::{campo}"`) — um contador (`st.session_state["servidor_nonce"]`) que só é incrementado quando uma **busca nova encontra um servidor diferente** do último buscado (rastreado via `st.session_state["ultima_busca_servidor"]`, comparando o par `(masp, admissao)`). A `key` de cada campo (`f"{nonce}::nome"`, `f"{nonce}::cargo_classe"`, etc.) só muda quando o nonce muda:
  - Nonce parado (usuário digitando manualmente, sem nova busca): `key` estável → Streamlit confia no widget, digitação não reverte.
  - Nonce incrementado (nova busca encontrou servidor diferente): `key` muda → Streamlit trata como widget novo → aplica o `value=ds[...]` fresco vindo do Supabase, sobrescrevendo qualquer edição manual anterior (comportamento desejado, já que é outro servidor).
- **Campos com nonce:** `nome`, `cargo_classe`, `cargo_nivel`, `cargo_grau`, `ch_semanal`, `dt_admissao` e `dt_fim_efetiva` — todos os campos que são **sobrescritos pela busca E editáveis manualmente**. `masp`/`admissao` ficam com `key` fixa (nunca sobrescritos por código). `Carga Horária Mensal` não recebeu key nenhuma — é `disabled=True` (só leitura, recalculada a cada rodada), então não há risco de reverter uma digitação que nunca acontece.
- **Efeito colateral encontrado e corrigido (mesma sessão):** com `key` estável (nonce parado), o `.upper().strip()` encadeado após `c6.text_input(...)` (Cargo/Grau) e `.strip()` (Nível) passou a normalizar só a **variável Python** (`ds["cargo_classe"]`, usada na busca de cargo e no PDF exportado), sem refletir na **tela** — digitar `"penf  "` (minúsculo, espaços sobrando) continuava mostrando `"penf  "` no campo, porque o widget (chave estável) ignora `value=` depois da primeira renderização; só a variável interna ficava normalizada. Corrigido com o mesmo padrão de `on_change` já usado no projeto para `on_change_masp`/`on_change_moeda` (`utils/ui_callbacks.py`): dois callbacks novos, `on_change_maiusculo_strip` e `on_change_strip` (mais os métodos `FormatadorCampos.maiusculo_strip`/`FormatadorCampos.strip`), conectados via `on_change=..., args=(key,)` nos 3 campos de Cargo — o callback normaliza `st.session_state[key]` **antes** do rerun, então a normalização já aparece na tela na mesma interação. Testado com Playwright: digitar `"penf  "` agora exibe `"PENF"` no campo.
- **2º efeito colateral encontrado e corrigido (mesma sessão):** o Streamlit acusou o warning `"The widget with key ... was created with a default value but also had its value set via the Session State API"` para os 3 campos de Cargo — porque, ao mesmo tempo, o código passava `value=ds["cargo_classe"]` pro widget **e** o callback `on_change` escrevia direto em `st.session_state[key]`; as duas formas de definir o valor do mesmo widget são consideradas conflitantes pelo Streamlit (hoje só warning, mas pode virar erro em versão futura). **Corrigido:** removido o `value=` desses 3 campos — a "semente" inicial do valor passou a ser escrita direto em `st.session_state[f"{nonce_novo}::cargo_classe"]` (e `cargo_nivel`/`cargo_grau`) no próprio bloco de busca, **só quando o nonce é incrementado** (busca nova, não em toda rodada — importante pra não sobrescrever edição manual a cada rerun). `nome`, `dt_admissao`, `dt_fim_efetiva` e `ch_semanal` não têm `on_change`, então não disparam esse warning e continuam com `value=ds[...]` normalmente. Confirmado via log do servidor: warning não aparece mais após a correção.
- **Melhorias adicionais pedidas pelo usuário (mesma sessão):**
  1. **`.upper()`/`.strip()` redundantes removidos:** como o `on_change` já garante que `st.session_state[key]` chega normalizado *antes* do widget renderizar nesta rodada, encadear `.upper().strip()` no retorno de `c6.text_input(...)` (Cargo/Grau) e `.strip()` (Nível) virou trabalho duplicado. Removido dos 3 campos — confirmado (via consulta ao Supabase) que os dados de origem (`cod_carreira`, `grau`) já são uniformemente maiúsculos e sem espaços, então a "semente" inicial (vinda da busca) também não precisa de normalização extra.
  2. **Campos limpos quando a busca não encontra correspondência:** antes, mudar MASP/Admissão para uma combinação sem correspondência **mantinha na tela** os dados do servidor buscado anteriormente (Nome, Cargo, Nível, Grau, CH, datas) — enganoso, pois pareciam pertencer ao MASP/Admissão atual. Corrigido: a mesma lógica de nonce que já preenchia os campos numa busca nova bem-sucedida agora também **limpa** esses campos (`""`/`0`/`None`) quando uma busca nova não encontra nada — usando o mesmo gatilho (`busca_atual != ultima_busca_servidor`), então digitar parcialmente um MASP/Admissão não fica limpando os campos a cada tecla, só quando uma combinação *diferente* da última processada é de fato buscada.
  - Testado (Playwright): busca válida preenche Nome/Cargo/Nível; busca seguinte com combinação inexistente limpa os 3 campos para `''`. Fluxo completo (busca → edição manual → nova busca) e normalização continuam funcionando sem regressão; nenhum warning/erro no log do servidor.
- **Testado (Playwright, 3 passos em sequência):** 1) primeira busca preenche Cargo=PENF/Nível=2 corretamente; 2) edição manual do campo Cargo (digitação char-a-char) persiste como "TOS", sem reverter; 3) segunda busca com servidor diferente (60h, MEDRE) sobrescreve corretamente para Cargo=MEDRE/Nível=1/CH=60. Os três cenários confirmados sem erros de console.
- **Ainda não confirmado em uso real:** o sintoma original relatado pelo usuário (revert ao digitar MASP/Admissão) não foi replicável em teste automatizado (Playwright não recria com fidelidade o timing de foco/digitação humana). A correção de MASP/Admissão (`key="masp"`/`key="admissao"`, estável — não usa nonce, pois esses dois campos nunca são sobrescritos por código) segue de pé, mas pede confirmação do usuário em uso real.
- **Reimplementação (27/08) — guarda condicional substitui a semente dentro do bloco de busca:** o usuário reverteu `ui/form_servidor.py` pra uma versão anterior a essa pendência (pra reduzir volume de mudanças acumuladas) e reimplementou a lógica de nonce do zero, com o mesmo objetivo mas uma variação mais simples pro problema do 2º efeito colateral (linha 499 acima): em vez de escrever a semente de `cargo_classe`/`cargo_nivel`/`cargo_grau` **dentro** do bloco `if busca_atual != ultima_busca_servidor` (acoplado à lógica de busca), a semente agora é escrita **logo antes de cada widget renderizar**, protegida por `if key not in st.session_state: st.session_state[key] = ds[campo]`. Efeito prático idêntico (a guarda só dispara na primeira aparição de cada key, ou seja, exatamente quando o nonce muda), mas desacopla a semeadura da lógica de busca — não precisa calcular `nonce_novo` dentro do bloco de busca nem duplicar a atribuição lá.
  - Também corrigido nesta reimplementação: os 3 `on_change` (Cargo/Nível/Grau) precisam de `args=(key,)` explícito — sem isso o Streamlit chama o callback sem argumento e lança `TypeError` (`on_change_maiusculo_strip() missing 1 required positional argument: 'key'`) assim que o usuário edita o campo. Bug introduzido numa iteração intermediária (key adicionada antes do `args=`) e pego em revisão antes de ir pra teste.
  - Nível usa `on_change_strip` (sem forçar maiúsculas — valor costuma ser numérico/romano, ex. "2" ou "II", ver `data/provedor_servidores.py`), Cargo e Grau usam `on_change_maiusculo_strip`.
  - **Decisão registrada:** o warning do Streamlit sobre `value=` + Session State API (linha 499) foi avaliado e considerado aceitável de ignorar caso reapareça em algum campo no futuro — funcionalmente o `session_state` sempre prevalece sobre `value=` quando os dois coexistem, então não há bug real, só ruído no terminal. Se for necessário silenciar, a opção mais cirúrgica é um `logging.Filter` no logger `"streamlit"` filtrando pela mensagem específica (em vez de `[logger] level = "error"` no `.streamlit/config.toml`, que esconde todo warning do Streamlit, não só esse).
  - Comentários explicando o padrão (leitura do nonce pós-busca; guarda `if key not in session_state` nos campos com `on_change`) foram adicionados diretamente em `ui/form_servidor.py`, pra não depender só deste histórico pra entender o "porquê" do código.
  - Validação desta rodada foi só por revisão de código (sem Playwright) — segue valendo o mesmo aviso da linha 505: confirmação em uso real ainda pendente.
  - **Achado à parte, não tratado:** `ui/form_servidor.py` ainda importa `FormatadorCampos` e `on_change_masp` (linha 3) sem usar nenhum dos dois — sobra de uma versão anterior do arquivo. Cleanup trivial, não bloqueia nada.

### 4.15 🟡 Pendente — ajustes nos cálculos de verbas conforme repasses da equipe do HEM

- Aguardando detalhamento específico da equipe do HEM sobre quais fórmulas/regras precisam de ajuste. Registrado aqui só como lembrete de que revisões nas calculadoras (`calculadoras/*.py`) estão a caminho — sem escopo definido ainda.

### 4.16 🟡 Pendente — Nível: converter algarismo arábico para romano ao preencher manualmente

- Hoje a conversão só acontece num sentido: `data/provedor_servidores.py` (`NIVEL_ROMANO_PARA_ARABICO`) converte o `nivel` vindo do Supabase (romano, ex. "II") para arábico (ex. "2"), porque `data/tabelas.json` (`tabela_cargos`) usa arábico na busca de cargo.
- Quando o usuário **digita** o Nível manualmente (cargo não encontrado automaticamente), o campo aceita o algarismo arábico como está — não há conversão de volta pra romano em nenhum ponto do fluxo (tela, PDF, etc.).
- Falta avaliar: converter pra romano só na exibição (mantendo arábico internamente pra bater com `tabela_cargos`), ou se o pedido é sobre outro ponto do fluxo (ex. PDF exportado). Confirmar com o usuário o comportamento exato esperado antes de implementar.

### 4.17 🟡 Pendente — GRS: trocar de selectbox por preenchimento manual do valor

- Hoje o campo `grs_risco` (`ui/selecao_verba.py`) é um `selectbox` com opções textuais ("Risco Médio", "Risco Alto", "Não faz jus" — 2 ou 3 opções dependendo da verba, ver `_render` linha ~145), resolvido pra valor numérico via `ProvedorDadosFhemig.obter_valor_grs(grs_risco)` (parser centralizado, puxa de `tabela_grs` em `data/tabelas.json`).
- Pedido: substituir esse selectbox por um campo de valor livre (o usuário digita o valor da GRS diretamente, em vez de escolher risco médio/alto/não faz jus e deixar o sistema resolver o valor).
- Impacto a mapear antes de implementar: todas as calculadoras que hoje recebem `grs_risco` (`grs_dias.py`, `grs_meses.py`, `grs_13.py`, `grs_desconto_horas.py`, `ferias_terco.py`, `ferias_indenizadas.py`, `faltas_horas.py`, `faltas_dias.py`, `ipsemg.py`, `licenca_maternidade.py`) usam `ProvedorDadosFhemig.obter_valor_grs(grs_risco)` internamente — precisam passar a receber o valor já numérico direto, sem o parser. Também mexe em `CONFIG_CAMPOS` (`ui/config.py`) e na lógica dinâmica de exibição de 2 vs 3 opções (que deixa de fazer sentido).

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
- ~~**INSS Mensal**: a base atualmente usa **apenas o `vencimento_basico`**...~~ ✅ Esclarecido (18/08) — ver seção 14
- **INSS Mensal — soma por competência**: hoje `valor_outras_vantagens` soma **todo** o histórico da sessão, sem filtrar por mês/ano batendo com a competência do cálculo do INSS Mensal sendo feito. Confirmar com a área se é necessário filtrar por competência (ver seção 14).
- ~~GIEFS 13º: o valor a sofrer incidência é o próprio valor da GIEFS?~~ ✅ Esclarecido — a base do INSS sobre 13º é a soma (13º + GIEFS 13º)
- **INSS sobre 13º Salário**: base hoje é só `13º Salário + GIEFS 13º`. Falta avaliar se **Piso Enfermagem — 13º** e **GRS — 13º** também devem entrar, seguindo o mesmo raciocínio aplicado ao INSS Mensal (ver seção 14 e pendência 4.6).
- Aumento Salarial: cálculo combinado "2024 + 2026" será **composto** (`base × 1,0462 × 1,054`)? Aguardando confirmação da área. **Relacionado:** o novo campo `valor_outras_vantagens` do INSS Mensal soma automaticamente todas as ocorrências de "Aumento Salarial" no histórico (2024 e 2026 juntos, se ambas existirem) — se o cálculo combinado for confirmado como composto, pode ser necessário revisar essa soma simples.
- **Adicional de Desempenho (ADE) é "somente efetivo"** (achado em 19/08, ver pendência 4.7): o documento oficial de levantamento de dados do RH/CCPT indica que o ADE (código 537) só se aplica a servidores efetivos. Como a calculadora é exclusivamente para **contratados**, isso levanta a dúvida se o campo `ad_desempenho` — usado hoje em `ferias_terco.py`, `faltas_horas.py`, `faltas_dias.py` e `ipsemg.py` — deveria ser removido dessas fórmulas. Não avaliado ainda; aguardando decisão para tratar em sessão futura.

---

## 7. Como rodar

```bash
streamlit run app.py
```

Dependências: `streamlit`, `reportlab`, `pandas`, `supabase` (ver `requirements.txt`)

Para reimportar/atualizar os dados dos servidores no Supabase (requer `.streamlit/secrets.toml` com `[supabase_admin]`):

```bash
python scripts/populate_servidores.py
```

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
- `65b10ae` — "feat: revisa verbas de cálculo de grs, férias e inicia revisão de verbas de giefs"
- `4892e40` — "feat: revisa cálculos de giefs e verbas de 13º"
- `a4a6e14` — "feat: revisa verbas de 13o, implementa inss 13o e desconto de ipsemg"
- `d5f4576` — "feat: adiciona lógica de exportar pdf com histórico dos cálculos"
- `172ccef` — "feat: implementa lógica de persistência dos valores dos campos entre troca de verbas e cálculo de licença maternidade, revisão final das regras de negócio iniciais dos cálculos conforme planilha fornecida pela equipe da taxação" (sessão 17/08 — ver seção 13)

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
---

## 12. Plano de desenvolvimento — sessão 14/08

> **Sessão:** correção do pré-preenchimento do histórico + implementação do PDF + planejamento da persistência de campos manuais.
> **Status:** trabalho em andamento — alguns itens concluídos, outros pendentes (ver marcadores ✅/🟡).

### 12.1 ✅ Concluído — Correção do pré-preenchimento (bug do histórico)

**Problema:** ao trocar de verba, campos que vêm do histórico (adicional noturno, grat. final de semana, 13º, GIEFS 13º, ajuda de custo) não voltavam para o valor do cálculo anterior — mantinham o valor editado manualmente em outra verba (ex.: editar "Adicional Noturno" no 13º e ver esse valor no IPSEMG em vez do histórico).

**Causa raiz:** widgets sem `key` explícita tinham chave automática baseada no rótulo; o Streamlit reutilizava o estado persistido e ignorava o default `value`, e **apaga o estado de widgets não renderizados** numa execução (confirmado via debug).

**Solução aplicada em `ui/selecao_verba.py`:**
- Cada campo passou a receber uma `campo_key` explícita:
  - **Campos do histórico** (5): `key = "{verba_nonce}::{campo}"` → o nonce muda a cada troca de verba, o widget é tratado como novo e o default do histórico é reaplicado.
  - **Campos manuais** (vencimento, GIEFS, dias, GRS, etc.): `key = "in::{campo}"` → mantém o valor digitado enquanto o widget for renderizado entre verbas.

**Validação (AppTest):**
| Cenário | Resultado |
|---|---|
| Histórico reseta na troca (adicional no IPSEMG volta pro histórico) | ✅ |
| GRS persiste entre verbas que o usam (IPSEMG → 13º) | ✅ |
| **GIEFS/dias persiste após passar por verba não relacionada (GIEFS → 13º → GIEFS)** | ❌ **PENDENTE** (requer mecanismo `mem`, ver 12.3) |

### 12.2 ✅ Concluído — Exportação de PDF (`utils/exportador_pdf.py`)

- Classe **`GeradorPDF`** implementada no layout do `PDFGenerator` de outra aplicação.
- Estrutura: `BaseDocTemplate` + `PageTemplate` (1ª página com logo, demais sem), cor institucional `#108da5`, seções "Dados do Servidor", "Verbas Calculadas" (com totais), "Memória de Cálculo" e "Observações", rodapé com data/aviso.
- Logo: `assets/cabecalho_pdf.png` (desenhado só se o arquivo existir).
- Integração: botão **"📄 Gerar PDF"** em `_render_historico` (`st.download_button`); `GeradorPDF` exportado pelo pacote `utils`.

### 12.3 ✅ Resolvido (17/08) — Persistência de campos manuais

**Resolução:** em vez do mecanismo `mem::{campo}` descrito abaixo, a persistência foi implementada via o dicionário `st.session_state["valores_digitados"]` (`persistidos`), já usado como fallback em todo o bloco de defaults de `_render_calculadora`. Cada campo grava seu valor em `persistidos[campo] = valores[campo]` ao final de cada iteração do loop (ver 2.4 — "Cabeçalho volta a 'irradiar'..."), sobrevivendo à troca de verba (diferente do estado de widget, que o Streamlit apaga quando o campo não é renderizado). Resolve o mesmo problema descrito no critério de aceite abaixo.

> Plano original (histórico, não implementado literalmente — mantido como referência):

**Contexto:** descoberto (via debug/`AppTest`) que o **Streamlit apaga o estado de widgets não renderizados** — `in::valor_giefs` vira `<nao existe>` ao passar pelo 13º. Por isso, a chave `in::...` não garante persistência quando o campo some de uma verba intermediária.

**Plano (a implementar):** persistir o valor dos campos manuais em chave própria (dado nosso, não de widget — o Streamlit não apaga):
1. **Gravar:** ao renderizar cada campo manual, gravar o retorno do widget em `st.session_state[f"mem::{campo}"]` (ou usar callback `on_change`).
2. **Ler:** ao renderizar, usar `value = st.session_state.get(f"mem::{campo}", valor_default)` como default.
3. **Selectbox (GRS, ano, carga):** guardar a string selecionada em `mem`; ao voltar, recomputar o `index` (com fallback pro default se a opção não existir mais — caso do "Não faz jus").
4. **Campos do histórico continuam com o nonce** (reset na troca) — convivem sem conflito.

**Critério de aceite (AppTest):** GIEFS — Dias digita 500 → vai ao 13º → volta → campo GIEFS deve mostrar **500** (hoje volta a 0).

### 12.4 ✅ Commitado
- Trabalho da sessão 14/08 commitado em `d5f4576` ("feat: adiciona lógica de exportar pdf com histórico dos cálculos") e commits seguintes — ver seção 8.

---

## 13. Plano de desenvolvimento — sessão 17/08

> **Sessão:** correção de bugs de persistência/comparação em `ui/selecao_verba.py`, implementação da verba **Licença Maternidade** e revisão final das regras de negócio conforme planilha da equipe de taxação. Trabalho **commitado** em `172ccef` (ver seção 8).

### 13.1 ✅ Concluído — ver seção 2.4 e 3.16
- Fallback `0.0`/`0` do `else` genérico de defaults conforme `tipo` (`moeda` vs. demais)
- Cabeçalho volta a "irradiar" para `vencimento_basico`/`carga_horaria_mensal`/`valor_base_aumento` ao trocar de servidor, mantendo edição manual entre trocas de verba
- Correção de 2 bugs de comparação (`campo == (tupla)` sempre falso; `campo in ("ad_desempenho")` sem vírgula)
- Reordenação de verbas no selectbox (`data/tabelas.json`): "Aumento Salarial" movida para logo após "Hora Extra"
- Nova verba **Licença Maternidade** implementada e validada (4232,07 + 371,91 + 180,00 + 0,00 = 4783,98)

### 13.2 🟡 Plano para amanhã

1. **Deploy** — gerar a URL pública do Streamlit (Streamlit Community Cloud ou equivalente) para a aplicação.
2. **Merge para `main`** — dar merge da branch `galhozinho-iza` (branch de trabalho atual) na `main`.
3. **Dúvida a esclarecer com a área — INSS Mensal e INSS sobre 13º:**
   - Quais verbas efetivamente entram na base de cálculo do INSS Mensal? (ver dúvida já registrada na seção 6/11.2 — hoje a base usa só `vencimento_basico`)
   - Confirmar mais uma vez se a base do INSS sobre 13º (`13º + GIEFS 13º`, já validada em 10.6) está correta, ou se há algo a revisar.
4. **Melhorias a implementar:**
   - **GRS no histórico:** para as verbas de GRS, exibir no nome da linha da tabela do histórico se é "Risco Alto" ou "Risco Médio" (hoje o histórico mostra só o nome da verba, sem essa distinção) — provavelmente ajustar `nome_verba_historico` em `_render_calculadora` (`ui/selecao_verba.py`, por analogia ao tratamento já existente para "Aumento Salarial (2024)"/"Aumento Salarial (2026)").
   - **Busca de dados do servidor pelo MASP:** trazer/preencher automaticamente os dados do servidor a partir do MASP informado (hoje o formulário em `ui/form_servidor.py` não faz essa busca — precisa avaliar se há fonte de dados disponível para isso, ex: nova tabela em `tabelas.json` ou integração externa).
5. **Encaminhar e-mail para a área** solicitando validação e testes para homologação da ferramenta (após os itens acima, ou em paralelo, conforme prioridade).

---

## 14. Plano de desenvolvimento — sessão 18/08

> **Sessão:** revisão da base de cálculo do INSS Mensal, conforme resposta da área de taxação (ver dúvida da seção 13.2, item 3).

### 14.1 ✅ Concluído — Base do INSS Mensal ampliada (residual)

**Resposta da área:** entram na base do INSS Mensal **todas as verbas de Vantagem já calculadas**, **exceto Ajuda de Custo**. As verbas de 13º (13º Salário, GIEFS 13º, Piso 13º, GRS 13º) **não** entram aqui — pelo mesmo raciocínio, elas entram é na base do **INSS sobre 13º Salário** (ver pendência 4.6).

**Abordagem implementada:** em vez de um campo por verba (chegou a ser cogitado e descartado por ficar com campos demais), a base usa um **campo único somado automaticamente** a partir do histórico:

```python
NOMES_EXCLUIDOS_INSS = {
    "Ajuda de Custo Mensal",
    "13º Salário", "GIEFS — 13º Salário",
    "Piso Enfermagem — 13º Salário", "GRS — 13º Salário",
}
valor_outras_vantagens = sum(
    item["valor"] for item in historico
    if item.get("tipo") == "Vantagem" and item.get("nome_verba") not in NOMES_EXCLUIDOS_INSS
)
```

- Campo `valor_outras_vantagens` (novo em `ui/config.py`/`ui/selecao_verba.py`): pré-preenchido com essa soma, mas continua **editável**.
- Campo `outras_verbas` (novo): manual, default `0.0`, sem pré-preenchimento — resguardo para vantagens que a área possa ter esquecido de mapear como verba própria na aplicação.
- **Fórmula:** `Base = vencimento_basico + valor_outras_vantagens + outras_verbas` → tabela progressiva do INSS aplicada sobre essa base (lógica de faixas inalterada).
- **Vantagem da abordagem residual:** soma automaticamente **todas as ocorrências** de cada verba no histórico (não só a mais recente) — resolve por construção a dúvida que existia sobre "somar tudo vs. valor mais recente". Também resolve o caso do "Aumento Salarial" (nome no histórico vem com sufixo de ano, ex. `"Aumento Salarial (2026)"`) sem precisar de lógica de prefixo, já que a soma só filtra por `tipo` e nomes excluídos explícitos.
- **Arquivos alterados:** `calculadoras/inss_mensal.py` (fórmula reescrita), `ui/config.py` (2 campos novos), `ui/selecao_verba.py` (bloco de default para `valor_outras_vantagens`).
- Nenhuma verba de **Desconto** entra na base (natural, já que a soma filtra só `tipo == "Vantagem"`).

**Limitação conhecida (ver seção 6):** a soma não filtra por competência (mês/ano) — soma todo o histórico da sessão, independente do período de cada lançamento. Fica como pendência para quando a área confirmar se isso é necessário.

### 14.2 🟡 Pendências geradas nesta sessão

- Ver seção 4.6: expandir a base do **INSS sobre 13º Salário** para incluir Piso 13º e GRS 13º (mesmo raciocínio, ainda não implementado).
- Ver seção 6: confirmar com a área se `valor_outras_vantagens` deve filtrar por competência.
- Ver seção 6: se o cálculo combinado "Aumento Salarial 2024+2026" vier a ser composto (pendência 10.7), revisar se a soma simples de `valor_outras_vantagens` ainda está correta nesse cenário.

### 14.3 ✅ Concluído — Identidade visual

- **`main.py`**: `st.set_page_config` atualizado — `page_title="Calculadora de Verbas - Fhemig"` e `page_icon="assets/icone.png"` (favicon na aba do navegador).
- **`ui/cabecalho.py`**: adicionada a logo institucional `assets/LogoFhemig.png` no topo da página, ao lado do título (`st.columns` com `vertical_alignment="center"`).
- Novos arquivos de imagem em `assets/`: `icone.png` (favicon) e `LogoFhemig.png` (logo do cabeçalho) — além do já existente `cabecalho_pdf.png` (logo do PDF).

### 14.4 ✅ Concluído — Remoção do `app.py` legado

- Ver seção 4.3 (resolvida). `app.py` saiu da raiz e foi arquivado em `old/app_old.py`; `main.py` é agora o único entrypoint.

### 14.5 ✅ Concluído (18/08) — Deploy no Streamlit Community Cloud

Pendência da seção 13.2 (itens 1 e 2) **executada**:

- Merge de `galhozinho-iza` → `main` feito diretamente no GitHub; branch `galhozinho-iza` excluída (local e remota) após o merge.
- Deploy realizado no [share.streamlit.io](https://share.streamlit.io) apontando pra `main` / `main.py`.
- **Obstáculo encontrado:** erro "You do not have access to this app or it does not exist" ao tentar deployar — causa raiz foi o **GitHub App do Streamlit não estar instalado na organização `fhemig-projetos`** (só na conta pessoal). Resolvido instalando/configurando o app em `github.com/settings/installations` (ou pelo link de gerenciamento de acesso dentro do próprio Streamlit Cloud) e liberando o repositório `calculadora-verbas-fhemig` para a org.
- Mesmo após corrigir a instalação, o deploy só emplacou **colando a URL completa do repositório manualmente** no formulário do Streamlit Cloud (o seletor de repositório/organização não estava listando o repo, provavelmente por cache do dropdown).
- **Local:** branch `galhozinho-iza` local também apagada após confirmar (`git merge-base --is-ancestor`) que estava 100% contida em `origin/main`; `main` local atualizado via `git pull`.

### 14.6 🟡 Novas pendências identificadas pós-deploy (18/08)

Levantadas pelo usuário após o app já publicado — ver detalhes em 4.7 a 4.10:
1. ✅ Substituir os códigos placeholder/incorretos das verbas em `data/tabelas.json` pelos códigos oficiais (4.7) — **10 de ~20 códigos aplicados em 19/08**, restante aguardando confirmação da área.
2. Preenchimento automático dos dados do servidor no cabeçalho a partir do MASP (4.8).
3. ✅ Incluir Data Fim Efetiva na tabela "Dados do Servidor" do PDF exportado (4.9) — resolvido em 19/08.
4. ✅ Ampliar o intervalo de anos selecionáveis em Data de Admissão e Data Fim Efetiva (4.10) — resolvido em 19/08.

### 14.7 ✅ Concluído (19/08) — README.md atualizado

- Entrypoint corrigido para `main.py` (antes mandava rodar `app.py`, já removido).
- Lista completa das 24 verbas com nomes atuais (antes faltavam Piso 13º, GRS 13º, GRS — Meses, Licença Maternidade).
- Nova seção com o link da aplicação publicada: `https://calculadora-verbas-fhemig.streamlit.app/`.
- Instalação via `pip install -r requirements.txt` (antes só mandava instalar `streamlit`).
- Seção "Próximos passos" desatualizada substituída por ponteiro para `contexto.md`/`duvidas.md`.

---

## 15. Plano de desenvolvimento — sessão 24/08

> **Sessão:** integração com Supabase para popular e consultar dados funcionais dos servidores, com pré-preenchimento automático do cabeçalho a partir de MASP + Nº de Admissão. Trabalho **não commitado ainda** nesta sessão.

### 15.1 ✅ Concluído — Script de importação para o Supabase (`scripts/populate_servidores.py`)

- Novo script (fora do pacote da aplicação) que lê `data/dados_funcionais_calculadora_verbas.csv` e faz `upsert` em lotes de 500 na tabela `servidores` do Supabase, usando `masp_admissao` como chave de conflito.
- **Bug encontrado e corrigido:** 45 valores duplicados de `masp_admissao` no CSV (2904 linhas → 2859 únicas) faziam o `upsert` falhar com `ON CONFLICT DO UPDATE command cannot affect row a second time`. Resolvido deduplicando via `{r["masp_admissao"]: r for r in registros}` antes do upsert (mantém a última ocorrência de cada). Detalhes e a pendência de confirmação com a área de extração de dados em 4.11.
- Requer `.streamlit/secrets_admin.toml` (ou `secrets.toml`, dependendo da versão) com a seção `[supabase_admin]` (`url`, `key`) — **não versionado** (fora do git).
- Executado com sucesso: **2859 registros** importados para a tabela `servidores`.

### 15.2 ✅ Concluído — Pré-preenchimento do cabeçalho via Supabase

**Novo arquivo:** `data/provedor_servidores.py` — classe `ProvedorServidoresSupabase`, seguindo o mesmo padrão de `ProvedorDadosFhemig` (namespace estático), mas para dados externos (Supabase) em vez do JSON local:
- `_cliente()` (função de módulo, `@st.cache_resource`) — cria e cacheia o cliente Supabase a partir de `st.secrets["supabase_admin"]`.
- `buscar_servidor(masp, numero_admissao)` (`@st.cache_data`) — consulta `servidores` filtrando por `masp` + `numero_admissao` (`.eq(...).eq(...).limit(1)`), com `try/except` pra não quebrar o app em caso de falha de rede (mostra `st.warning` e retorna `None`).
- **Conversão de nível romano→arábico:** o campo `nivel` vem em algarismo romano no Supabase (`"I"` a `"VI"`, confirmado por consulta — ver `NIVEL_ROMANO_PARA_ARABICO`), mas `tabela_cargos` (`data/tabelas.json`) usa arábico (`"1"` a `"4"`). Sem essa conversão, a busca local de cargo (`ProvedorDadosFhemig.buscar_cargo`) nunca encontraria nada para dados reais vindos do Supabase — corrigido na fonte, dentro de `buscar_servidor`.
- Registrado em `data/__init__.py` e adicionado `supabase>=2.0.0` ao `requirements.txt`.

**`ui/form_servidor.py` reestruturado:**
- Ordem dos campos do cabeçalho mudou de **Nome → MASP → Admissão** para **MASP → Nº de Admissão → Nome** (decisão do usuário) — a busca acontece assim que os dois primeiros estão preenchidos, e o Nome (junto com os demais campos) já vem pré-preenchido quando o widget de Nome é renderizado.
- Gatilho da busca: **automático** (mesmo padrão já usado pela busca de cargo local), não por botão — decisão explícita do usuário, com cache (`st.cache_data`) evitando reconsultas repetidas pra mesma combinação MASP+Admissão.
- Quando encontrado: preenche `nome`, `dt_admissao`, `dt_fim_efetiva` (convertidas de string ISO via `datetime.date.fromisoformat`), `cargo_classe` (de `cod_carreira`), `cargo_nivel`, `cargo_grau` e `ch_semanal` (de `carga_horaria`) — disparando em cascata a busca local de cargo já existente (`ProvedorDadosFhemig.buscar_cargo`), que por sua vez preenche o vencimento básico.
- Quando não encontrado: `st.info` avisando, campos ficam livres para preenchimento manual (comportamento idêntico ao já existente para cargo não encontrado).
- **Simplificação do usuário:** consolidada a checagem `if ds["masp"] and ds["admissao"]:` (antes duplicada — uma vez pra disparar a busca, outra pra decidir qual mensagem mostrar) num único bloco, fundindo a exibição de `st.success`/`st.info` dentro do próprio bloco de busca — mais simples que a alternativa cogitada (variável `busca_realizada`).
- Testado end-to-end no navegador (Playwright) nos dois caminhos (encontrado / não encontrado), sem erros de console.

### 15.3 ✅ Concluído — Carga Horária Semanal/Mensal viraram campos livres

Ver detalhamento completo em 4.12. Resumo: `selectbox` com opções fixas (que não cobriam todos os valores reais da base: 12h, 24h, 60h além de 30h/40h) foi substituído por `number_input` livre em `ui/form_servidor.py`, e o campo espelho `carga_horaria_mensal` em `ui/selecao_verba.py` teve seu bloco especial de `selectbox` removido, caindo no `number_input` genérico já usado por `vencimento_basico`.

### 15.4 🟡 Pendências geradas nesta sessão

1. **Configurar secrets do Supabase no Streamlit Cloud** antes do deploy dessa funcionalidade (ver 4.13) — hoje só funciona localmente.
2. **Confirmar correção do bug de reset de campos ao digitar duas buscas seguidas** (ver 4.14) — corrigido via `key=` explícita, mas não confirmado em uso real.
3. **Confirmar com a área de extração de dados** a unicidade de `masp_admissao` (ver 4.11) e os valores válidos de carga horária (ver 4.12).
4. `calculadoras/faltas_horas.py` sem proteção contra divisão por zero em `carga_horaria_mensal` (ver 4.12) — não corrigido, só identificado.
5. Avaliar se `app_hem.py` (app de teste na raiz, criado para testar deploy de múltiplos apps no mesmo repo) ainda é necessário ou pode ser removido (ver 4.13).
6. `teste_supabase.py` (raiz do repo, não commitado) parece ser um script exploratório do usuário para testar a conexão com Supabase — avaliar se deve ser movido para `scripts/`, formalizado, ou descartado antes do commit.

