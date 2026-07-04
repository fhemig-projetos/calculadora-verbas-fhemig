# Contexto — Calculadora de Verbas FHEMIG

## Objetivo
Implementar a classe `ui/form_servidor.py` para encapsular o formulário de
dados do servidor (cabeçalho do PDF) que hoje está solto no `app.py`.

## Arquivos envolvidos
- `ui/form_servidor.py` → classe sendo implementada
- `teste_form.py` → arquivo de teste para rodar o formulário isolado
- `app.py` → arquivo original (referência)
- `data/provedor_dados.py` → classe `ProvedorDadosFhemig` com busca de cargo
- `data/tabelas.json` → base de cargos e tabelas
- `utils/formatador_campos.py` → `FormatadorCampos` com `brl()` e `masp()`
- `utils/ui_callbacks.py` → `on_change_masp` (callback opcional)

## Progresso

### ✅ Passo 1 — Concluído
`__init__` criado com todas as chaves do dicionário `dados_servidor`:
- `nome`, `masp`, `admissao`, `dt_admissao` (None), `dt_fim_efetiva` (None)
- `cargo_classe`, `cargo_nivel`, `cargo_grau`
- `ch_semanal` (0), `ch_mensal` (0.0), `vencimento_basico` (0.0)

### ✅ Passo 2 — Concluído
`render()` implementado com:
1. `with st.expander("Dados do Servidor", expanded=True):`
2. `ds = st.session_state["dados_servidor"]`
3. 3 colunas com: Nome, MASP, Admissão

### ✅ Passo 3 — Concluído
Datas implementadas com `st.date_input` (formato DD/MM/YYYY):
- `dt_admissao` → "Data de Admissão"
- `dt_fim_efetiva` → "Data Fim Efetiva"
- Campos vinculados ao `ds` para preservar estado entre reruns

### ✅ Passo 4 — Concluído
Campos de cargo com 4 colunas, todos salvos em `ds[...]`:
- `c6`: Cargo / Classe (text_input, `.upper().strip()`, salvo em `ds["cargo_classe"]`)
- `c7`: Nível (text_input, `.strip()`, salvo em `ds["cargo_nivel"]`)
- `c8`: Grau (text_input, `.upper().strip()`, salvo em `ds["cargo_grau"]`)
- `c9`: C.H. Semanal (selectbox com opções: "- Selecione -", 20, 30, 40, 44)
- Removido `key="ch_semanal_select"` desnecessário

### ✅ Passo 5 — Parcialmente concluído
Busca automática de cargo via `ProvedorDadosFhemig.buscar_cargo()`
com chave composta de 4 campos (classe + nivel + grau + ch_semanal):
```python
cargo_encontrado = ProvedorDadosFhemig.buscar_cargo(
    ds["cargo_classe"], ds["cargo_nivel"], ds["cargo_grau"], ds["ch_semanal"]
)

if cargo_encontrado:
    ds["ch_mensal"] = cargo_encontrado["ch_mensal"]
    ds["vencimento_basico"] = cargo_encontrado["vencimento_basico"]
    # Exibe st.success com dados do cargo encontrado
```

### ⬜ Passo 6 — Fallback manual (pendente)
Se cargo não encontrado, exibir campos manuais para:
- C.H. Mensal (number_input)
- Vencimento Básico (number_input)

## Mudanças já aplicadas
- `data/tabelas.json`: `ch_semanal` alterado de string para int (ex: `40` em vez de `"40 Horas Semanais"`); `vencimento` renomeado para `vencimento_basico`
- `data/provedor_dados.py`: `buscar_cargo()` aceita 4º parâmetro `ch_semanal` (int) e filtra por ele
- `ui/form_servidor.py`: `ch_semanal` agora é int; `vencimento` renomeado para `vencimento_basico`; selectbox sem `key`; campos de cargo sincronizados com `ds`; datas preservam estado; busca automática implementada

## Como testar
```bash
streamlit run teste_form.py
```

## Pendências
- Implementar fallback manual (Passo 6)
- Ajustar `app.py` para usar `ProvedorDadosFhemig` e novo formato (ch_semanal int, vencimento_basico)