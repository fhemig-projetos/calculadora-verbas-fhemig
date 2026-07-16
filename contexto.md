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
│   ├── gratificacao_final_semana.py  # ✅ Implementada (⚠️ fator 0,5 — ver pendências)
│   ├── grs_dias.py            # ✅ Implementada
│   ├── inss_mensal.py         # ✅ Implementada
│   └── decimo_terceiro.py     # ✅ Implementada (com _parser_nivel_grs)
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

### 2.1 Calculadoras (6 de 21)

| Verba | Arquivo | Status |
|---|---|---|
| Hora Extra | `calculadoras/hora_extra.py` | ✅ |
| Adicional Noturno | `calculadoras/adicional_noturno.py` | ✅ |
| Gratificação de Final de Semana | `calculadoras/gratificacao_final_semana.py` | ✅ |
| GRS — Dias | `calculadoras/grs_dias.py` | ✅ |
| 13º Salário | `calculadoras/decimo_terceiro.py` | ✅ |
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

## 3. Próximo passo: GIEFS — 13º Salário

### Fórmula
```
Valor base ÷ 12 × Nº de Parcelas
```

### Arquivos a criar/modificar

#### 3.1 Criar `calculadoras/giefs_13.py`

```python
from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraGIEFS13(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: Valor base ÷ 12 × Nº de Parcelas"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_base", "numero_parcelas"]

    def calcular(self, valor_base: float, numero_parcelas: int) -> ResultadoCalculo:
        valor = (valor_base / 12) * numero_parcelas
        memoria = [
            f"{FormatadorCampos.brl(valor_base)} ÷ 12 = {FormatadorCampos.brl(valor_base/12)}/parcela",
            f"× {numero_parcelas} parcelas",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)
```

#### 3.2 Modificar `calculadoras/__init__.py`
Adicionar: `from .giefs_13 import CalculadoraGIEFS13`

#### 3.3 Modificar `calculadoras/factory.py`
Adicionar ao `REGISTRO_CALCULADORAS`:
```python
"GIEFS — 13º Salário": CalculadoraGIEFS13(),
```

#### 3.4 Modificar `ui/config.py`
Adicionar:
```python
"valor_base": {"label": "Valor base (R$)", "tipo": "moeda"},
"numero_parcelas": {"label": "Nº de Parcelas", "tipo": "parcelas"},
```

#### 3.5 Modificar `ui/selecao_verba.py`
No `_render_calculadora()`, adicionar antes do `else`:
```python
elif campo == "valor_base":
    valor_default = 0.0
elif campo == "numero_parcelas":
    valor_default = 12
```

No bloco de renderização, adicionar:
```python
elif campo == "numero_parcelas":
    valores[campo] = st.number_input(
        config["label"],
        value=valor_default,
        min_value=1,
        max_value=12,
    )
```

`valor_base` cai no `else` como `number_input` normal.

---

## 4. Pendências (a fazer)

### 4.1 Calculadoras faltantes (15 restantes do `app.py`)

Seguir o mesmo padrão das já implementadas.

| Verba | Código | Tipo | Fórmula (app.py) |
|---|---|---|---|
| GIEFS — 13º Salário | 3171 | Vantagem | valor_base ÷ 12 × parcelas |
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

### 4.3 Funcionalidade de "Conferência"

- No `app.py` (linhas 670-683): compara valor calculado com valor informado pela unidade
- Não implementada na versão modular

### 4.4 Agrupamento de verbas em categorias

- No `app.py` (linhas 343-353): GRUPOS organizam as verbas (Gratificações, 13º, GIEFS, GRS, Férias, Descontos)
- Na versão modular, as verbas são listadas em ordem alfabética do JSON

### 4.5 Remover duplicação de dados

- `app.py` tem `TABELA_CARGOS`, `TABELA_INSS`, `VERBAS_META` duplicados
- Versão modular usa `data/tabelas.json`
- Quando `app.py` for descontinuado, remover as duplicatas

---

## 5. Bugs conhecidos

### 5.1 Fator da Gratificação de Final de Semana

- `app.py` (linha 386): fator **1,0833 (13/12)** ✅
- `calculadoras/gratificacao_final_semana.py` (linha 24): fator **0,5** ❌
- **Suspeita:** o valor correto é 13/12 (1,0833). O fator 0,5 parece ser um erro de implementação.

### 5.2 Condição obsoleta no form_servidor.py

- Linha 56: `if ds["ch_semanal"] != "- Selecione -":` — a opção "- Selecione -" foi removida, então a condição é sempre True. Pode ser removida.

---

## 6. Dúvidas em aberto (ver `dúvidas.md`)

- Abono Emergência é valor fixo (R$ 150)?
- GIEFS 13º: o valor a sofrer incidência é o próprio valor da GIEFS?

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
- Último commit: `ee184f0` — "feat: implementa competencia por ano para cálculo de 13o e campo de observação"

---

## 9. Padrão para criar novas calculadoras

1. Criar classe em `calculadoras/` estendendo `CalculadoraVerba`
2. Implementar `descricao_formula`, `campos_necessarios`, `calcular()`
3. Importar em `calculadoras/__init__.py`
4. Registrar em `calculadoras/factory.py`
5. Adicionar campos em `ui/config.py` (se forem novos)
6. Adicionar defaults e renderização em `ui/selecao_verba.py`