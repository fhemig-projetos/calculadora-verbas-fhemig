import streamlit as st
from data import ProvedorDadosFhemig
from calculadoras import CalculadoraVerba, REGISTRO_CALCULADORAS
from utils import CONFIG_CAMPOS, FormatadorCampos

class SelecaoVerba:

    def __init__(self):
        if "historico" not in st.session_state:
            st.session_state["historico"] = []

        if "ultimo_resultado" not in st.session_state:
            st.session_state["ultimo_resultado"] = {}

    def render(self):
        verbas_json = ProvedorDadosFhemig.obter_verbas()
        nomes_verbas = list(verbas_json.keys())

        st.markdown("### 1. Selecione a verba")
        opcoes = ["— Selecione uma verba —"] + nomes_verbas
        verba_input   = st.selectbox(
            "Verba",
            options=opcoes,
            label_visibility="collapsed"
        )

        if verba_input == "— Selecione uma verba —":
            st.info("Selecione uma verba acima para exibir os campos de cálculo.")
            return
        
        st.divider()

        # Seleciona a verba e passa os metadados correspondentes
        st.markdown("### 2. Preencha os dados")
        verba_meta = verbas_json[verba_input]

        if verba_meta["tipo"] == "Vantagem":
            tipo_tag = (
            '<span style="background:#e6f5ee;color:#1a7f4b;padding:2px 10px;'
            'border-radius:20px;font-size:0.75rem;font-weight:700;">VANTAGEM</span>'
            ) # Sintaxe para concatenar string
        else:
            tipo_tag = (
            '<span style="background:#fef2f2;color:#b91c1c;padding:2px 10px;'
            'border-radius:20px;font-size:0.75rem;font-weight:700;">DESCONTO</span>'
        )

        st.markdown(f'**Verba {verba_meta["codigo"]}** &nbsp; {tipo_tag}', unsafe_allow_html=True)
        
        # Verifica se existe calculadora correspondente
        calculadora = REGISTRO_CALCULADORAS.get(verba_input)
        if calculadora: 
            self._render_calculadora(calculadora, verba_meta)

    def _render_calculadora(self, calculadora: CalculadoraVerba, verba_meta: dict):
        # Exibe a fórmula
        st.caption(calculadora.descricao_formula)

        # Pega valores default preenchidos no cabeçalho
        ds = st.session_state.get("dados_servidor", {})

        # Gera os campos dinamicamente
        valores = {}
        cols = st.columns(2)

        for i, campo in enumerate(calculadora.campos_necessarios):
            config = CONFIG_CAMPOS.get(campo)

            if campo == "vencimento_basico":
                valor_default = ds.get("vencimento_basico")
            elif campo == "ad_desempenho":
                valor_default = 0.0
            elif campo == "carga_horaria_mensal":
                valor_default = ds.get("ch_mensal")
            elif campo == "horas_realizadas":
                valor_default = 0
            else:
                valor_default = 0
            
            desabilitado = campo in ("vencimento_basico", "carga_horaria_mensal")
            desabilitado = False

            with cols[i % 2]:
                    valores[campo] = st.number_input(
                        config["label"],
                        value=valor_default,
                        disabled=desabilitado,
                    )

        if st.button("Calcular", type="primary", use_container_width=True):
            resultado = calculadora.calcular(**valores)

            st.session_state["ultimo_resultado"] = {
                "verba": verba_meta,
                "valor": resultado.valor,
                "memoria": resultado.memoria_calculo,
            }

            self._exibir_resultado()

    def _exibir_resultado(self):
        ur = st.session_state["ultimo_resultado"]

        st.divider()
        st.markdown("### Resultado")
        st.metric(label="Resultado", value=FormatadorCampos.brl(ur["valor"]), label_visibility="collapsed")

        with st.expander("Ver memória de cálculo"):
            texto_memoria = "\n".join(ur["memoria"])
            st.code(texto_memoria, language="text")