import streamlit as st
import io
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# ─── CONFIGURAÇÃO DA PÁGINA ───────────────────────────────────────────────────

st.set_page_config(
    page_title="Calculadora de Verbas — FHEMIG",
    page_icon="🏥",
    layout="centered",
)

st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; max-width: 800px; }
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
    .tag-vantagem { background:#e6f5ee; color:#1a7f4b; padding:2px 10px; border-radius:20px; font-size:0.75rem; font-weight:700; }
    .tag-desconto { background:#fef2f2; color:#b91c1c; padding:2px 10px; border-radius:20px; font-size:0.75rem; font-weight:700; }
    hr { border: none; border-top: 1px solid #e2e8f0; margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)

# ─── TABELA DE CARGOS ─────────────────────────────────────────────────────────

TABELA_CARGOS = [
    {"classe": "PENF", "nivel": "2", "grau": "A", "ch_semanal": "40 Horas Semanais", "ch_mensal": 240, "vencimento": 2138.08, "dt_inicio": "01/01/2026"},
    {"classe": "PENF", "nivel": "4", "grau": "A", "ch_semanal": "40 Horas Semanais", "ch_mensal": 240, "vencimento": 4204.52, "dt_inicio": "01/01/2026"},
    {"classe": "TOS",  "nivel": "1", "grau": "A", "ch_semanal": "40 Horas Semanais", "ch_mensal": 240, "vencimento": 1732.73, "dt_inicio": "01/01/2026"},
    {"classe": "AGAS", "nivel": "1", "grau": "A", "ch_semanal": "40 Horas Semanais", "ch_mensal": 240, "vencimento": 4204.52, "dt_inicio": "01/01/2026"},
]

def buscar_cargo(classe, nivel, grau):
    """Retorna o registro de cargo ou None se não encontrado."""
    for c in TABELA_CARGOS:
        if (c["classe"].upper() == classe.upper() and
            c["nivel"] == str(nivel) and
            c["grau"].upper() == grau.upper()):
            return c
    return None

# ─── TABELAS INSS ─────────────────────────────────────────────────────────────

TABELA_INSS = {
    2026: [
        {"limite": 1621.00, "aliq": 0.075, "deducao": 0.00},
        {"limite": 2902.84, "aliq": 0.090, "deducao": 24.32},
        {"limite": 4354.27, "aliq": 0.120, "deducao": 111.40},
        {"limite": 8475.55, "aliq": 0.140, "deducao": 198.49},
    ],
    2025: [
        {"limite": 1518.00, "aliq": 0.075, "deducao": 0.00},
        {"limite": 2793.88, "aliq": 0.090, "deducao": 22.77},
        {"limite": 4190.83, "aliq": 0.120, "deducao": 106.59},
        {"limite": 8157.41, "aliq": 0.140, "deducao": 190.40},
    ],
    2024: [
        {"limite": 1412.00, "aliq": 0.075, "deducao": 0.00},
        {"limite": 2666.68, "aliq": 0.090, "deducao": 21.18},
        {"limite": 4000.03, "aliq": 0.120, "deducao": 101.18},
        {"limite": 7786.02, "aliq": 0.140, "deducao": 181.18},
    ],
}

def calc_inss(base: float, ano: int):
    tabela = TABELA_INSS.get(ano, TABELA_INSS[2026])
    for faixa in tabela:
        if base <= faixa["limite"]:
            return base * faixa["aliq"] - faixa["deducao"], faixa["aliq"]
    ultima = tabela[-1]
    return base * ultima["aliq"] - ultima["deducao"], ultima["aliq"]

# ─── METADADOS DAS VERBAS ─────────────────────────────────────────────────────

VERBAS_META = {
    "Gratificação de Final de Semana": {"codigo": "2416", "tipo": "Vantagem"},
    "Adicional Noturno":               {"codigo": "2411", "tipo": "Vantagem"},
    "Hora Extra":                      {"codigo": "2412", "tipo": "Vantagem"},
    "13º Salário":                     {"codigo": "2491", "tipo": "Vantagem"},
    "GIEFS — 13º Salário":             {"codigo": "3171", "tipo": "Vantagem"},
    "INSS sobre 13º Salário":          {"codigo": "7708", "tipo": "Desconto"},
    "GIEFS — Dias":                    {"codigo": "2417", "tipo": "Vantagem"},
    "GIEFS — Meses (parcelas)":        {"codigo": "2417", "tipo": "Vantagem"},
    "GIEFS — 1/3 de Férias":           {"codigo": "3242", "tipo": "Vantagem"},
    "GRS — Dias":                      {"codigo": "2420", "tipo": "Vantagem"},
    "GRS — Meses":                     {"codigo": "2420", "tipo": "Vantagem"},
    "GRS — Desconto de Horas":         {"codigo": "7820", "tipo": "Desconto"},
    "1/3 de Férias":                   {"codigo": "2431", "tipo": "Vantagem"},
    "Férias Indenizadas":              {"codigo": "2432", "tipo": "Vantagem"},
    "Faltas — Horas (desconto)":       {"codigo": "7810", "tipo": "Desconto"},
    "Faltas — Dias (desconto)":        {"codigo": "7811", "tipo": "Desconto"},
    "Ajuda de Custo Mensal":           {"codigo": "2070", "tipo": "Vantagem"},
    "Desconto de Custeio (4%)":        {"codigo": "9018", "tipo": "Desconto"},
    "Aumento Salarial (4,62%)":        {"codigo": "----", "tipo": "Vantagem"},
    "Desconto de IPSEMG (3,2%)":       {"codigo": "7700", "tipo": "Desconto"},
    "INSS Mensal (tabela progressiva)":{"codigo": "7808", "tipo": "Desconto"},
}

# ─── UTILITÁRIOS ──────────────────────────────────────────────────────────────

def brl(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def brl_num(valor: float) -> str:
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ─── SESSION STATE ────────────────────────────────────────────────────────────

if "historico" not in st.session_state:
    st.session_state.historico = []

if "ultimo_resultado" not in st.session_state:
    st.session_state.ultimo_resultado = None  # {"verba", "codigo", "tipo", "valor", "memoria"}


if "dados_servidor" not in st.session_state:
    st.session_state.dados_servidor = {
        "nome": "", "masp": "", "admissao": "1",
        "dt_admissao": "", "dt_fim_efetiva": "",
        "cargo_classe": "", "cargo_nivel": "", "cargo_grau": "",
        "ch_semanal": "", "ch_mensal": 0.0, "vencimento": 0.0,
    }

# ─── GERAÇÃO DE PDF ───────────────────────────────────────────────────────────

def gerar_pdf(historico, ds) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=1.8*cm, rightMargin=1.8*cm,
        topMargin=1.8*cm, bottomMargin=1.8*cm,
    )
    styles = getSampleStyleSheet()
    azul   = colors.HexColor("#1a3a5c")
    azul2  = colors.HexColor("#2563a8")
    cinza  = colors.HexColor("#f0f4f8")
    verm   = colors.HexColor("#b91c1c")
    verde  = colors.HexColor("#1a7f4b")

    titulo_style = ParagraphStyle("titulo", fontSize=13, textColor=azul,
                                   fontName="Helvetica-Bold", spaceAfter=2,
                                   alignment=TA_CENTER)
    sub_style    = ParagraphStyle("sub", fontSize=8, textColor=colors.HexColor("#64748b"),
                                   spaceAfter=10, alignment=TA_CENTER)
    label_style  = ParagraphStyle("label", fontSize=7, textColor=colors.HexColor("#64748b"),
                                   fontName="Helvetica-Bold", leading=10)
    valor_style  = ParagraphStyle("valor", fontSize=9, textColor=azul,
                                   fontName="Helvetica-Bold", leading=12)
    cell_style   = ParagraphStyle("cell", fontSize=8, leading=11)

    story = []

    # Cabeçalho
    story.append(Paragraph("FHEMIG — Calculadora de Verbas Remuneratórias", titulo_style))
    story.append(Paragraph("DIGEPE / CCPT · Conferência de Resumos Funcionais", sub_style))

    # Dados do servidor
    def campo_pdf(label, valor):
        return [Paragraph(label, label_style), Paragraph(str(valor) if valor else "—", valor_style)]

    dados_tabela = [
        ["Nome do Servidor", ds["nome"] or "—",           "MASP",            ds["masp"] or "—"],
        ["Admissão",         ds["admissao"] or "—",        "Data Admissão",   ds["dt_admissao"] or "—"],
        ["Data Fim Efetiva", ds["dt_fim_efetiva"] or "—", "",                ""],
        ["Cargo / Classe",   ds["cargo_classe"] or "—",   "Nível",           ds["cargo_nivel"] or "—"],
        ["Grau",             ds["cargo_grau"] or "—",     "C.H. Semanal",    ds["ch_semanal"] or "—"],
        ["C.H. Mensal (h)",  f'{ds["ch_mensal"]:.0f}h' if ds["ch_mensal"] else "—",
         "Vencimento Básico", brl(ds["vencimento"]) if ds["vencimento"] else "—"],
    ]

    col_w = [3.2*cm, 5.8*cm, 3.2*cm, 5.8*cm]
    t_dados = Table(dados_tabela, colWidths=col_w)
    t_dados.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (0,-1), cinza),
        ("BACKGROUND",  (2,0), (2,-1), cinza),
        ("FONTNAME",    (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME",    (2,0), (2,-1), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,-1), 8),
        ("TEXTCOLOR",   (0,0), (0,-1), colors.HexColor("#64748b")),
        ("TEXTCOLOR",   (2,0), (2,-1), colors.HexColor("#64748b")),
        ("TEXTCOLOR",   (1,0), (1,-1), azul),
        ("TEXTCOLOR",   (3,0), (3,-1), azul),
        ("FONTNAME",    (1,0), (1,-1), "Helvetica-Bold"),
        ("FONTNAME",    (3,0), (3,-1), "Helvetica-Bold"),
        ("GRID",        (0,0), (-1,-1), 0.4, colors.HexColor("#d1d9e0")),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [colors.white, colors.white]),
        ("TOPPADDING",  (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(t_dados)
    story.append(Spacer(1, 0.4*cm))

    # Tabela de verbas
    cabecalho = ["Código", "Descrição da Verba", "Tipo", "Mês/Ano Ref.", "Valor (R$)"]
    linhas = [cabecalho]
    total_vantagens = 0.0
    total_descontos = 0.0

    for h in historico:
        tipo = h["tipo"]
        cor_tipo = verde if tipo == "Vantagem" else verm
        linhas.append([
            h["codigo"],
            h["verba"],
            Paragraph(f'<font color="{cor_tipo.hexval()}">{tipo}</font>', cell_style),
            h["referencia"],
            brl_num(h["valor"]),
        ])
        if tipo == "Vantagem":
            total_vantagens += h["valor"]
        else:
            total_descontos += h["valor"]

    # Totais
    linhas.append(["", "TOTAL VANTAGENS", "", "", brl_num(total_vantagens)])
    linhas.append(["", "TOTAL DESCONTOS", "", "", brl_num(total_descontos)])
    linhas.append(["", "LÍQUIDO (Vantagens − Descontos)", "", "", brl_num(total_vantagens - total_descontos)])

    col_w2 = [1.5*cm, 7.0*cm, 2.2*cm, 2.5*cm, 2.8*cm]
    t_verbas = Table(linhas, colWidths=col_w2, repeatRows=1)
    n = len(linhas)
    t_verbas.setStyle(TableStyle([
        # Cabeçalho
        ("BACKGROUND",   (0,0), (-1,0),  azul2),
        ("TEXTCOLOR",    (0,0), (-1,0),  colors.white),
        ("FONTNAME",     (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 8),
        ("ALIGN",        (4,0), (4,-1),  "RIGHT"),
        ("ALIGN",        (0,0), (0,-1),  "CENTER"),
        ("ALIGN",        (2,0), (2,-1),  "CENTER"),
        ("GRID",         (0,0), (-1,n-4), 0.4, colors.HexColor("#d1d9e0")),
        ("ROWBACKGROUNDS",(0,1),(-1,n-4),[colors.white, cinza]),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        # Linhas de total
        ("LINEABOVE",    (0, n-3), (-1, n-3), 1, azul),
        ("FONTNAME",     (1, n-3), (1, n-1), "Helvetica-Bold"),
        ("FONTNAME",     (4, n-3), (4, n-1), "Helvetica-Bold"),
        ("TEXTCOLOR",    (1, n-3), (-1, n-3), verde),
        ("TEXTCOLOR",    (1, n-2), (-1, n-2), verm),
        ("TEXTCOLOR",    (1, n-1), (-1, n-1), azul),
        ("BACKGROUND",   (0, n-1), (-1, n-1), colors.HexColor("#e8f0f9")),
    ]))
    story.append(t_verbas)

    # Rodapé
    story.append(Spacer(1, 0.5*cm))
    rodape = ParagraphStyle("rodape", fontSize=7, textColor=colors.HexColor("#94a3b8"),
                             alignment=TA_CENTER)
    story.append(Paragraph(
        f"Gerado em {date.today().strftime('%d/%m/%Y')} · FHEMIG / DIGEPE · CCPT",
        rodape
    ))

    doc.build(story)
    return buf.getvalue()

# ═══════════════════════════════════════════════════════════════════════════════
# INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("## 🏥 Calculadora de Verbas Remuneratórias")
st.markdown("**FHEMIG · DIGEPE / CCPT** — Conferência de Resumos Funcionais")
st.markdown("<hr>", unsafe_allow_html=True)

# ─── SEÇÃO 1: DADOS DO SERVIDOR ───────────────────────────────────────────────

with st.expander("📋 Dados do Servidor (cabeçalho do PDF)", expanded=True):
    ds = st.session_state.dados_servidor

    c1, c2, c3 = st.columns(3)
    ds["nome"]           = c1.text_input("Nome Completo do Servidor", value=ds["nome"])
    ds["masp"]           = c2.text_input("MASP", value=ds["masp"])
    ds["admissao"]       = c3.text_input("Admissão", value=ds["admissao"], help="Ex: 1, 2")

    c4, c5 = st.columns(2)
    ds["dt_admissao"]    = c4.text_input("Data de Admissão", value=ds["dt_admissao"], placeholder="DD/MM/AAAA")
    ds["dt_fim_efetiva"] = c5.text_input("Data Fim Efetiva",  value=ds["dt_fim_efetiva"], placeholder="DD/MM/AAAA")

    st.markdown("<hr style='margin:0.6rem 0'>", unsafe_allow_html=True)
    st.caption("**Cargo** — preencha para busca automática do vencimento e carga horária")

    c6, c7, c8 = st.columns(3)
    cargo_classe = c6.text_input("Cargo / Classe", value=ds["cargo_classe"], placeholder="Ex: PENF").upper().strip()
    cargo_nivel  = c7.text_input("Nível",          value=ds["cargo_nivel"],  placeholder="Ex: 2").strip()
    cargo_grau   = c8.text_input("Grau",           value=ds["cargo_grau"],   placeholder="Ex: A").upper().strip()

    # Busca automática
    cargo_encontrado = None
    if cargo_classe and cargo_nivel and cargo_grau:
        cargo_encontrado = buscar_cargo(cargo_classe, cargo_nivel, cargo_grau)

    if cargo_encontrado:
        st.success(
            f"✅ Cargo encontrado · Vencimento: **{brl(cargo_encontrado['vencimento'])}** · "
            f"C.H. Semanal: **{cargo_encontrado['ch_semanal']}** · "
            f"C.H. Mensal: **{cargo_encontrado['ch_mensal']}h** · "
            f"Vigência: **{cargo_encontrado['dt_inicio']}**"
        )
        ds["cargo_classe"] = cargo_classe
        ds["cargo_nivel"]  = cargo_nivel
        ds["cargo_grau"]   = cargo_grau
        ds["ch_semanal"]   = cargo_encontrado["ch_semanal"]
        ds["ch_mensal"]    = float(cargo_encontrado["ch_mensal"])
        ds["vencimento"]   = cargo_encontrado["vencimento"]
    else:
        if cargo_classe and cargo_nivel and cargo_grau:
            st.warning("⚠️ Cargo não encontrado na tabela. Preencha manualmente abaixo.")
        ds["cargo_classe"] = cargo_classe
        ds["cargo_nivel"]  = cargo_nivel
        ds["cargo_grau"]   = cargo_grau

        c9, c10, c11 = st.columns(3)
        ds["ch_semanal"]  = c9.text_input("C.H. Semanal",    value=ds.get("ch_semanal",""), placeholder="Ex: 40 Horas Semanais")
        ds["ch_mensal"]   = c10.number_input("C.H. Mensal (h)", value=ds.get("ch_mensal", 0.0), min_value=0.0, step=1.0, format="%.0f")
        ds["vencimento"]  = c11.number_input("Vencimento Básico (R$)", value=ds.get("vencimento", 0.0), min_value=0.0, step=0.01, format="%.2f")

# Atalhos para uso nos campos de verba
_vb_default = float(ds["vencimento"])
_ch_default = float(ds["ch_mensal"]) if ds["ch_mensal"] else 240.0

st.markdown("<hr>", unsafe_allow_html=True)

# ─── SEÇÃO 2: SELEÇÃO DA VERBA ────────────────────────────────────────────────

GRUPOS = {
    "Gratificações e Adicionais": ["Gratificação de Final de Semana","Adicional Noturno","Hora Extra"],
    "13º Salário":                ["13º Salário","GIEFS — 13º Salário","INSS sobre 13º Salário"],
    "GIEFS":                      ["GIEFS — Dias","GIEFS — Meses (parcelas)","GIEFS — 1/3 de Férias"],
    "GRS":                        ["GRS — Dias","GRS — Meses","GRS — Desconto de Horas"],
    "Férias":                     ["1/3 de Férias","Férias Indenizadas"],
    "Descontos e Outros":         ["Faltas — Horas (desconto)","Faltas — Dias (desconto)",
                                   "Ajuda de Custo Mensal","Desconto de Custeio (4%)",
                                   "Aumento Salarial (4,62%)","Desconto de IPSEMG (3,2%)",
                                   "INSS Mensal (tabela progressiva)"],
}

todas_verbas = ["— Selecione uma verba —"]
for verbas in GRUPOS.values():
    todas_verbas.extend(verbas)

st.markdown("### 1. Selecione a verba")
verba = st.selectbox("Verba", todas_verbas, label_visibility="collapsed")

if verba == "— Selecione uma verba —":
    st.info("Selecione uma verba acima para exibir os campos de cálculo.")
else:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 2. Preencha os dados")

    meta = VERBAS_META.get(verba, {"codigo": "----", "tipo": "Vantagem"})
    tipo_tag = f'<span class="tag-vantagem">VANTAGEM</span>' if meta["tipo"] == "Vantagem" else f'<span class="tag-desconto">DESCONTO</span>'
    st.markdown(f'**Verba {meta["codigo"]}** &nbsp; {tipo_tag}', unsafe_allow_html=True)

    resultado = None
    memoria   = []

    # ── Gratificação de Final de Semana ──────────────────────────────────────
    if verba == "Gratificação de Final de Semana":
        st.markdown('<div class="descricao-verba">Fórmula: (Venc. Básico + Ad. Desempenho) ÷ Carga Horária × Horas Realizadas × 1,0833</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        vb = c1.number_input("Vencimento Básico (R$)", value=_vb_default, min_value=0.0, step=0.01, format="%.2f")
        ad = c2.number_input("Adicional de Desempenho (R$)", min_value=0.0, step=0.01, format="%.2f")
        c3, c4 = st.columns(2)
        ch = c3.number_input("Carga Horária Mensal (h)", value=_ch_default, min_value=1.0, step=1.0, format="%.0f")
        hr = c4.number_input("Horas de Final de Semana Realizadas", min_value=0.0, step=1.0, format="%.0f")
        if st.button("Calcular", type="primary", use_container_width=True):
            base = vb + ad
            resultado = (base / ch) * hr * (13/12)
            memoria = [f"Base (Venc + Ad. Desempenho): {brl(base)}",
                       f"Valor/hora: {brl(base/ch)}",
                       f"× {hr:.0f} horas × fator 1,0833 (13/12)",
                       f"= {brl(resultado)}"]

    elif verba == "Adicional Noturno":
        st.markdown('<div class="descricao-verba">Fórmula: Venc. Básico ÷ Carga Horária × Horas Noturnas × 0,20</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        vb = c1.number_input("Vencimento Básico (R$)", value=_vb_default, min_value=0.0, step=0.01, format="%.2f")
        ch = c2.number_input("Carga Horária Mensal (h)", value=_ch_default, min_value=1.0, step=1.0, format="%.0f")
        hr = c3.number_input("Horas Noturnas (22h–5h)", min_value=0.0, step=1.0, format="%.0f")
        if st.button("Calcular", type="primary", use_container_width=True):
            vh = vb / ch
            resultado = vh * hr * 0.20
            memoria = [f"Valor/hora: {brl(vh)}", f"Adicional 20%: {brl(vh*0.20)}/h",
                       f"× {hr:.0f} horas noturnas", f"= {brl(resultado)}"]

    elif verba == "Hora Extra":
        st.markdown('<div class="descricao-verba">Fórmula: (Venc. Básico + Ad. Desempenho) ÷ Carga Horária × Horas × 1,50</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        vb = c1.number_input("Vencimento Básico (R$)", value=_vb_default, min_value=0.0, step=0.01, format="%.2f")
        ad = c2.number_input("Adicional de Desempenho (R$)", min_value=0.0, step=0.01, format="%.2f")
        c3, c4 = st.columns(2)
        ch = c3.number_input("Carga Horária Mensal (h)", value=_ch_default, min_value=1.0, step=1.0, format="%.0f")
        hr = c4.number_input("Quantidade de Horas Extras", min_value=0.0, step=1.0, format="%.0f")
        if st.button("Calcular", type="primary", use_container_width=True):
            base = vb + ad
            resultado = (base / ch) * hr * 1.5
            memoria = [f"Base: {brl(base)}", f"Valor/hora: {brl(base/ch)}",
                       f"× {hr:.0f} horas × 1,50", f"= {brl(resultado)}"]

    elif verba == "13º Salário":
        st.markdown('<div class="descricao-verba">Fórmula: (Venc + Ad. Desempenho + Ab. Emergência + Grat. Fim Semana + Ad. Noturno + GRS) ÷ 12 × Nº Meses</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        vb  = c1.number_input("Vencimento Básico (R$)", value=_vb_default, min_value=0.0, step=0.01, format="%.2f")
        ad  = c2.number_input("Adicional de Desempenho (R$)", min_value=0.0, step=0.01, format="%.2f")
        ae  = c3.number_input("Abono de Emergência (R$)", min_value=0.0, step=0.01, format="%.2f")
        c4, c5, c6 = st.columns(3)
        gfs = c4.number_input("Grat. Final de Semana (R$)", min_value=0.0, step=0.01, format="%.2f")
        an  = c5.number_input("Adicional Noturno (R$)", min_value=0.0, step=0.01, format="%.2f")
        grs = c6.number_input("GRS (R$)", min_value=0.0, step=0.01, format="%.2f")
        mm  = st.number_input("Nº de Meses de Direito (1–12)", min_value=1, max_value=12, value=12, step=1)
        if st.button("Calcular", type="primary", use_container_width=True):
            base = vb + ad + ae + gfs + an + grs
            resultado = (base / 12) * mm
            memoria = [f"Venc. Básico: {brl(vb)}", f"Ad. Desempenho: {brl(ad)}",
                       f"Ab. Emergência: {brl(ae)}", f"Grat. Fim Semana: {brl(gfs)}",
                       f"Ad. Noturno: {brl(an)}", f"GRS: {brl(grs)}",
                       f"─────────────────────", f"BASE: {brl(base)}",
                       f"÷ 12 × {mm} meses", f"= {brl(resultado)}"]

    elif verba == "GIEFS — 13º Salário":
        st.markdown('<div class="descricao-verba">Fórmula: Valor base ÷ 12 × Nº de Parcelas</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        base = c1.number_input("Valor base (R$)", min_value=0.0, step=0.01, format="%.2f")
        parc = c2.number_input("Nº de Parcelas", min_value=1, max_value=12, value=12, step=1)
        if st.button("Calcular", type="primary", use_container_width=True):
            resultado = (base / 12) * parc
            memoria = [f"{brl(base)} ÷ 12 = {brl(base/12)}/parcela",
                       f"× {parc} parcelas", f"= {brl(resultado)}"]

    elif verba == "INSS sobre 13º Salário":
        st.markdown('<div class="descricao-verba">Tabela progressiva INSS sobre (13º Salário + GIEFS do 13º)</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        dec   = c1.number_input("Valor do 13º (R$)", min_value=0.0, step=0.01, format="%.2f")
        giefs = c2.number_input("GIEFS do 13º (R$)", min_value=0.0, step=0.01, format="%.2f")
        ano   = c3.selectbox("Ano de Referência", [2026, 2025, 2024])
        if st.button("Calcular", type="primary", use_container_width=True):
            base_c = dec + giefs
            resultado, aliq = calc_inss(base_c, ano)
            memoria = [f"13º: {brl(dec)}", f"GIEFS 13º: {brl(giefs)}",
                       f"Base INSS: {brl(base_c)}", f"Alíquota ({ano}): {aliq*100:.1f}%",
                       f"= {brl(resultado)}"]

    elif verba == "GIEFS — Dias":
        st.markdown('<div class="descricao-verba">Fórmula: Valor base ÷ 30 × Nº de Dias</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        base = c1.number_input("Valor base (R$)", min_value=0.0, step=0.01, format="%.2f")
        dias = c2.number_input("Nº de Dias", min_value=1, max_value=30, value=1, step=1)
        if st.button("Calcular", type="primary", use_container_width=True):
            resultado = (base / 30) * dias
            memoria = [f"{brl(base)} ÷ 30 = {brl(base/30)}/dia",
                       f"× {dias} dias", f"= {brl(resultado)}"]

    elif verba == "GIEFS — Meses (parcelas)":
        st.markdown('<div class="descricao-verba">Fórmula: Valor base ÷ 6 × Nº de Parcelas</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        base = c1.number_input("Valor base (R$)", min_value=0.0, step=0.01, format="%.2f")
        parc = c2.number_input("Nº de Parcelas", min_value=1, max_value=6, value=1, step=1)
        if st.button("Calcular", type="primary", use_container_width=True):
            resultado = (base / 6) * parc
            memoria = [f"{brl(base)} ÷ 6 = {brl(base/6)}/parcela",
                       f"× {parc} parcelas", f"= {brl(resultado)}"]

    elif verba == "GIEFS — 1/3 de Férias":
        st.markdown('<div class="descricao-verba">Fórmula: Valor base ÷ 3</div>', unsafe_allow_html=True)
        base = st.number_input("Valor base (R$)", min_value=0.0, step=0.01, format="%.2f")
        if st.button("Calcular", type="primary", use_container_width=True):
            resultado = base / 3
            memoria = [f"{brl(base)} ÷ 3", f"= {brl(resultado)}"]

    elif verba == "GRS — Dias":
        st.markdown('<div class="descricao-verba">Fórmula: GRS ÷ 30 × Nº de Dias</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        grs  = c1.number_input("Valor da GRS (R$)", min_value=0.0, step=0.01, format="%.2f")
        dias = c2.number_input("Nº de Dias", min_value=1, max_value=30, value=1, step=1)
        if st.button("Calcular", type="primary", use_container_width=True):
            resultado = (grs / 30) * dias
            memoria = [f"GRS/dia: {brl(grs/30)}", f"× {dias} dias", f"= {brl(resultado)}"]

    elif verba == "GRS — Meses":
        st.markdown('<div class="descricao-verba">Fórmula: GRS × Nº de Meses</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        grs   = c1.number_input("Valor da GRS (R$)", min_value=0.0, step=0.01, format="%.2f")
        meses = c2.number_input("Nº de Meses", min_value=1, max_value=12, value=1, step=1)
        if st.button("Calcular", type="primary", use_container_width=True):
            resultado = grs * meses
            memoria = [f"{brl(grs)} × {meses} meses", f"= {brl(resultado)}"]

    elif verba == "GRS — Desconto de Horas":
        st.markdown('<div class="descricao-verba">Fórmula: GRS ÷ Carga Horária × Horas de Falta</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        grs = c1.number_input("Valor da GRS (R$)", min_value=0.0, step=0.01, format="%.2f")
        ch  = c2.number_input("Carga Horária Mensal (h)", value=_ch_default, min_value=1.0, step=1.0, format="%.0f")
        hf  = c3.number_input("Horas de Falta", min_value=0.0, step=1.0, format="%.0f")
        if st.button("Calcular", type="primary", use_container_width=True):
            resultado = (grs / ch) * hf
            memoria = [f"GRS/hora: {brl(grs/ch)}", f"× {hf:.0f} horas", f"= {brl(resultado)}"]

    elif verba == "1/3 de Férias":
        st.markdown('<div class="descricao-verba">Fórmula: (Salário + Ab. Emergência + Ad. Desempenho + Ad. Noturno + GRS) ÷ 3</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        sal = c1.number_input("Salário (R$)", value=_vb_default, min_value=0.0, step=0.01, format="%.2f")
        ae  = c2.number_input("Abono de Emergência (R$)", min_value=0.0, step=0.01, format="%.2f")
        ad  = c3.number_input("Adicional de Desempenho (R$)", min_value=0.0, step=0.01, format="%.2f")
        c4, c5 = st.columns(2)
        an  = c4.number_input("Adicional Noturno (R$)", min_value=0.0, step=0.01, format="%.2f")
        grs = c5.number_input("GRS (R$)", min_value=0.0, step=0.01, format="%.2f")
        if st.button("Calcular", type="primary", use_container_width=True):
            base = sal + ae + ad + an + grs
            resultado = base / 3
            memoria = [f"Salário: {brl(sal)}", f"Ab. Emergência: {brl(ae)}",
                       f"Ad. Desempenho: {brl(ad)}", f"Ad. Noturno: {brl(an)}",
                       f"GRS: {brl(grs)}", f"─────────────────",
                       f"BASE: {brl(base)}", f"÷ 3", f"= {brl(resultado)}"]

    elif verba == "Férias Indenizadas":
        st.markdown('<div class="descricao-verba">Fórmula: (Salário + GIEFS + Ab. Emergência + GRS + Ad. Noturno) ÷ 30 × Nº de Dias</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        sal  = c1.number_input("Salário (R$)", value=_vb_default, min_value=0.0, step=0.01, format="%.2f")
        gie  = c2.number_input("GIEFS (R$)", min_value=0.0, step=0.01, format="%.2f")
        ae   = c3.number_input("Abono de Emergência (R$)", min_value=0.0, step=0.01, format="%.2f")
        c4, c5, c6 = st.columns(3)
        grs  = c4.number_input("GRS (R$)", min_value=0.0, step=0.01, format="%.2f")
        an   = c5.number_input("Adicional Noturno (R$)", min_value=0.0, step=0.01, format="%.2f")
        dias = c6.number_input("Nº de Dias de Férias", min_value=1, max_value=30, value=30, step=1)
        if st.button("Calcular", type="primary", use_container_width=True):
            base = sal + gie + ae + grs + an
            resultado = (base / 30) * dias
            memoria = [f"Salário: {brl(sal)}", f"GIEFS: {brl(gie)}",
                       f"Ab. Emergência: {brl(ae)}", f"GRS: {brl(grs)}",
                       f"Ad. Noturno: {brl(an)}", f"─────────────────",
                       f"BASE: {brl(base)}", f"÷ 30 × {dias} dias", f"= {brl(resultado)}"]

    elif verba == "Faltas — Horas (desconto)":
        st.markdown('<div class="descricao-verba">Fórmula: (Venc + Ad. Desempenho + Ab. Emergência + GRS) ÷ Carga Horária × Horas de Falta</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        vb  = c1.number_input("Vencimento Básico (R$)", value=_vb_default, min_value=0.0, step=0.01, format="%.2f")
        ad  = c2.number_input("Adicional de Desempenho (R$)", min_value=0.0, step=0.01, format="%.2f")
        ae  = c3.number_input("Abono de Emergência (R$)", min_value=0.0, step=0.01, format="%.2f")
        c4, c5, c6 = st.columns(3)
        grs = c4.number_input("GRS (R$)", min_value=0.0, step=0.01, format="%.2f")
        ch  = c5.number_input("Carga Horária Mensal (h)", value=_ch_default, min_value=1.0, step=1.0, format="%.0f")
        hf  = c6.number_input("Horas de Falta", min_value=0.0, step=1.0, format="%.0f")
        if st.button("Calcular", type="primary", use_container_width=True):
            base = vb + ad + ae + grs
            resultado = (base / ch) * hf
            memoria = [f"Base: {brl(base)}", f"Valor/hora: {brl(base/ch)}",
                       f"× {hf:.0f} horas de falta", f"= {brl(resultado)}"]

    elif verba == "Faltas — Dias (desconto)":
        st.markdown('<div class="descricao-verba">Fórmula: (Venc + Ad. Desempenho + Ab. Emergência + GRS) ÷ 30 × Dias de Falta</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        vb   = c1.number_input("Vencimento Básico (R$)", value=_vb_default, min_value=0.0, step=0.01, format="%.2f")
        ad   = c2.number_input("Adicional de Desempenho (R$)", min_value=0.0, step=0.01, format="%.2f")
        ae   = c3.number_input("Abono de Emergência (R$)", min_value=0.0, step=0.01, format="%.2f")
        c4, c5 = st.columns(2)
        grs  = c4.number_input("GRS (R$)", min_value=0.0, step=0.01, format="%.2f")
        dias = c5.number_input("Dias de Falta", min_value=1, max_value=30, value=1, step=1)
        if st.button("Calcular", type="primary", use_container_width=True):
            base = vb + ad + ae + grs
            resultado = (base / 30) * dias
            memoria = [f"Base: {brl(base)}", f"÷ 30 × {dias} dias de falta", f"= {brl(resultado)}"]

    elif verba == "Ajuda de Custo Mensal":
        st.markdown('<div class="descricao-verba">Fórmula: Valor Diário × Quantidade de Dias ou Plantões</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        vd   = c1.number_input("Valor Diário (R$)", min_value=0.0, step=0.01, format="%.2f")
        dias = c2.number_input("Quantidade de Dias ou Plantões", min_value=1, value=1, step=1)
        if st.button("Calcular", type="primary", use_container_width=True):
            resultado = vd * dias
            memoria = [f"{brl(vd)} × {dias} dias/plantões", f"= {brl(resultado)}"]

    elif verba == "Desconto de Custeio (4%)":
        st.markdown('<div class="descricao-verba">Fórmula: Valor que gerou o desconto × 4%</div>', unsafe_allow_html=True)
        base = st.number_input("Valor que gerou o desconto (R$)", min_value=0.0, step=0.01, format="%.2f")
        if st.button("Calcular", type="primary", use_container_width=True):
            resultado = base * 0.04
            memoria = [f"{brl(base)} × 4%", f"= {brl(resultado)}"]

    elif verba == "Aumento Salarial (4,62%)":
        st.markdown('<div class="descricao-verba">Fórmula: Valor atual × 4,62%</div>', unsafe_allow_html=True)
        base = st.number_input("Valor que sofrerá o aumento (R$)", min_value=0.0, step=0.01, format="%.2f")
        if st.button("Calcular", type="primary", use_container_width=True):
            aumento = base * 0.0462
            resultado = aumento
            memoria = [f"{brl(base)} × 4,62%",
                       f"Aumento: {brl(aumento)}", f"Novo valor: {brl(base + aumento)}"]

    elif verba == "Desconto de IPSEMG (3,2%)":
        st.markdown('<div class="descricao-verba">Fórmula: Base de incidência × 3,2%</div>', unsafe_allow_html=True)
        base = st.number_input("Valor a sofrer incidência de IPSEMG (R$)", min_value=0.0, step=0.01, format="%.2f")
        if st.button("Calcular", type="primary", use_container_width=True):
            resultado = base * 0.032
            memoria = [f"{brl(base)} × 3,2%", f"= {brl(resultado)}"]

    elif verba == "INSS Mensal (tabela progressiva)":
        st.markdown('<div class="descricao-verba">Cálculo progressivo conforme tabela INSS do ano de referência</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        base = c1.number_input("Base de cálculo (R$)", min_value=0.0, step=0.01, format="%.2f")
        ano  = c2.selectbox("Ano de Referência", [2026, 2025, 2024])
        if st.button("Calcular", type="primary", use_container_width=True):
            resultado, aliq = calc_inss(base, ano)
            tab = TABELA_INSS[ano]
            memoria = [f"Base: {brl(base)} | Ano: {ano}", f"Tabela INSS {ano}:"] + \
                      [f"  até {brl(f['limite'])}: {f['aliq']*100:.1f}%" for f in tab] + \
                      [f"Alíquota aplicada: {aliq*100:.1f}%", f"= {brl(resultado)}"]

    # ── Salva resultado no session_state ao calcular ─────────────────────────

    if resultado is not None:
        st.session_state.ultimo_resultado = {
            "verba":   verba,
            "codigo":  meta["codigo"],
            "tipo":    meta["tipo"],
            "valor":   resultado,
            "memoria": memoria,
        }

    # ── Exibe resultado persistido ────────────────────────────────────────────

    ur = st.session_state.ultimo_resultado
    if ur is not None and ur["verba"] == verba:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### Resultado")
        st.metric(label=ur["verba"], value=brl(ur["valor"]))

        if ur["memoria"]:
            with st.expander("Ver memória de cálculo"):
                st.markdown(
                    '<div class="memoria-box">' + "\n".join(ur["memoria"]) + '</div>',
                    unsafe_allow_html=True
                )

        # Adicionar ao histórico
        st.markdown("<hr>", unsafe_allow_html=True)
        c_ref, c_add = st.columns([3, 1])
        ref_input = c_ref.text_input(
            "Mês/Ano de Referência",
            placeholder="Ex: FL2/26, 2026, FL1/26",
            key="ref_input"
        )
        if c_add.button("➕ Adicionar à lista", use_container_width=True):
            st.session_state.historico.append({
                "verba":      ur["verba"],
                "codigo":     ur["codigo"],
                "tipo":       ur["tipo"],
                "referencia": ref_input or "—",
                "valor":      ur["valor"],
            })
            st.session_state.ultimo_resultado = None
            st.rerun()

        # Conferência
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### 3. Conferência")
        st.caption("Compare com o valor informado pela unidade no Resumo Funcional.")
        c1, c2 = st.columns([3, 1])
        val_unidade = c1.number_input("Valor informado pela unidade (R$)",
                                       min_value=0.0, step=0.01, format="%.2f", key="val_unidade")
        if c2.button("Conferir", use_container_width=True) and val_unidade > 0:
            dif = abs(val_unidade - ur["valor"])
            if dif < 0.05:
                st.success(f"✅ **Valores conferem.** Calculado: **{brl(ur['valor'])}** | Informado: **{brl(val_unidade)}**")
            else:
                sinal = "a mais" if val_unidade > ur["valor"] else "a menos"
                st.error(f"❌ **Divergência de {brl(dif)} ({sinal}).** Calculado: **{brl(ur['valor'])}** | Informado: **{brl(val_unidade)}**")

# ─── SEÇÃO 3: LISTA DE CÁLCULOS E EXPORTAÇÃO ─────────────────────────────────

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### 📄 Lista de cálculos realizados")

if not st.session_state.historico:
    st.info("Nenhum cálculo adicionado ainda. Após calcular uma verba, clique em **➕ Adicionar à lista**.")
else:
    # Tabela resumo
    import pandas as pd
    df = pd.DataFrame([{
        "Código":      h["codigo"],
        "Verba":       h["verba"],
        "Tipo":        h["tipo"],
        "Referência":  h["referencia"],
        "Valor (R$)":  brl_num(h["valor"]),
    } for h in st.session_state.historico])
    st.dataframe(df, use_container_width=True, hide_index=True)

    total_v = sum(h["valor"] for h in st.session_state.historico if h["tipo"] == "Vantagem")
    total_d = sum(h["valor"] for h in st.session_state.historico if h["tipo"] == "Desconto")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Vantagens", brl(total_v))
    c2.metric("Total Descontos", brl(total_d))
    c3.metric("Líquido", brl(total_v - total_d))

    col_limpar, col_pdf = st.columns([1, 2])

    if col_limpar.button("🗑️ Limpar lista", use_container_width=True):
        st.session_state.historico = []
        st.rerun()

    if col_pdf.button("📥 Gerar PDF", type="primary", use_container_width=True):
        pdf_bytes = gerar_pdf(st.session_state.historico, st.session_state.dados_servidor)
        nome_arquivo = f"verbas_{st.session_state.dados_servidor['masp'] or 'servidor'}_{date.today().strftime('%Y%m%d')}.pdf"
        st.download_button(
            label="⬇️ Baixar PDF agora",
            data=pdf_bytes,
            file_name=nome_arquivo,
            mime="application/pdf",
            use_container_width=True,
        )
