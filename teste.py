import streamlit as st
import urllib.parse
from data import ProvedorDadosFhemig
from utils import FormatadorCampos, on_change_masp, on_change_moeda, CONFIG_CAMPOS
from calculadoras import REGISTRO_CALCULADORAS

st.title("🧪 Laboratório de Teste do Provedor de Dados")
st.markdown("Use este espaço para validar se o arquivo JSON está sendo lido corretamente.")

st.markdown("""
<style>
    /* Esconde os botões +/- de todos os number_input */
    input[type=number]::-webkit-inner-spin-button,
    input[type=number]::-webkit-outer-spin-button {
        -webkit-appearance: none;
    }
    /* Esconde as setinhas laterais do Streamlit */
    button[data-testid="stNumberInputStepDown"],
    button[data-testid="stNumberInputStepUp"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

st.subheader("1. Testando 'buscar_cargo'")
c1, c2, c3 = st.columns(3)
classe = c1.text_input("Classe", value="eppgg")
nivel = c2.text_input("Nível", value="1")
grau = c3.text_input("Grau", value="j")

# Executa a função do provedor
cargo_resultado = ProvedorDadosFhemig.buscar_cargo(classe, nivel, grau)

if cargo_resultado:
    st.success(f"Cargo encontrado! Vencimento: R$ {cargo_resultado['vencimento']}")
    st.json(cargo_resultado)
else:
    st.error("Cargo não encontrado na base de dados (tabelas.json).")

st.divider()

st.subheader("2. Testando 'obter_tabela_inss'")
ano = st.selectbox("Selecione o Ano", [2027, 2026, 2025, 2024])
tabela_inss = ProvedorDadosFhemig.obter_tabela_inss(ano)
st.write(f"Faixas de INSS retornadas para o ano {ano}:")
st.json(tabela_inss)

st.divider()

st.subheader("3. Visualizando Metadados e Grupos")
with st.expander("Ver dicionário completo de verbas_meta"):
    st.json(ProvedorDadosFhemig.obter_metadados_verbas())

with st.expander("Ver dicionário de grupos organizados"):
    st.json(ProvedorDadosFhemig.obter_grupos_verbas())   

st.divider()

st.subheader("4. Testando 'FormatadorCampos' (Módulo Utils)")
st.write("Demonstração prática: os inputs guardam o dado puro (float/str) e a tela exibe a máscara.")

col_input_valor, col_input_masp = st.columns(2)

with col_input_valor:
    valor_teste = st.number_input(
        "Digite um valor numérico bruto (R$):",
        value=None,
        format="%.2f",
        key="campo_valor_teste",
        on_change=on_change_moeda,
        args=("campo_valor_teste",),
        placeholder="0,00",
        help="Ao sair do campo (Tab), arredonda automaticamente para 2 casas.",
    )

with col_input_masp:
    masp_teste = st.text_input(
        "Digite um MASP para mascarar:",
        value="",
        key="campo_masp_teste",
        on_change=on_change_masp,
        args=("campo_masp_teste",),
        placeholder="Ex: 12345678",
        help="Ao sair do campo (Tab), formata automaticamente para 1234567-8.",
    )

st.divider()
st.subheader("5. Testando Cálculos")

# 1. Seleção Simples
opcoes = ["— Selecione uma verba —"] + list(REGISTRO_CALCULADORAS.keys())
verba = st.selectbox("Selecione a Verba", opcoes)

if verba != "— Selecione uma verba —":
    # Puxa a classe correta através do dicionário de registro
    calculadora = REGISTRO_CALCULADORAS[verba]
    
    st.info(calculadora.descricao_formula)
    st.markdown("### Preencha os dados:")
    inputs_coletados = {}
    
    for nome_campo in calculadora.campos_necessarios:
        config = CONFIG_CAMPOS.get(nome_campo)
        chave_campo = f"input_{nome_campo}"

        if config["tipo"] == "moeda":
            valor = st.number_input( 
                label=config["label"],
                value=None,
                format="%.2f",
                key=chave_campo,
                on_change=on_change_moeda,
                args=(chave_campo,),
                placeholder="0,00",
                help="Ao sair do campo (Tab), arredonda automaticamente para 2 casas.",
            )

        elif config["tipo"] == "hora_mensal":
            valor = st.selectbox(
                        label=config["label"],
                        options=["- Selecione -", 160, 180, 200, 240],
                        key=chave_campo,
                    )

        elif config["tipo"] == "horas_realizadas":
            valor = st.number_input(
                        label=config["label"],
                        value=None,
                        format="%.0f",
                        key=chave_campo,
                        placeholder="0",
                        help="Digite a quantidade de horas trabalhadas."
                    )
            
        inputs_coletados[nome_campo] = valor
        
    if st.button("Testar Captura de Dados"):
        st.write("Dados capturados pelo formulário:")
        st.json(inputs_coletados)
            
        # if config["tipo"] == "hora_mensal":
        # # Campos de Input
        # c1, c2 = st.columns(2)
        # venc = c1.number_input("Vencimento Básico (R$)", value=2000.00)
        # ad = c2.number_input("Adicional Desempenho (R$)", value=500.00)
        
        # c3, c4 = st.columns(2)
        # ch = c3.number_input("Carga Horária", value=240)
        # hr = c4.number_input("Horas Extras Feitas", value=10)
        
        # # 4. Acionamento do Cálculo via OOP
        # if st.button("Calcular", type="primary"):
        #     resultado = calculadora.calcular(
        #         vencimento=venc, 
        #         ad_desempenho=ad, 
        #         carga_horaria=ch, 
        #         horas=hr
        #     )
            
        #     st.success(f"**Resultado:** {FormatadorCampos.brl(resultado.valor)}")
            
        #     with st.expander("Ver memória de cálculo", expanded=True):
        #         # O Streamlit renderiza legal listas formatadas
        #         for linha in resultado.memoria_calculo:
        #             st.code(linha)