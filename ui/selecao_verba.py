import streamlit as st
from data import ProvedorDadosFhemig
from calculadoras import CalculadoraVerba, REGISTRO_CALCULADORAS
from utils import FormatadorCampos, GeradorPDF
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

        # Guarda o último valor digitado em cada campo, entre trocas de verba
        if "valores_digitados" not in st.session_state:
            st.session_state["valores_digitados"] = {}

        # Guarda a última "assinatura" do cabeçalho vista, para detectar troca de servidor
        if "ultima_referencia_cabecalho" not in st.session_state:
            st.session_state["ultima_referencia_cabecalho"] = None

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
        Detecta troca de verba: se a verba escolhida agora é diferente da última
        selecionada, faz dois ajustes de estado:
        1. Limpa "ultimo_resultado" — some o resultado (e tudo que depende dele:
            competência, observação, botão "Adicionar à lista") da tela, já que
            pertence ao cálculo da verba anterior.
        2. Incrementa "verba_nonce" — esse número entra na `key` de todos os
            campos (`f"{nonce}::{campo}"`), fazendo o Streamlit tratá-los como
            widgets "novos" e reaplicar o `value=valor_default` (histórico/
            persistido/cabeçalho), em vez de manter o valor antigo que estava
            guardado na `key` da verba anterior.
        Só entra aqui na troca de verba (não em todo rerun) — por isso a comparação
        com "ultima_verba_selecionada" antes de agir.
        """
        if st.session_state.get("ultima_verba_selecionada") != verba_input:
            st.session_state["ultimo_resultado"] = None
            if "verba_nonce" not in st.session_state:
                st.session_state["verba_nonce"] = 0
            st.session_state["verba_nonce"] += 1
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

        # Nonce da verba atual
        nonce = st.session_state.get("verba_nonce", 0)

        # Atalho para o dicionário persistente
        persistidos = st.session_state["valores_digitados"]

        # Gera os campos dinamicamente
        valores = {}
        cols = st.columns(2)

        """
        Se vencimento/ch_mensal do cabeçalho mudarem (novo servidor), limpa o valor
        persistido desses campos e bump no verba_nonce para recriar as `key`s dos
        widgets — assim o cabeçalho novo "irradia" para os campos, e a partir daí
        o usuário pode editá-los livremente até a próxima troca de servidor.
        """
        referencia_cabecalho = (ds.get("vencimento_basico"), ds.get("ch_mensal"))
        if st.session_state["ultima_referencia_cabecalho"] is not None and st.session_state["ultima_referencia_cabecalho"] != referencia_cabecalho:
            for campo_cabecalho in ("vencimento_basico", "carga_horaria_mensal", "valor_base_aumento"):
                persistidos.pop(campo_cabecalho, None)
            st.session_state["verba_nonce"] = st.session_state.get("verba_nonce", 0) + 1
            nonce = st.session_state["verba_nonce"]  # atualiza a variável já usada nas keys abaixo
        st.session_state["ultima_referencia_cabecalho"] = referencia_cabecalho

        for i, campo in enumerate(calculadora.campos_necessarios):
            config = CONFIG_CAMPOS.get(campo)

            # Define os valores default para cada campo
            ## Campos do Cabeçalho → default do cabeçalho, mas persiste o que digitei
            if campo == "vencimento_basico":
                valor_default = persistidos.get(campo, ds.get("vencimento_basico"))
            elif campo == "carga_horaria_mensal":
                valor_default = persistidos.get(campo, ds.get("ch_mensal"))
                opcoes_ch = [120, 180, 240, 264]
                indice_default = opcoes_ch.index(valor_default) if valor_default in opcoes_ch else 0
            elif campo == "valor_base_aumento":
                valor_default = persistidos.get(campo, ds.get("vencimento_basico"))
            ## Campos de selectbox → índice vem do persistido (se a opção existir)
            elif campo == "ano_referencia":
                opcoes_ano = [2024, 2026] if nome_verba == "Aumento Salarial" else [2024, 2025, 2026]
                valor_persistido = persistidos.get(campo)
                if valor_persistido in opcoes_ano:
                    ano_default = valor_persistido
                else:
                    ano_default = date.today().year if date.today().year in opcoes_ano else opcoes_ano[-1]
                indice_default_ano = opcoes_ano.index(ano_default)
            elif campo == "grs_risco":
                if nome_verba in ["GRS — Dias", "GRS — Meses", "GRS — 13º Salário", "GRS — Desconto de Horas"]:
                    opcoes_grs = ["Risco Médio (R$ 160,20)", "Risco Alto (R$ 320,40)"]
                else:
                    opcoes_grs = ["Não faz jus (R$ 0,00)", "Risco Médio (R$ 160,20)", "Risco Alto (R$ 320,40)"]
                valor_persistido = persistidos.get(campo)
                indice_default_grs = opcoes_grs.index(valor_persistido) if valor_persistido in opcoes_grs else 0
            ## Campos do Histórico → histórico primeiro, persistido como fallback
            elif campo in ("grat_final_semana", "adicional_noturno", "valor_13_salario",
                        "giefs_13_salario", "valor_ajuda_custo"):
                nome_alvo_dict = { ## tentar melhorar essa lógica depois para ficar mais eficiente
                    "grat_final_semana": "Gratificação de Final de Semana",
                    "adicional_noturno": "Adicional Noturno",
                    "valor_13_salario": "13º Salário",
                    "giefs_13_salario": "GIEFS — 13º Salário",
                    "valor_ajuda_custo": "Ajuda de Custo Mensal",
                }
                nome_alvo = nome_alvo_dict[campo]
                historico = st.session_state.get("historico", [])
                for item in reversed(historico):
                    if item.get("nome_verba") == nome_alvo:
                        valor_default = item["valor"]
                        break # quebra o loop quando encontrar correspondência na tabela do histórico
                else:
                    valor_default = persistidos.get(campo, 0.0)
            # Demais manuais → persistido, com default puro
            elif campo == "ajuda_custo_diario":
                valor_default = persistidos.get(campo, 75.0)
            elif campo in ("dias_trabalhados", "numero_meses", "dias_ferias_indenizadas", "faltas_horas", "faltas_dias"):
                valor_default = persistidos.get(campo, 1)
            else:  # ad_desempenho, horas_realizadas, abono_emergencia, valor_giefs, valor_piso, etc.
                if config["tipo"] == "moeda":
                    valor_default = persistidos.get(campo, 0.0)
                else:
                    valor_default = persistidos.get(campo, 0)

            # Renderiza os campos
            ## Se campo == "ad_desempenho", desabilitado == True
            desabilitado = campo in ("ad_desempenho",)

            ## Chave sempre com nonce: widget "novo" a cada troca de verba
            campo_key = f"{nonce}::{campo}"

            with cols[i % 2]:
                if campo == "ano_referencia":
                    valores[campo] = st.selectbox(
                        config["label"],
                        options=opcoes_ano,
                        index=indice_default_ano,
                        key=campo_key,
                    )
                elif campo == "grs_risco":
                    valores[campo] = st.selectbox(
                        config["label"],
                        options=opcoes_grs,
                        index=indice_default_grs,
                        key=campo_key,
                    )
                elif campo == "carga_horaria_mensal":
                    valores[campo] = st.selectbox(
                        config["label"],
                        options=opcoes_ch, # [120, 180, 240, 264]
                        index=indice_default, # já vem pré-selecionado de acordo com o cabeçalho
                        key=campo_key,
                    )
                elif campo in ("dias_trabalhados", "dias_ferias_indenizadas", "faltas_dias"):
                    valores[campo] = st.number_input(
                        config["label"],
                        value=valor_default,
                        min_value=1,
                        max_value=30,
                        key=campo_key,
                    )
                elif campo == "numero_meses":
                    valores[campo] = st.number_input(
                        config["label"],
                        value=valor_default,
                        min_value=1,
                        max_value=12,
                        key=campo_key,
                    )
                elif campo == "faltas_horas":
                    valores[campo] = st.number_input(
                        config["label"],
                        value=valor_default,
                        key=campo_key,
                    )
                else: # vencimento_basico, ad_desempenho, carga_horaria_mensal, horas_realizadas, etc.
                    valores[campo] = st.number_input(
                            config["label"],
                            value=valor_default,
                            disabled=desabilitado,
                            key=campo_key,
                        )

            # Persiste o valor atual (menos os campos que sempre vêm do cabeçalho)
            persistidos[campo] = valores[campo]

        if st.button("Calcular", type="primary", use_container_width=True):
            resultado = calculadora.calcular(**valores)

            # Se for Aumento Salarial, inclui o ano no nome p/ diferenciar no histórico
            nome_verba_historico = nome_verba
            if nome_verba == "Aumento Salarial":
                nome_verba_historico = f"{nome_verba} ({valores['ano_referencia']})"

            st.session_state["ultimo_resultado"] = {
                "nome_verba": nome_verba_historico,
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

        # Renderiza os campos correspondentes e retorna a competência e a observação
        competencia = self._render_competencia(ur["nome_verba"])
        observacao = self._render_observacao()

        if st.button("➕ Adicionar à lista", type="secondary", use_container_width=True):
            st.session_state["historico"].append({
                "nome_verba": ur["nome_verba"],
                "codigo": ur["codigo"],
                "tipo": ur["tipo"],
                "valor": ur["valor"],
                "memoria": ur["memoria"],
                "competencia": competencia,
                "observacao": observacao
            })
            st.rerun()

    def _render_competencia(self, nome_verba: str):
        st.divider()
        st.markdown("#### 📅 Competência")

        if nome_verba in (
            "13º Salário",
            "GIEFS — 13º Salário",
            "Piso Enfermagem — 13º Salário",
            "GRS — 13º Salário",
            "INSS sobre 13º Salário",
        ):
            # Apenas ano
            st.caption("Selecione o ano de referência do cálculo")
            hoje = date.today()
            ano = st.selectbox("Ano", options=range(2000, 2031), index=hoje.year - 2000)
            competencia = str(ano)
            return competencia
        else: 
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

    def _render_observacao(self): 
        st.divider()
        st.markdown("#### 📝 Observação")
        observacao = st.text_area(
            "Observação (opcional)",
            max_chars=200,
            placeholder="Ex: Verba calculada com base no mês de competência...",
            label_visibility="collapsed",
        )
        st.caption(f"{len(observacao)}/200 caracteres")
        return observacao

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
                "Observação": item.get("observacao"), 
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

        # Botões de ação sobre a lista (remover / limpar / gerar PDF)
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            if st.button("🗑️ Remover último", type="secondary", use_container_width=True):
                st.session_state["historico"].pop()
                st.rerun()
        with col_btn2:
            if st.button("🗑️ Limpar lista", type="secondary", use_container_width=True):
                st.session_state["historico"] = []
                st.rerun()
        with col_btn3:
            ds = st.session_state.get("dados_servidor", {})
            masp = FormatadorCampos.masp(ds.get("masp")) or "servidor"
            nome_arquivo = f"verbas_{masp}_{date.today().strftime('%d%m%Y')}.pdf"
            st.download_button(
                "📄 Gerar PDF",
                data=GeradorPDF(historico, ds).gerar(),
                file_name=nome_arquivo,
                mime="application/pdf",
                type="primary",
                use_container_width=True,
            )