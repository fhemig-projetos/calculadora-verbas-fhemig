CONFIG_CAMPOS = {
    "vencimento_basico":       {"label": "Vencimento Básico (R$)", "tipo": "moeda"},
    "carga_horaria_mensal":    {"label": "Carga Horária Mensal (h/mês)", "tipo": "hora_mensal"},
    "horas_realizadas": {"label": "Horas Realizadas", "tipo": "horas_realizadas"},
    "ano_referencia":   {"label": "Ano de Referência", "tipo": "ano"},
    "ano_referencia_aumento": {
        "label": "Ano de Referência",
        "tipo": "ano",
        "help": (
            "Aplica, em sequência (composto), todas as alíquotas do ano de referência em diante. "
            "Em 2024 aplica as alíquotas de 2024 e 2026; em 2026 aplica só a de 2026. "
            "Resultado = valor reajustado − Venc. Básico."
        ),
    },
    "valor_grs": {
        "label": "GRS (R$)",
        "tipo": "moeda",
        "help": "Risco Médio: R$ 160,20 · Risco Alto: R$ 320,40 (valores 2026) · Se não fizer jus, deixe R$ 0,00.",
    },
    "dias_trabalhados": {"label": "Nº de Dias Trabalhados no Mês", "tipo": "dias"},
    "abono_emergencia": {"label": "Abono de Emergência (R$)", "tipo": "moeda"},
    "grat_final_semana": {"label": "Grat. Final de Semana (R$)", "tipo": "moeda"},
    "adicional_noturno": {"label": "Adicional Noturno (R$)", "tipo": "moeda"},
    "numero_meses": {"label": "Nº de Meses de Direito", "tipo": "meses"},
    "valor_giefs": {"label": "Valor da GIEFS (R$)", "tipo": "moeda"},
    "valor_piso": {
        "label": "Valor do Piso (R$)",
        "tipo": "moeda",
        "help": (
            "Pré-preenchido apenas para PENF nível II e IV (contratados) com CH 30 ou 40, "
            "conforme o cargo informado no cabeçalho. Nos demais cargos, informe manualmente."
        ),
    },
    "dias_ferias_indenizadas": {"label": "Nº de Dias de Férias Indenizadas", "tipo": "dias"},
    "faltas_horas": {"label": "Nº de Horas de Faltas", "tipo": "horas"},
    "faltas_dias": {"label": "Nº de Dias de Faltas", "tipo": "dias"},
    "ajuda_custo_fixa_diario": {"label": "Valor Diário da Ajuda de Custo Fixa (R$)", "tipo": "moeda"},
    "ajuda_custo_variavel_diario": {"label": "Valor Diário da Ajuda de Custo Variável (R$)", "tipo": "moeda"},
    "valor_ajuda_custo": {"label": "Valor da Ajuda de Custo (R$)", "tipo": "moeda"},
    "valor_13_salario":  {"label": "Valor do 13º Salário (R$)", "tipo": "moeda"},
    "giefs_13_salario":  {"label": "Valor da GIEFS do 13º (R$)", "tipo": "moeda"},
    "valor_outras_vantagens": {"label": "Outras Vantagens (soma automática do histórico) (R$)", "tipo": "moeda"},
    "outras_verbas": {"label": "Outras Verbas (R$)", "tipo": "moeda"},
    "valor_pmc": {"label": "Valor do PMC (R$)", "tipo": "moeda"},
    "valor_auxilio_transporte": {"label": "Valor do Auxílio Transporte (R$)", "tipo": "moeda"},
    "valor_ipsemg_filho": {"label": "Valor do Desconto IPSEMG Filho 21 a 39 anos (R$)", "tipo": "moeda"},
}
