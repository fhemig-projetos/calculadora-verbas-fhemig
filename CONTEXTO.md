# Contexto — Calculadora de Verbas FHEMIG

## Objetivo
Refatorar o `app.py` original para uma arquitetura modular, encapsulando
cada seção da interface em classes próprias dentro do pacote `ui/`.

## Arquivos envolvidos
- `ui/form_servidor.py` → formulário de dados do servidor (✅ concluído)
- `ui/cabecalho.py` → cabeçalho da calculadora (✅ concluído)
- `ui/selecao_verba.py` → seleção e cálculo de verbas (⬜ em andamento)
- `main.py` → entry point do app refatorado
- `app.py` → arquivo original (referência, será descontinuado)
- `data/provedor_dados.py` → classe `ProvedorDadosFhemig` com acesso a dados
- `data/tabelas.json` → base de cargos, INSS e metadados das verbas
- `utils/formatador_campos.py` → `FormatadorCampos` com `brl()` e `masp()`
- `utils/ui_callbacks.py` → `on_change_masp` (callback opcional)

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

### ⬜ Módulo `ui/selecao_verba.py` — Em andamento
Estrutura inicial criada (classe `SelecaoVerba` com `render()` vazio).
Pendente: migrar selectbox de verbas, cálculos, resultado e conferência do `app.py`.

## Mudanças já aplicadas
- `data/tabelas.json`: `ch_semanal` alterado de string para int; `vencimento` renomeado para `vencimento_basico`; `verbas_meta` renomeado para `verbas`; `grupos` removido (não era utilizado)
- `data/provedor_dados.py`: `buscar_cargo()` aceita 4º parâmetro `ch_semanal` (int) e filtra por ele
- `ui/form_servidor.py`: implementação completa dos Passos 1 a 6
- `ui/cabecalho.py`: criado com classe `Cabecalho`
- `ui/selecao_verba.py`: criado com classe `SelecaoVerba` (esqueleto)
- `main.py`: entry point do app refatorado

## Como testar
```bash
streamlit run main.py
```

## Pendências
- Migrar seleção e cálculo de verbas do `app.py` para `ui/selecao_verba.py`
- Migrar geração de PDF do `app.py` para `utils/exportador_pdf.py`
- Migrar histórico e lista de cálculos
- Ajustar `app.py` para usar `ProvedorDadosFhemig` e novo formato (ou descontinuar)