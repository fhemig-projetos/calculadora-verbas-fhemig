import streamlit as st
# Importa as funções que criamos dentro do pacote data
from data import ProvedorDadosFhemig
from utils import FormatadorCampos, on_change_masp, on_change_moeda

# Inicializa as classes
provedor_dados = ProvedorDadosFhemig()
formatador_campos = FormatadorCampos()

st.title("🧪 Laboratório de Teste do Provedor de Dados")
st.markdown("Use este espaço para validar se o arquivo JSON está sendo lido corretamente.")

st.subheader("1. Testando 'buscar_cargo'")
c1, c2, c3 = st.columns(3)
classe = c1.text_input("Classe", value="PENF")
nivel = c2.text_input("Nível", value="2")
grau = c3.text_input("Grau", value="A")

# Executa a função do provedor
cargo_resultado = provedor_dados.buscar_cargo(classe, nivel, grau)

if cargo_resultado:
    st.success(f"Cargo encontrado! Vencimento: R$ {cargo_resultado['vencimento']}")
    st.json(cargo_resultado)
else:
    st.error("Cargo não encontrado na base de dados (tabelas.json).")

st.markdown("---")

st.subheader("2. Testando 'obter_tabela_inss'")
ano = st.selectbox("Selecione o Ano", [2027, 2026, 2025, 2024])
tabela_inss = provedor_dados.obter_tabela_inss(ano)
st.write(f"Faixas de INSS retornadas para o ano {ano}:")
st.json(tabela_inss)

st.markdown("---")

st.subheader("3. Visualizando Metadados e Grupos")
with st.expander("Ver dicionário completo de verbas_meta"):
    st.json(provedor_dados.obter_metadados_verbas())

with st.expander("Ver dicionário de grupos organizados"):
    st.json(provedor_dados.obter_grupos_verbas())   

st.subheader("4. Testando 'FormatadorCampos' (Módulo Utils)")
st.write("Demonstração prática: os inputs guardam o dado puro (float/str) e a tela exibe a máscara.")

col_input_valor, col_input_masp = st.columns(2)

with col_input_valor:
    valor_teste = st.number_input(
        "Digite um valor numérico bruto:",
        value=14204.52,
        format="%.2f",
        step=0.01,
        key="campo_valor_teste",
        on_change=on_change_moeda,
        args=("campo_valor_teste",),   # <- adiciona isso
        help="Ao sair do campo (Tab), arredonda automaticamente para 2 casas.",
    )

with col_input_masp:
    masp_teste = st.text_input(
        "Digite um MASP para mascarar:",
        value="12345678",
        key="masp_input",
        on_change=on_change_masp,
        args=("masp_input",),          # <- adiciona isso
        placeholder="Ex: 12345678",
        help="Ao sair do campo (Tab), formata automaticamente para 1234567-8.",
    )

st.write("##### Máscaras geradas pela classe:")

cx1, cx2, cx3 = st.columns(3)

with cx1:
    st.caption(f"moeda_com_simbolo({st.session_state['campo_valor_teste']})")
    st.success(FormatadorCampos.moeda_com_simbolo(st.session_state["campo_valor_teste"]))

with cx2:
    st.caption(f"moeda_sem_simbolo({st.session_state['campo_valor_teste']})")
    st.info(FormatadorCampos.moeda_sem_simbolo(st.session_state["campo_valor_teste"]))

with cx3:
    st.caption(f"masp('{st.session_state['masp_input']}')")
    st.error(st.session_state["masp_input"])