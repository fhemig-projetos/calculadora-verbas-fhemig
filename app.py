import streamlit as st

# ─── CONFIGURAÇÃO DA PÁGINA ───────────────────────────────────────────────────

st.set_page_config(
    page_title="Calculadora de Verbas — FHEMIG",
    page_icon="🏥",
    layout="centered",
)

# ─── ESTILO CUSTOMIZADO ───────────────────────────────────────────────────────

st.markdown("""
<style>
    .block-container { padding-top: 2rem; max-width: 760px; }
    .titulo-verba { font-size: 1.05rem; font-weight: 700; color: #1a3a5c; }
    .descricao-verba { font-size: 0.82rem; color: #64748b; margin-top: 2px; margin-bottom: 16px; }
    .memoria-box {
        background: #f0f4f8;
        border-left: 3px solid #2563a8;
        padding: 12px 16px;
        border-radius: 0 6px 6px 0;
        font-family: monospace;
        font-size: 0.83rem;
        line-height: 1.8;
        white-space: pre-wrap;
    }
    hr { border: none; border-top: 1px solid #e2e8f0; margin: 1.2rem 0; }
</style>
""", unsafe_allow_html=True)

# ─── TABELAS INSS ─────────────────────────────────────────────────────────────

TABELA_INSS = {
    2026: [
        {"limite": 1621.00,   "aliq": 0.075, "deducao": 0.00},
        {"limite": 2902.84,   "aliq": 0.090, "deducao": 24.32},
        {"limite": 4354.27,   "aliq": 0.120, "deducao": 111.40},
        {"limite": 8475.55,   "aliq": 0.140, "deducao": 198.49},
    ],
    2025: [
        {"limite": 1518.00,   "aliq": 0.075, "deducao": 0.00},
        {"limite": 2793.88,   "aliq": 0.090, "deducao": 22.77},
        {"limite": 4190.83,   "aliq": 0.120, "deducao": 106.59},
        {"limite": 8157.41,   "aliq": 0.140, "deducao": 190.40},
    ],
    2024: [
        {"limite": 1412.00,   "aliq": 0.075, "deducao": 0.00},
        {"limite": 2666.68,   "aliq": 0.090, "deducao": 21.18},
        {"limite": 4000.03,   "aliq": 0.120, "deducao": 101.18},
        {"limite": 7786.02,   "aliq": 0.140, "deducao": 181.18},
    ],
}

def calc_inss(base: float, ano: int) -> tuple[float, float]:
    """Retorna (valor_inss, aliquota_aplicada)."""
    tabela = TABELA_INSS.get(ano, TABELA_INSS[2026])
    for faixa in tabela:
        if base <= faixa["limite"]:
            return base * faixa["aliq"] - faixa["deducao"], faixa["aliq"]
    ultima = tabela[-1]
    return base * ultima["aliq"] - ultima["deducao"], ultima["aliq"]

# ─── UTILITÁRIO ───────────────────────────────────────────────────────────────

def brl(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ─── HEADER ───────────────────────────────────────────────────────────────────

st.markdown("## 🏥 Calculadora de Verbas Remuneratórias")
st.markdown("**FHEMIG · DIGEPE / CCPT** — Conferência de Resumos Funcionais")
st.markdown("<hr>", unsafe_allow_html=True)

# ─── SELEÇÃO DA VERBA ─────────────────────────────────────────────────────────

GRUPOS = {
    "Gratificações e Adicionais": [
        "Gratificação de Final de Semana",
        "Adicional Noturno",
        "Hora Extra",
    ],
    "13º Salário": [
        "13º Salário",
        "GIEFS — 13º Salário",
        "INSS sobre 13º Salário",
    ],
    "GIEFS": [
        "GIEFS — Dias",
        "GIEFS — Meses (parcelas)",
        "GIEFS — 1/3 de Férias",
    ],
    "GRS": [
        "GRS — Dias",
        "GRS — Meses",
        "GRS — Desconto de Horas",
    ],
    "Férias": [
        "1/3 de Férias",
        "Férias Indenizadas",
    ],
    "Descontos e Outros": [
        "Faltas — Horas (desconto)",
        "Faltas — Dias (desconto)",
        "Ajuda de Custo Mensal",
        "Desconto de Custeio (4%)",
        "Aumento Salarial (4,62%)",
        "Desconto de IPSEMG (3,2%)",
        "INSS Mensal (tabela progressiva)",
    ],
}

todas_verbas = ["— Selecione uma verba —"]
for grupo, verbas in GRUPOS.items():
    for v in verbas:
        todas_verbas.append(v)

st.markdown("### 1. Selecione a verba")
verba = st.selectbox("Verba", todas_verbas, label_visibility="collapsed")

if verba == "— Selecione uma verba —":
    st.info("Selecione uma verba acima para exibir os campos de cálculo.")
    st.stop()

st.markdown("<hr>", unsafe_allow_html=True)

# ─── CAMPOS E CÁLCULO POR VERBA ───────────────────────────────────────────────

st.markdown("### 2. Preencha os dados")

resultado = None
memoria   = []

# ── Gratificação de Final de Semana ──────────────────────────────────────────
if verba == "Gratificação de Final de Semana":
    st.markdown('<div class="descricao-verba">Fórmula: (Venc. Básico + Ad. Desempenho) ÷ Carga Horária × Horas Realizadas × 1,0833</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    vb = c1.number_input("Vencimento Básico (R$)", min_value=0.0, step=0.01, format="%.2f")
    ad = c2.number_input("Adicional de Desempenho (R$)", min_value=0.0, step=0.01, format="%.2f")
    c3, c4 = st.columns(2)
    ch = c3.number_input("Carga Horária Mensal (h)", min_value=1.0, value=240.0, step=1.0, format="%.0f")
    hr = c4.number_input("Horas de Final de Semana Realizadas", min_value=0.0, step=1.0, format="%.0f")
    if st.button("Calcular", type="primary", use_container_width=True):
        base = vb + ad
        resultado = (base / ch) * hr * (13 / 12)
        memoria = [
            f"Base (Venc + Ad. Desempenho): {brl(base)}",
            f"Valor/hora: {brl(base)} ÷ {ch:.0f}h = {brl(base/ch)}",
            f"× {hr:.0f} horas × fator 1,0833 (13/12)",
            f"= {brl(resultado)}",
        ]

# ── Adicional Noturno ─────────────────────────────────────────────────────────
elif verba == "Adicional Noturno":
    st.markdown('<div class="descricao-verba">Fórmula: Venc. Básico ÷ Carga Horária × Horas Noturnas × 0,20</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    vb = c1.number_input("Vencimento Básico (R$)", min_value=0.0, step=0.01, format="%.2f")
    ch = c2.number_input("Carga Horária Mensal (h)", min_value=1.0, value=240.0, step=1.0, format="%.0f")
    hr = c3.number_input("Horas Noturnas (22h–5h)", min_value=0.0, step=1.0, format="%.0f")
    if st.button("Calcular", type="primary", use_container_width=True):
        valor_hora = vb / ch
        resultado = valor_hora * hr * 0.20
        memoria = [
            f"Valor/hora: {brl(vb)} ÷ {ch:.0f}h = {brl(valor_hora)}",
            f"Adicional noturno (20%): {brl(valor_hora * 0.20)}/h",
            f"× {hr:.0f} horas noturnas",
            f"= {brl(resultado)}",
        ]

# ── Hora Extra ────────────────────────────────────────────────────────────────
elif verba == "Hora Extra":
    st.markdown('<div class="descricao-verba">Fórmula: (Venc. Básico + Ad. Desempenho) ÷ Carga Horária × Horas × 1,50</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    vb = c1.number_input("Vencimento Básico (R$)", min_value=0.0, step=0.01, format="%.2f")
    ad = c2.number_input("Adicional de Desempenho (R$)", min_value=0.0, step=0.01, format="%.2f")
    c3, c4 = st.columns(2)
    ch = c3.number_input("Carga Horária Mensal (h)", min_value=1.0, value=240.0, step=1.0, format="%.0f")
    hr = c4.number_input("Quantidade de Horas Extras", min_value=0.0, step=1.0, format="%.0f")
    if st.button("Calcular", type="primary", use_container_width=True):
        base = vb + ad
        resultado = (base / ch) * hr * 1.5
        memoria = [
            f"Base: {brl(base)}",
            f"Valor/hora: {brl(base/ch)}",
            f"× {hr:.0f} horas × fator 1,50",
            f"= {brl(resultado)}",
        ]

# ── 13º Salário ───────────────────────────────────────────────────────────────
elif verba == "13º Salário":
    st.markdown('<div class="descricao-verba">Fórmula: (Venc + Ad. Desempenho + Ab. Emergência + Grat. Fim Semana + Ad. Noturno + GRS) ÷ 12 × Nº Meses</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    vb  = c1.number_input("Vencimento Básico (R$)",       min_value=0.0, step=0.01, format="%.2f")
    ad  = c2.number_input("Adicional de Desempenho (R$)", min_value=0.0, step=0.01, format="%.2f")
    ae  = c3.number_input("Abono de Emergência (R$)",     min_value=0.0, step=0.01, format="%.2f")
    c4, c5, c6 = st.columns(3)
    gfs = c4.number_input("Grat. Final de Semana (R$)",   min_value=0.0, step=0.01, format="%.2f")
    an  = c5.number_input("Adicional Noturno (R$)",       min_value=0.0, step=0.01, format="%.2f")
    grs = c6.number_input("GRS (R$)",                     min_value=0.0, step=0.01, format="%.2f")
    mm  = st.number_input("Nº de Meses de Direito (1–12)", min_value=1, max_value=12, value=12, step=1)
    if st.button("Calcular", type="primary", use_container_width=True):
        base = vb + ad + ae + gfs + an + grs
        resultado = (base / 12) * mm
        memoria = [
            f"Venc. Básico:        {brl(vb)}",
            f"Ad. Desempenho:      {brl(ad)}",
            f"Ab. Emergência:      {brl(ae)}",
            f"Grat. Fim Semana:    {brl(gfs)}",
            f"Ad. Noturno:         {brl(an)}",
            f"GRS:                 {brl(grs)}",
            f"─────────────────────────────",
            f"TOTAL BASE:          {brl(base)}",
            f"÷ 12 × {mm} meses",
            f"= {brl(resultado)}",
        ]

# ── GIEFS — 13º Salário ───────────────────────────────────────────────────────
elif verba == "GIEFS — 13º Salário":
    st.markdown('<div class="descricao-verba">Fórmula: Valor base ÷ 12 × Nº de Parcelas</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    base = c1.number_input("Valor base (R$)", min_value=0.0, step=0.01, format="%.2f")
    parc = c2.number_input("Nº de Parcelas a Receber", min_value=1, max_value=12, value=12, step=1)
    if st.button("Calcular", type="primary", use_container_width=True):
        resultado = (base / 12) * parc
        memoria = [
            f"{brl(base)} ÷ 12 = {brl(base/12)} por parcela",
            f"× {parc} parcelas",
            f"= {brl(resultado)}",
        ]

# ── INSS sobre 13º Salário ────────────────────────────────────────────────────
elif verba == "INSS sobre 13º Salário":
    st.markdown('<div class="descricao-verba">Tabela progressiva INSS aplicada sobre (13º Salário + GIEFS do 13º)</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    dec   = c1.number_input("Valor do 13º Salário (R$)", min_value=0.0, step=0.01, format="%.2f")
    giefs = c2.number_input("GIEFS do 13º (R$)",         min_value=0.0, step=0.01, format="%.2f")
    ano   = c3.selectbox("Ano de Referência", [2026, 2025, 2024])
    if st.button("Calcular", type="primary", use_container_width=True):
        base_calc = dec + giefs
        valor_inss, aliq = calc_inss(base_calc, ano)
        resultado = valor_inss
        memoria = [
            f"13º Salário:   {brl(dec)}",
            f"GIEFS 13º:     {brl(giefs)}",
            f"Base INSS:     {brl(base_calc)}",
            f"Alíquota ({ano}): {aliq*100:.1f}%",
            f"= {brl(resultado)}",
        ]

# ── GIEFS — Dias ──────────────────────────────────────────────────────────────
elif verba == "GIEFS — Dias":
    st.markdown('<div class="descricao-verba">Fórmula: Valor base ÷ 30 × Nº de Dias</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    base = c1.number_input("Valor base (R$)", min_value=0.0, step=0.01, format="%.2f")
    dias = c2.number_input("Nº de Dias", min_value=1, max_value=30, value=1, step=1)
    if st.button("Calcular", type="primary", use_container_width=True):
        resultado = (base / 30) * dias
        memoria = [
            f"{brl(base)} ÷ 30 dias = {brl(base/30)}/dia",
            f"× {dias} dias",
            f"= {brl(resultado)}",
        ]

# ── GIEFS — Meses ─────────────────────────────────────────────────────────────
elif verba == "GIEFS — Meses (parcelas)":
    st.markdown('<div class="descricao-verba">Fórmula: Valor base ÷ 6 × Nº de Parcelas</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    base = c1.number_input("Valor base (R$)", min_value=0.0, step=0.01, format="%.2f")
    parc = c2.number_input("Nº de Parcelas a Receber", min_value=1, max_value=6, value=1, step=1)
    if st.button("Calcular", type="primary", use_container_width=True):
        resultado = (base / 6) * parc
        memoria = [
            f"{brl(base)} ÷ 6 = {brl(base/6)} por parcela",
            f"× {parc} parcelas",
            f"= {brl(resultado)}",
        ]

# ── GIEFS — 1/3 de Férias ─────────────────────────────────────────────────────
elif verba == "GIEFS — 1/3 de Férias":
    st.markdown('<div class="descricao-verba">Fórmula: Valor base ÷ 3</div>', unsafe_allow_html=True)
    base = st.number_input("Valor base (R$)", min_value=0.0, step=0.01, format="%.2f")
    if st.button("Calcular", type="primary", use_container_width=True):
        resultado = base / 3
        memoria = [
            f"{brl(base)} ÷ 3",
            f"= {brl(resultado)}",
        ]

# ── GRS — Dias ────────────────────────────────────────────────────────────────
elif verba == "GRS — Dias":
    st.markdown('<div class="descricao-verba">Fórmula: GRS ÷ 30 × Nº de Dias</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    grs  = c1.number_input("Valor da GRS (R$)", min_value=0.0, step=0.01, format="%.2f")
    dias = c2.number_input("Nº de Dias", min_value=1, max_value=30, value=1, step=1)
    if st.button("Calcular", type="primary", use_container_width=True):
        resultado = (grs / 30) * dias
        memoria = [
            f"GRS/dia: {brl(grs)} ÷ 30 = {brl(grs/30)}",
            f"× {dias} dias",
            f"= {brl(resultado)}",
        ]

# ── GRS — Meses ───────────────────────────────────────────────────────────────
elif verba == "GRS — Meses":
    st.markdown('<div class="descricao-verba">Fórmula: GRS × Nº de Meses</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    grs   = c1.number_input("Valor da GRS (R$)", min_value=0.0, step=0.01, format="%.2f")
    meses = c2.number_input("Nº de Meses", min_value=1, max_value=12, value=1, step=1)
    if st.button("Calcular", type="primary", use_container_width=True):
        resultado = grs * meses
        memoria = [
            f"{brl(grs)} × {meses} meses",
            f"= {brl(resultado)}",
        ]

# ── GRS — Desconto de Horas ───────────────────────────────────────────────────
elif verba == "GRS — Desconto de Horas":
    st.markdown('<div class="descricao-verba">Fórmula: GRS ÷ Carga Horária × Horas de Falta</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    grs = c1.number_input("Valor da GRS (R$)",      min_value=0.0, step=0.01, format="%.2f")
    ch  = c2.number_input("Carga Horária Mensal (h)", min_value=1.0, value=240.0, step=1.0, format="%.0f")
    hf  = c3.number_input("Horas de Falta",          min_value=0.0, step=1.0, format="%.0f")
    if st.button("Calcular", type="primary", use_container_width=True):
        resultado = (grs / ch) * hf
        memoria = [
            f"GRS/hora: {brl(grs)} ÷ {ch:.0f}h = {brl(grs/ch)}",
            f"× {hf:.0f} horas de falta",
            f"= {brl(resultado)}",
        ]

# ── 1/3 de Férias ─────────────────────────────────────────────────────────────
elif verba == "1/3 de Férias":
    st.markdown('<div class="descricao-verba">Fórmula: (Salário + Ab. Emergência + Ad. Desempenho + Ad. Noturno + GRS) ÷ 3</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    sal = c1.number_input("Salário (R$)",                  min_value=0.0, step=0.01, format="%.2f")
    ae  = c2.number_input("Abono de Emergência (R$)",      min_value=0.0, step=0.01, format="%.2f")
    ad  = c3.number_input("Adicional de Desempenho (R$)",  min_value=0.0, step=0.01, format="%.2f")
    c4, c5 = st.columns(2)
    an  = c4.number_input("Adicional Noturno (R$)",        min_value=0.0, step=0.01, format="%.2f")
    grs = c5.number_input("GRS (R$)",                      min_value=0.0, step=0.01, format="%.2f")
    if st.button("Calcular", type="primary", use_container_width=True):
        base = sal + ae + ad + an + grs
        resultado = base / 3
        memoria = [
            f"Salário:          {brl(sal)}",
            f"Ab. Emergência:   {brl(ae)}",
            f"Ad. Desempenho:   {brl(ad)}",
            f"Ad. Noturno:      {brl(an)}",
            f"GRS:              {brl(grs)}",
            f"──────────────────────────",
            f"BASE:             {brl(base)}",
            f"÷ 3",
            f"= {brl(resultado)}",
        ]

# ── Férias Indenizadas ────────────────────────────────────────────────────────
elif verba == "Férias Indenizadas":
    st.markdown('<div class="descricao-verba">Fórmula: (Salário + GIEFS + Ab. Emergência + GRS + Ad. Noturno) ÷ 30 × Nº de Dias</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    sal  = c1.number_input("Salário (R$)",             min_value=0.0, step=0.01, format="%.2f")
    gie  = c2.number_input("GIEFS (R$)",               min_value=0.0, step=0.01, format="%.2f")
    ae   = c3.number_input("Abono de Emergência (R$)", min_value=0.0, step=0.01, format="%.2f")
    c4, c5, c6 = st.columns(3)
    grs  = c4.number_input("GRS (R$)",                 min_value=0.0, step=0.01, format="%.2f")
    an   = c5.number_input("Adicional Noturno (R$)",   min_value=0.0, step=0.01, format="%.2f")
    dias = c6.number_input("Nº de Dias de Férias",     min_value=1, max_value=30, value=30, step=1)
    if st.button("Calcular", type="primary", use_container_width=True):
        base = sal + gie + ae + grs + an
        resultado = (base / 30) * dias
        memoria = [
            f"Salário:          {brl(sal)}",
            f"GIEFS:            {brl(gie)}",
            f"Ab. Emergência:   {brl(ae)}",
            f"GRS:              {brl(grs)}",
            f"Ad. Noturno:      {brl(an)}",
            f"──────────────────────────",
            f"BASE:             {brl(base)}",
            f"÷ 30 × {dias} dias",
            f"= {brl(resultado)}",
        ]

# ── Faltas — Horas ────────────────────────────────────────────────────────────
elif verba == "Faltas — Horas (desconto)":
    st.markdown('<div class="descricao-verba">Fórmula: (Venc + Ad. Desempenho + Ab. Emergência + GRS) ÷ Carga Horária × Horas de Falta</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    vb  = c1.number_input("Vencimento Básico (R$)",       min_value=0.0, step=0.01, format="%.2f")
    ad  = c2.number_input("Adicional de Desempenho (R$)", min_value=0.0, step=0.01, format="%.2f")
    ae  = c3.number_input("Abono de Emergência (R$)",     min_value=0.0, step=0.01, format="%.2f")
    c4, c5, c6 = st.columns(3)
    grs = c4.number_input("GRS (R$)",                     min_value=0.0, step=0.01, format="%.2f")
    ch  = c5.number_input("Carga Horária Mensal (h)",     min_value=1.0, value=240.0, step=1.0, format="%.0f")
    hf  = c6.number_input("Horas de Falta",               min_value=0.0, step=1.0, format="%.0f")
    if st.button("Calcular", type="primary", use_container_width=True):
        base = vb + ad + ae + grs
        resultado = (base / ch) * hf
        memoria = [
            f"Base: {brl(base)}",
            f"Valor/hora: {brl(base/ch)}",
            f"× {hf:.0f} horas de falta",
            f"= {brl(resultado)}",
        ]

# ── Faltas — Dias ─────────────────────────────────────────────────────────────
elif verba == "Faltas — Dias (desconto)":
    st.markdown('<div class="descricao-verba">Fórmula: (Venc + Ad. Desempenho + Ab. Emergência + GRS) ÷ 30 × Dias de Falta</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    vb   = c1.number_input("Vencimento Básico (R$)",       min_value=0.0, step=0.01, format="%.2f")
    ad   = c2.number_input("Adicional de Desempenho (R$)", min_value=0.0, step=0.01, format="%.2f")
    ae   = c3.number_input("Abono de Emergência (R$)",     min_value=0.0, step=0.01, format="%.2f")
    c4, c5 = st.columns(2)
    grs  = c4.number_input("GRS (R$)",                     min_value=0.0, step=0.01, format="%.2f")
    dias = c5.number_input("Dias de Falta",                min_value=1, max_value=30, value=1, step=1)
    if st.button("Calcular", type="primary", use_container_width=True):
        base = vb + ad + ae + grs
        resultado = (base / 30) * dias
        memoria = [
            f"Base: {brl(base)}",
            f"÷ 30 × {dias} dias de falta",
            f"= {brl(resultado)}",
        ]

# ── Ajuda de Custo Mensal ─────────────────────────────────────────────────────
elif verba == "Ajuda de Custo Mensal":
    st.markdown('<div class="descricao-verba">Fórmula: Valor Diário × Quantidade de Dias ou Plantões</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    vd   = c1.number_input("Valor Diário (R$)",               min_value=0.0, step=0.01, format="%.2f")
    dias = c2.number_input("Quantidade de Dias ou Plantões",   min_value=1, value=1, step=1)
    if st.button("Calcular", type="primary", use_container_width=True):
        resultado = vd * dias
        memoria = [
            f"{brl(vd)} × {dias} dias/plantões",
            f"= {brl(resultado)}",
        ]

# ── Desconto de Custeio ───────────────────────────────────────────────────────
elif verba == "Desconto de Custeio (4%)":
    st.markdown('<div class="descricao-verba">Fórmula: Valor que gerou o desconto × 4%</div>', unsafe_allow_html=True)
    base = st.number_input("Valor que gerou o desconto (R$)", min_value=0.0, step=0.01, format="%.2f")
    if st.button("Calcular", type="primary", use_container_width=True):
        resultado = base * 0.04
        memoria = [
            f"{brl(base)} × 4%",
            f"= {brl(resultado)}",
        ]

# ── Aumento Salarial ──────────────────────────────────────────────────────────
elif verba == "Aumento Salarial (4,62%)":
    st.markdown('<div class="descricao-verba">Fórmula: Valor atual × 4,62%</div>', unsafe_allow_html=True)
    base = st.number_input("Valor que sofrerá o aumento (R$)", min_value=0.0, step=0.01, format="%.2f")
    if st.button("Calcular", type="primary", use_container_width=True):
        aumento = base * 0.0462
        resultado = aumento
        memoria = [
            f"{brl(base)} × 4,62%",
            f"Aumento:    {brl(aumento)}",
            f"Novo valor: {brl(base + aumento)}",
        ]

# ── IPSEMG ────────────────────────────────────────────────────────────────────
elif verba == "Desconto de IPSEMG (3,2%)":
    st.markdown('<div class="descricao-verba">Fórmula: Base de incidência × 3,2%</div>', unsafe_allow_html=True)
    base = st.number_input("Valor a sofrer incidência de IPSEMG (R$)", min_value=0.0, step=0.01, format="%.2f")
    if st.button("Calcular", type="primary", use_container_width=True):
        resultado = base * 0.032
        memoria = [
            f"{brl(base)} × 3,2%",
            f"= {brl(resultado)}",
        ]

# ── INSS Mensal ───────────────────────────────────────────────────────────────
elif verba == "INSS Mensal (tabela progressiva)":
    st.markdown('<div class="descricao-verba">Cálculo progressivo conforme tabela INSS do ano de referência</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    base = c1.number_input("Base de cálculo (R$)", min_value=0.0, step=0.01, format="%.2f")
    ano  = c2.selectbox("Ano de Referência", [2026, 2025, 2024])
    if st.button("Calcular", type="primary", use_container_width=True):
        valor_inss, aliq = calc_inss(base, ano)
        resultado = valor_inss
        tab = TABELA_INSS[ano]
        memoria = [
            f"Base: {brl(base)} | Ano: {ano}",
            f"Tabela INSS {ano}:",
        ] + [
            f"  até {brl(f['limite'])}: {f['aliq']*100:.1f}%"
            for f in tab
        ] + [
            f"Alíquota aplicada: {aliq*100:.1f}%",
            f"= {brl(resultado)}",
        ]

# ─── EXIBIÇÃO DO RESULTADO ────────────────────────────────────────────────────

if resultado is not None:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### Resultado")
    st.metric(label=verba, value=brl(resultado))

    if memoria:
        with st.expander("Ver memória de cálculo"):
            st.markdown(
                '<div class="memoria-box">' +
                "\n".join(memoria) +
                '</div>',
                unsafe_allow_html=True
            )

    # ── Comparador ───────────────────────────────────────────────────────────
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 3. Conferência")
    st.caption("Compare o valor calculado com o informado pela unidade no Resumo Funcional.")

    c1, c2 = st.columns([3, 1])
    val_unidade = c1.number_input(
        "Valor informado pela unidade (R$)",
        min_value=0.0, step=0.01, format="%.2f",
        key="val_unidade"
    )
    conferir = c2.button("Conferir", use_container_width=True)

    if conferir and val_unidade > 0:
        diferenca = abs(val_unidade - resultado)
        if diferenca < 0.05:
            st.success(
                f"✅ **Valores conferem.**  \n"
                f"Calculado: **{brl(resultado)}** | Informado: **{brl(val_unidade)}**"
            )
        else:
            sinal = "a mais" if val_unidade > resultado else "a menos"
            st.error(
                f"❌ **Divergência de {brl(diferenca)} ({sinal}).**  \n"
                f"Calculado: **{brl(resultado)}** | Informado: **{brl(val_unidade)}**"
            )
