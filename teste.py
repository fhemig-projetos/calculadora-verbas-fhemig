import streamlit as st
# Importa as funções que criamos dentro do pacote data
from data import ProvedorDadosFhemig

st.title("🧪 Laboratório de Teste do Provedor de Dados")
st.markdown("Use este espaço para validar se o arquivo JSON está sendo lido corretamente.")

st.subheader("1. Testando 'buscar_cargo'")
c1, c2, c3 = st.columns(3)
classe = c1.text_input("Classe", value="PENF")
nivel = c2.text_input("Nível", value="2")
grau = c3.text_input("Grau", value="A")

# Inicializa e executa a função do provedor
provedor_dados = ProvedorDadosFhemig()
cargo_resultado = provedor_dados.buscar_cargo(classe, nivel, grau)

if cargo_resultado:
    st.success(f"Cargo encontrado! Vencimento: R$ {cargo_resultado['vencimento']}")
    st.json(cargo_resultado)
else:
    st.error("Cargo não encontrado na base de dados (tabelas.json).")

st.markdown("---")

st.subheader("2. Testando 'obter_tabela_inss'")
ano = st.selectbox("Selecione o Ano", [2026, 2025, 2024])
tabela_inss = provedor_dados.obter_tabela_inss(ano)
st.write(f"Faixas de INSS retornadas para o ano {ano}:")
st.json(tabela_inss)

st.markdown("---")

st.subheader("3. Visualizando Metadados e Grupos")
with st.expander("Ver dicionário completo de verbas_meta"):
    st.json(provedor_dados.obter_metadados_verbas())

with st.expander("Ver dicionário de grupos organizados"):
    st.json(provedor_dados.obter_grupos_verbas())