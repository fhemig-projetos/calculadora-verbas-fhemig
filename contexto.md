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
│   ├── decimo_terceiro.py     # ✅ Implementada (com _parser_nivel_grs)
│   ├── giefs_13.py            # ✅ Implementada
│   └── piso_enfermagem_13.py  # ✅ Implementada
│
├── data/                      # Dados externos
│   ├── __init__.py
│   ├── provedor_dados.py      # ProvedorDadosFhemig (cache + acesso JSON)
│   └── tabelas.json           # Cargos, INSS, verbas, GRS
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

### 2.1 Calculadoras (8 de 21 — 13 restantes)

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
- **Competência** (mês/ano ou apenas ano para 13º)
- **Observação** (opcional, até 200 caracteres)
- **Histórico** em dataframe com totais (vantagens, descontos, líquido)
- Botões: "Remover último", "Limpar lista"

### 2.3 Dados

- `data/tabelas.json` com:
  - `tabela_cargos`: 4 registros (PENF, TOS, AGAS)
  - `tabela_inss`: 2024, 2025, 2026
  - `verbas`: 21 metadados (código + tipo)
  - `tabela_grs`: `nao_faz_jus: 0.0`, `risco_medio: 160.20`, `risco_alto: 320.40`

### 2.4 Decisões de implementação recentes

- **GRS**: Adicionada chave `"nao_faz_jus": 0.0` no JSON. UI dinâmica: se verba = "GRS — Dias", exibe apenas "Risco Médio" e "Risco Alto"; senão, exibe as 3 opções. Calculadoras usam `_parser_nivel_grs()` ou parser inline para mapear string → chave do JSON.
- **CH Mensal**: Mudou de `number_input` para `selectbox` com opções [120, 180, 240, 264]. Default vem do formulário do servidor (CH Semanal ÷ 5 × 30). Se valor default não estiver nas opções, fallback para índice 2 (240).
- **CH Semanal**: Selectbox sem opção "Selecione", default = 40 (index 2).

---

## 3. Próximas implementações planejadas

### 3.1 ✅ GIEFS — 13º Salário (implementada)

**Arquivo:** `calculadoras/giefs_13.py` — classe `CalculadoraGIEFS13`

**Fórmula:** `Valor GIEFS ÷ 12 × Nº de Meses`

**Campos:** `valor_giefs` (moeda), `numero_meses` (reaproveitado)

**Detalhes:**
- `valor_giefs` → campo de input do tipo moeda, default 0.0
- `numero_meses` → reutiliza campo já existente, default 1, min 1, max 12
- Registrada na factory como `"GIEFS — 13º Salário"` (código 3171, Vantagem)

### 3.2 ✅ Piso Enfermagem — 13º Salário (implementada)

**Arquivo:** `calculadoras/piso_enfermagem_13.py` — classe `CalculadoraPisoEnfermagem13`

**Fórmula:** `Valor do Piso ÷ 12 × Nº de Meses`

**Campos:** `valor_piso` (moeda), `numero_meses` (reaproveitado)

**Detalhes:**
- `valor_piso` → campo de input do tipo moeda, default 0.0
- `numero_meses` → reutiliza campo já existente
- Registrada na factory como `"Piso Enfermagem — 13º Salário"` (código 1164, Vantagem)

### 3.3 🔄 INSS sobre 13º Salário (próxima implementação)

**Arquivo:** `calculadoras/inss_decimo_terceiro.py` — classe `CalculadoraINSSDecimoTerceiro`

**Fórmula:** `INSS s/ 13º = (13º + GIEFS 13º) × Alíquota − Dedução (tabela progressiva)`

**Entradas:**
| Campo | Origem |
|-------|--------|
| `valor_13_salario` | Busca automática do último valor de "13º Salário" no histórico |
| `giefs_13_salario` | Busca automática do último valor de "GIEFS — 13º Salário" no histórico |
| `ano_referencia` | Selectbox do usuário (2024, 2025, 2026) |

**Base de cálculo:** `valor_13_salario + giefs_13_salario`

**Regra de negócio (confirmada):** A base é a **soma** do 13º Salário com a GIEFS do 13º. Exemplo:
```
1010,95 (13º) + 64,04 (GIEFS 13º) = 1074,99 → alíq 7,5% → 80,62
```

**Lógica:** Reaproveita `ProvedorDadosFhemig.obter_tabela_inss(ano)` — mesma tabela progressiva do INSS Mensal.

**Arquivos a modificar:**

| Arquivo | Ação |
|---------|------|
| `calculadoras/inss_decimo_terceiro.py` | Criar |
| `calculadoras/__init__.py` | +1 import |
| `calculadoras/factory.py` | +1 import + 1 registro |
| `ui/config.py` | +2 campos: `valor_13_salario`, `giefs_13_salario` |
| `ui/selecao_verba.py` | +2 defaults com busca no histórico (mesmo padrão de `grat_final_semana` e `adicional_noturno`) |

---

## 4. Pendências (a fazer)

### 4.1 Calculadoras faltantes (13 restantes do `app.py`)

Seguir o mesmo padrão das já implementadas.

| Verba | Código | Tipo | Fórmula (app.py) |
|---|---|---|---|
| INSS sobre 13º Salário | 7708 | Desconto | Tabela progressiva INSS sobre (13º + GIEFS 13º) |
| GIEFS — Dias | 2417 | Vantagem | valor_base ÷ 30 × dias |
| GIEFS — Meses (parcelas) | 2417 | Vantagem | valor_base ÷ 6 × parcelas |
| GIEFS — 1/3 de Férias | 3242 | Vantagem | valor_base ÷ 3 |
| GRS — Meses | 2420 | Vantagem | GRS × meses |
| GRS — Desconto de Horas | 7820 | Desconto | GRS ÷ CH × horas_falta |
| 1/3 de Férias | 2431 | Vantagem | (salário + ab_emerg + ad_desempenho + ad_noturno + GRS) ÷ 3 |
| Férias Indenizadas | 2432 | Vantagem | (salário + GIEFS + ab_emerg + GRS + ad_noturno) ÷ 30 × dias |
| Faltas — Horas (desconto) | 7810 | Desconto | (venc + ad_desem + ab_emerg + GRS) ÷ CH × horas_falta |
| Faltas — Dias (desconto) | 7811 | Desconto | (venc + ad_desem + ab_emerg + GRS) ÷ 30 × dias_falta |
| Ajuda de Custo Mensal | 2070 | Vantagem | valor_diário × dias |
| Desconto de Custeio (4%) | 9018 | Desconto | base × 4% |
| Aumento Salarial (4,62%) | ---- | Vantagem | base × 4,62% |
| Desconto de IPSEMG (3,2%) | 7700 | Desconto | base × 3,2% |

### 4.2 Exportação PDF

- `utils/exportador_pdf.py` está **vazio**
- A função `gerar_pdf()` completa existe no `app.py` (linhas 141-273)
- Precisa ser extraída para o módulo e integrada à UI modular

### 4.3 Remover duplicação de dados

- `app.py` tem `TABELA_CARGOS`, `TABELA_INSS`, `VERBAS_META` duplicados
- Versão modular usa `data/tabelas.json`
- Quando `app.py` for descontinuado, remover as duplicatas

---

## 5. Observações sobre regras de negócio

- **Gratificação de Final de Semana**: fator de cálculo é **0,5** (confirmado como correto)
- **Condição obsoleta no form_servidor.py**: já corrigida — a condição `!= "- Selecione -"` foi removida junto com a opção obsoleta
- **INSS sobre 13º**: a base de cálculo é a **soma** do 13º Salário com a GIEFS do 13º (confirmado com exemplo: 1010,95 + 64,04 = 1074,99)
- **GIEFS 13º**: campo renomeado de `valor_base` para `valor_giefs` (mais semântico), reutiliza `numero_meses` existente
- **Piso Enfermagem 13º**: novo campo `valor_piso`, reutiliza `numero_meses` existente

---

## 6. Dúvidas em aberto (ver `dúvidas.md`)

- Abono Emergência é valor fixo (R$ 150)?
- ~~GIEFS 13º: o valor a sofrer incidência é o próprio valor da GIEFS?~~ ✅ Esclarecido — a base do INSS sobre 13º é a soma (13º + GIEFS 13º)

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
- Pendentes de commit: GIEFS 13º, Piso Enfermagem 13º, INSS sobre 13º

---

## 9. Padrão para criar novas calculadoras

1. Criar classe em `calculadoras/` estendendo `CalculadoraVerba`
2. Implementar `descricao_formula`, `campos_necessarios`, `calcular()`
3. Importar em `calculadoras/__init__.py`
4. Registrar em `calculadoras/factory.py`
5. Adicionar campos em `ui/config.py` (se forem novos)
6. Adicionar defaults e renderização em `ui/selecao_verba.py`