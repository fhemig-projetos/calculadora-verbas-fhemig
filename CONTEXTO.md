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

### ⬜ Passo 2 — Próximo passo
Implementar o `render()` com:
1. `with st.expander("📋 Dados do Servidor...", expanded=True):`
2. `ds = st.session_state["dados_servidor"]`
3. 3 colunas com: Nome, MASP, Admissão

Código esperado:
```python
def render(self):
    with st.expander("📋 Dados do Servidor (cabeçalho do PDF)", expanded=True):
        ds = st.session_state["dados_servidor"]
        c1, c2, c3 = st.columns(3)
        ds["nome"]     = c1.text_input("Nome Completo do Servidor", value=ds["nome"])
        ds["masp"]     = c2.text_input("MASP", value=ds["masp"])
        ds["admissao"] = c3.text_input("Admissão", value=ds["admissao"], help="Ex: 1, 2")
```

### ⬜ Passo 3 — Datas (dt_admissao, dt_fim_efetiva)
### ⬜ Passo 4 — Classe, Nível, Grau
### ⬜ Passo 5 — Busca automática de cargo (ProvedorDadosFhemig)
### ⬜ Passo 6 — Fallback manual (campos manuais se cargo não encontrado)

## Como testar
```bash
streamlit run teste_form.py
```

## Observações
- A formatação do MASP (hífen no dígito verificador) é opcional e pode ser
  deixada para depois.
- O `on_change_masp` existe em `utils/ui_callbacks.py` mas o `app.py` original
  não usa.