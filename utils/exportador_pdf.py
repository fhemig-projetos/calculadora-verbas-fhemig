"""Geração do PDF de conferência de verbas no layout padrão da FHEMIG."""

import io
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    Frame,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from utils.formatador_campos import FormatadorCampos

BASE_DIR = Path(__file__).resolve().parent.parent
LOGO_PATH = BASE_DIR / "assets" / "cabecalho_pdf.png"


class GeradorPDF:
    """Gera o PDF de conferência de verbas no layout padrão da FHEMIG.

    Espelha o gerador de PDF de outra aplicação do time: BaseDocTemplate com
    cabeçalho (logo) na primeira página, cor institucional #108da5, seções
    "Dados do Servidor" e "Verbas Calculadas" e rodapé com data + aviso.
    """

    AZUL = colors.HexColor("#108da5")

    def __init__(self, historico: list[dict], dados_servidor: dict):
        self.historico = historico or []
        self.dados_servidor = dados_servidor or {}
        self.styles = getSampleStyleSheet()
        self.estilo_titulo = ParagraphStyle(
            "Estilo",
            parent=self.styles["Heading2"],
            textColor=self.AZUL,
            fontSize=15,
            leading=18,
            spaceAfter=5,
        )

    # ── API pública ────────────────────────────────────────────────────────────
    def gerar(self) -> bytes:
        buf = io.BytesIO()
        largura_pagina, altura_pagina = A4

        doc = BaseDocTemplate(
            buf,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=90,
            bottomMargin=40,
        )

        frame_primeira_pagina = Frame(
            x1=40, y1=40,
            width=largura_pagina - 80,
            height=altura_pagina - 90 - 40,
            id="frame_primeira_pagina",
        )
        frame_demais_paginas = Frame(
            x1=40, y1=40,
            width=largura_pagina - 80,
            height=altura_pagina - 40 - 40,
            id="frame_demais_paginas",
        )

        doc.addPageTemplates([
            PageTemplate(
                id="primeira_pagina",
                frames=[frame_primeira_pagina],
                onPage=self._adicionar_cabecalho,
                autoNextPageTemplate="demais_paginas",
            ),
            PageTemplate(
                id="demais_paginas",
                frames=[frame_demais_paginas],
            ),
        ])

        elementos = []
        self._adicionar_dados_servidor(elementos)
        self._adicionar_verbas(elementos)
        self._adicionar_rodape(elementos)

        doc.build(elementos)
        return buf.getvalue()

    # ── Cabeçalho (logo) e estilos de célula ───────────────────────────────────
    def _adicionar_cabecalho(self, canvas, doc):
        canvas.saveState()
        largura_pagina, altura_pagina = A4
        if LOGO_PATH.exists():
            canvas.drawImage(
                str(LOGO_PATH),
                x=40,
                y=altura_pagina - 85,
                width=largura_pagina - 80,
                height=70,
                preserveAspectRatio=True,
            )
        canvas.restoreState()

    def _estilo_celula(self):
        return ParagraphStyle(
            "CelulaTabela",
            parent=self.styles["BodyText"],
            fontSize=8,
            leading=12,
        )

    def _estilo_celula_titulo(self):
        return ParagraphStyle(
            "CelulaTabelaTitulo",
            parent=self._estilo_celula(),
            textColor=self.AZUL,
        )

    # ── Dados do Servidor ──────────────────────────────────────────────────────
    def _adicionar_dados_servidor(self, elementos: list):
        ds = self.dados_servidor
        elementos.append(Paragraph("Dados do Servidor", self.estilo_titulo))

        estilo_celula = self._estilo_celula()
        estilo_celula_titulo = self._estilo_celula_titulo()

        dt_admissao = ds.get("dt_admissao")
        data_admissao = dt_admissao.strftime("%d/%m/%Y") if dt_admissao else "—"
        dt_fim_efetiva = ds.get("dt_fim_efetiva")
        data_fim_efetiva = dt_fim_efetiva.strftime("%d/%m/%Y") if dt_fim_efetiva else "—"
        ven = ds.get("vencimento_basico")

        def linha(label, valor):
            return [
                Paragraph(f"<b>{label}</b>", estilo_celula_titulo),
                Paragraph(str(valor), estilo_celula),
            ]

        dados_tabela = [
            linha("MASP", FormatadorCampos.masp(ds.get("masp")) or "—"),
            linha("Nº de Admissão", ds.get("admissao") or "—"),
            linha("Nome", ds.get("nome") or "—"),
            linha("Data de Admissão", data_admissao),
            linha("Data Fim Efetiva", data_fim_efetiva),
            linha("Cargo", ds.get("cargo_classe") or "—"),
            linha("Nível", ds.get("cargo_nivel") or "—"),
            linha("Grau", ds.get("cargo_grau") or "—"),
            linha("Carga Horária Mensal", f'{ds.get("ch_mensal") or 0:.0f}h'),
            linha("Vencimento Básico", FormatadorCampos.brl(ven) if ven else "—"),
        ]

        tabela = Table(dados_tabela, colWidths=[115, 200])
        tabela.hAlign = "LEFT"
        tabela.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.white),
            ("LINEAFTER", (0, 0), (0, -1), 0.75, self.AZUL),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEADING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        elementos.append(tabela)
        elementos.append(Spacer(1, 20))

    # ── Verbas calculadas + totais + memória ────────────────────────────────────
    def _totais(self):
        vantagens = sum(
            item.get("valor", 0.0) for item in self.historico
            if item.get("tipo") == "Vantagem"
        )
        descontos = sum(
            item.get("valor", 0.0) for item in self.historico
            if item.get("tipo") == "Desconto"
        )
        return vantagens, descontos, vantagens - descontos

    def _adicionar_verbas(self, elementos: list):
        elementos.append(Paragraph("Verbas Calculadas", self.estilo_titulo))

        estilo_celula = ParagraphStyle(
            "CelulaVerba",
            parent=self.styles["BodyText"],
            fontSize=8,
            leading=12,
            alignment=TA_CENTER,
        )
        estilo_cabecalho = ParagraphStyle(
            "CelulaVerbaCabecalho",
            parent=estilo_celula,
            textColor=colors.white,
        )
        estilo_negrito = ParagraphStyle(
            "CelulaVerbaNegrito",
            parent=estilo_celula,
            textColor=self.AZUL,
        )

        linhas = [[
            Paragraph("<b>Código</b>", estilo_cabecalho),
            Paragraph("<b>Verba</b>", estilo_cabecalho),
            Paragraph("<b>Tipo</b>", estilo_cabecalho),
            Paragraph("<b>Competência</b>", estilo_cabecalho),
            Paragraph("<b>Valor (R$)</b>", estilo_cabecalho),
        ]]

        for h in self.historico:
            linhas.append([
                Paragraph(str(h.get("codigo") or "—"), estilo_celula),
                Paragraph(str(h.get("nome_verba") or "—"), estilo_celula),
                Paragraph(str(h.get("tipo") or "—"), estilo_celula),
                Paragraph(str(h.get("competencia") or "—"), estilo_celula),
                Paragraph(FormatadorCampos.brl(h.get("valor", 0.0)), estilo_celula),
            ])

        vantagens, descontos, liquido = self._totais()
        linhas.append([
            Paragraph("<b>Total Vantagens</b>", estilo_negrito), "", "", "",
            Paragraph(FormatadorCampos.brl(vantagens), estilo_negrito),
        ])
        linhas.append([
            Paragraph("<b>Total Descontos</b>", estilo_negrito), "", "", "",
            Paragraph(FormatadorCampos.brl(descontos), estilo_negrito),
        ])
        linhas.append([
            Paragraph("<b>Líquido</b>", estilo_negrito), "", "", "",
            Paragraph(FormatadorCampos.brl(liquido), estilo_negrito),
        ])

        tabela = Table(linhas, colWidths=[50, 175, 80, 95, 115])
        tabela.hAlign = "CENTER"
        tabela.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.white),
            ("BACKGROUND", (0, 0), (-1, 0), self.AZUL),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.white),
            ("LINEAFTER", (0, 0), (0, -1), 0.75, self.AZUL),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ]))
        elementos.append(tabela)

        # Memória de cálculo de cada verba (opcional)
        itens_com_memoria = [
            (h.get("nome_verba", "Verba"), h.get("memoria") or [])
            for h in self.historico if h.get("memoria")
        ]
        if itens_com_memoria:
            elementos.append(Spacer(1, 20))
            elementos.append(Paragraph("Memória de Cálculo", self.estilo_titulo))
            for nome, memoria in itens_com_memoria:
                elementos.append(Paragraph(str(nome), self.styles["Heading3"]))
                texto = "<br/>".join(f"- {linha}" for linha in memoria)
                elementos.append(Paragraph(texto, self.styles["BodyText"]))
                elementos.append(Spacer(1, 6))

        # Observações das verbas (opcional)
        itens_com_obs = [
            (h.get("nome_verba", "Verba"), h.get("observacao"))
            for h in self.historico if h.get("observacao")
        ]
        if itens_com_obs:
            elementos.append(Spacer(1, 20))
            elementos.append(Paragraph("Observações", self.estilo_titulo))
            for nome, obs in itens_com_obs:
                elementos.append(
                    Paragraph(f"<b>{nome}:</b> {obs}", self.styles["BodyText"])
                )

    # ── Rodapé ────────────────────────────────────────────────────────────────
    def _adicionar_rodape(self, elementos: list):
        elementos.append(Spacer(1, 6))
        elementos.append(
            Paragraph(
                f"Relatório gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}.",
                self.styles["BodyText"],
            )
        )
        elementos.append(
            Paragraph(
                "Este documento possui caráter meramente informativo e não "
                "substitui análise oficial do órgão competente.",
                self.styles["Italic"],
            )
        )