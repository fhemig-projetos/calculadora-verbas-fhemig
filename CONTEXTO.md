# Contexto — Calculadora de Verbas FHEMIG

## Objetivo
Implementar a classe `ui/form_servidor.py` para encapsular o formulário de
dados do servidor (cabeçalho do PDF) que hoje está solto no `app.py`.

## Arquivos envolvidos
- `ui/form_servidor.py` → classe sendo implementada
- `teste_form.py` → arquivo de teste para rodar o formulário isolado
- `app.py` → arquivo original (referência)
- `data/provedor_dados.py` → classe `ProvedorDadosFhemig` com busca de cargo
- `utils/formatador_campos.py` → `FormatadorCampos` com `brl()` e `masp()`
- `utils/ui_callbacks.py` → `on_change_masp` (callback opcional)

## O que é um `st.expander`
Cria uma caixa colapsável no Streamlit.
- `expanded=True`: inicia aberta (▼)
- `expanded=False`: inicia fechada (▶)

## Progresso

### ✅ Passo 1 — Concluído
`__init__` criado com todas as 11 chaves do dicionário `dados_servidor`:
- nome, masp, admissao, dt_admissao, dt_fim_efetiva
- cargo_classe, cargo_nivel, cargo_grau
- ch_semanal, ch_mensal, vencimento

### ✅ Passo 2 — Concluído
`render()` implementado com:
1. `with st.expander("Dados do Servidor", expanded=True):`
2. `ds = st.session_state["dados_servidor"]`
3. 3 colunas com: Nome, MASP, Admissão

### ✅ Passo 3 — Concluído
Datas implementadas com `st.date_input` (formato DD/MM/YYYY):
- `dt_admissao` → "Data de Admissão"
- `dt_fim` → "Data Fim Efetiva"

### ✅ Passo 4 — Concluído
Campos de cargo com 4 colunas:
- `c6`: Cargo / Classe (text_input, `.upper().strip()`)
- `c7`: Nível (text_input, `.strip()`)
- `c8`: Grau (text_input, `.upper().strip()`)
- `c9`: C.H. Semanal (selectbox com opções: 20, 30, 40, 44 Horas Semanais)

### ⬜ Passo 5 — Próximo passo
Implementar a busca automática de cargo via `ProvedorDadosFhemig.buscar_cargo()`
com a chave composta de 4 campos (classe + nivel + grau + ch_semanal).

Atualmente o esqueleto está montado:
```python
cargo_encontrado = None
if cargo_classe and cargo_nivel and cargo_grau and ch_semanal != "- Selecione -":
    cargo_encontrado = ProvedorDadosFhemig.buscar_cargo(cargo_classe, cargo_nivel, cargo_grau, ch_semanal)

if cargo_encontrado:
    pass  # ← precisa preencher ds["ch_mensal"], ds["vencimento"], etc.
```

### ⬜ Passo 6 — Fallback manual
Se cargo não encontrado, exibir campos manuais para:
- C.H. Mensal (number_input)
- Vencimento Básico (number_input)

### ⬜ Pendências técnicas
- Remover `key="ch_semanal_select"` do selectbox (desnecessário, discutido em reunião)
- Ajustar `__init__` para inicializar `dt_admissao` e `dt_fim_efetiva` como `None` (já que agora são `date_input`)
- Ajustar `gerar_pdf()` em `app.py` para lidar com `datetime.date` ao invés de string nas datas

## Mudanças já aplicadas
- `data/provedor_dados.py`: `buscar_cargo()` agora aceita 4º parâmetro `ch_semanal` e filtra por ele
- `ui/form_servidor.py`: `render()` com Passos 2, 3 e 4 implementados

## Como testar
```bash
streamlit run teste_form.py
```

## Observações
- A formatação do MASP (hífen no dígito verificador) é opcional e pode ser
  deixada para depois.
- O `on_change_masp` existe em `utils/ui_callbacks.py` mas o `app.py` original
  não usa.
- A chave de busca de cargo agora é composta por 4 campos: Classe + Nível + Grau + CH Semanal