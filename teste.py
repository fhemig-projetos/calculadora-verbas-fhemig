import streamlit as st
# Importa as funções que criamos dentro do pacote data
from data import ProvedorDadosFhemig
from utils import FormatadorCampos

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


st.subheader("4. Testando 'FormatadorCampos'")
st.write("Validação das funções utilitárias de formatação visual.")

# Criamos uma linha com 3 colunas para testar os 3 métodos lado a lado
c1, c2, c3 = st.columns(3)

# Teste 1: Moeda com Símbolo
with c1:
    st.caption("moeda_com_simbolo(14204.529)")
    st.success(formatador_campos.moeda_com_simbolo(14204.529))

# Teste 2: Moeda sem Símbolo
with c2:
    st.caption("moeda_sem_simbolo(14204.529)")
    st.info(formatador_campos.moeda_sem_simbolo(14204.529))

# Teste 3: MASP
with c3:
    st.caption("masp('12345678')")
    masp_formatado = formatador_campos.masp("12345678")
    
    if masp_formatado is None:
        st.warning("Ainda não implementado")
    else:
        st.error(masp_formatado)