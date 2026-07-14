import streamlit as st
from data import ProvedorDadosFhemig
from calculadoras import CalculadoraVerba, REGISTRO_CALCULADORAS
from utils import FormatadorCampos
from datetime import date 
from .config import CONFIG_CAMPOS

class SelecaoVerba:

    def __init__(self):
        if "historico" not in st.session_state:
            st.session_state["historico"] = []

        if "ultimo_resultado" not in st.session_state:
            st.session_state["ultimo_resultado"] = None

        if "ultima_verba_selecionada" not in st.session_state:
            st.session_state["ultima_verba_selecionada"] = None

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
            # Persistir a tabela do histórico (mesmo quando não tiver verba selecionada)
            self._render_historico()
            return

        st.divider()

        """
        SE a última verba que eu calculei é DIFERENTE da verba que está no selectbox AGORA:
            ENTÃO:
                1. Apaga o resultado atual (some da tela) 
                2. Anota que agora a "última verba" é esta nova
        > 1. Apaga o resultado por conta de `if ur is None` em self._render_resultado().
        > 2. Precisa anotar para ativar a lógica do if p/ limpar a tela só quando troca a verba (se fosse só ultimo_resultado = None, sem o if, por exemplo iria limpar a tela assim que clicasse em `Calcular` e nunca iria exibir o histórico).
        > OBS: O histórico continua sendo renderizado, pq _render_historico() está fora do por conta de `if ur is None` em self._render_resultado() `if calculadora`.
        """

        if st.session_state.get("ultima_verba_selecionada") != verba_input:
            st.session_state["ultimo_resultado"] = None
            st.session_state["ultima_verba_selecionada"] = verba_input

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
            self._render_calculadora(calculadora, verba_meta, verba_input)

        # Fica fora do if p/ persistir a tabela do histórico (mesmo se não encontrar calculadora ou quando trocar de verba)
        self._render_historico()

    def _render_calculadora(self, calculadora: CalculadoraVerba, verba_meta: dict, nome_verba: str):
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
            elif campo == "ano_referencia":
                valor_default = date.today().year
            else:
                valor_default = 0

            desabilitado = campo in ("vencimento_basico", "carga_horaria_mensal")
            desabilitado = False

            with cols[i % 2]:
                if campo == "ano_referencia":
                    valores[campo] = st.selectbox(
                        config["label"],
                        options=[2024, 2025, 2026],
                        index=valor_default - 2024,
                    )
                else:
                    valores[campo] = st.number_input(
                            config["label"],
                            value=100,
                            #value=valor_default,
                            disabled=desabilitado,
                        )

        if st.button("Calcular", type="primary", use_container_width=True):
            resultado = calculadora.calcular(**valores)

            st.session_state["ultimo_resultado"] = {
                "nome_verba": nome_verba,
                "codigo": verba_meta["codigo"],
                "tipo": verba_meta["tipo"],
                "valor": resultado.valor,
                "memoria": resultado.memoria_calculo,
            }
        # Fica fora do if p/ persistir o resultado mesmo se clicar em outro campo (rerender do streamlit)
        self._render_resultado()

    def _render_resultado(self):
        ur = st.session_state["ultimo_resultado"]

        # Limpa a renderização do resultado e tudo depois dele
        if ur is None:
            return

        st.divider()
        st.markdown("### Resultado")
        st.metric(label="Resultado", value=FormatadorCampos.brl(ur["valor"]), label_visibility="collapsed")

        with st.expander("Ver memória de cálculo", expanded=True):
            texto_memoria = "\n".join(ur["memoria"])
            st.code(texto_memoria, language="text")

        # Renderiza os campos correspondentes e retorna a competência
        competencia = self._render_competencia()

        if st.button("➕ Adicionar à lista", type="secondary", use_container_width=True):
            st.session_state["historico"].append({
                "nome_verba": ur["nome_verba"],
                "codigo": ur["codigo"],
                "tipo": ur["tipo"],
                "valor": ur["valor"],
                "memoria": ur["memoria"],
                "competencia": competencia
            })
            st.rerun()

            print(f"historico: {st.session_state["historico"]}")

    def _render_competencia(self):
        st.divider()
        st.markdown("#### 📅 Competência")
        st.caption("Selecione o mês/ano de referência do cálculo")

        # Lógica para buscar mês anterior e ano atual como default
        hoje = date.today()
        if hoje.month == 1:
            mes_default, ano_default = 12, hoje.year - 1
        else:
            mes_default, ano_default = hoje.month - 1, hoje.year

        # Competência do cálculo (mês/ano)
        col_mes, col_ano = st.columns(2)
        mes = col_mes.selectbox("Mês", options=range(1, 13), format_func=lambda m: f"{m:02d}", index=mes_default - 1)
        ano = col_ano.selectbox("Ano", options=range(2000, 2031), index=ano_default - 2000)
        competencia = f"{mes:02d}/{ano}"

        return competencia

    def _render_historico(self):
        historico = st.session_state.get("historico")

        if not historico:
            return

        st.divider()
        st.markdown("### Lista de cálculos realizados")

        # Monta o dataframe c/ os itens
        dados = []
        for item in historico:
            dados.append({
                "Verba": item.get("nome_verba"),
                "Código": item.get("codigo"),
                "Tipo": item.get("tipo"),
                "Competência": item.get("competencia"),
                "Valor (R$)": FormatadorCampos.brl(item["valor"]),
            })

        st.dataframe(dados, width="stretch", hide_index=True)

        # Exibe totais separados
        vantagens = sum(item["valor"] for item in historico if item.get("tipo") == "Vantagem")
        descontos = sum(item["valor"] for item in historico if item.get("tipo") == "Desconto")
        liquido = vantagens - descontos

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Vantagens", FormatadorCampos.brl(vantagens))
        col2.metric("Total Descontos", FormatadorCampos.brl(descontos))
        col3.metric("Líquido", FormatadorCampos.brl(liquido))

        # Botões de limpar o dataframe
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🗑️ Remover último", type="secondary", use_container_width=True):
                st.session_state["historico"].pop()
                st.rerun()
        with col_btn2:
            if st.button("🗑️ Limpar lista", type="secondary", use_container_width=True):
                st.session_state["historico"] = []
                st.rerun()
