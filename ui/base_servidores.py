from dataclasses import asdict

import streamlit as st
from data import ProvedorServidoresLocal, ErroImportacao


def _milhar(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def _formatar_resumo(r: dict) -> str:
    """Resumo da importação (mesmo texto na mensagem logo após importar e no painel da base)."""
    partes = [f"{_milhar(r['total'])} registros de contrato ({_milhar(r['servidores'])} servidores)."]
    if r["tem_aba_ch"]:
        partes.append(f"Carga horária: {_milhar(r['ch_corrigida'])} corrigida(s) pelo relatório de CH; "
                      f"{_milhar(r['ch_indefinida'])} sem correspondência (ficam sem CH)"
                      + (f"; {_milhar(r['ch_ambigua'])} ambígua(s) (ficam sem CH)." if r["ch_ambigua"] else "."))
    if r["linhas_ignoradas"]:
        partes.append(f"{r['linhas_ignoradas']} linha(s) sem MASP/Nº de admissão foram ignoradas.")
    if r["linhas_malformadas"]:
        partes.append(f"{r['linhas_malformadas']} linha(s) com número de colunas incorreto foram ignoradas.")
    if r["datas_invalidas"]:
        partes.append(f"{r['datas_invalidas']} data(s) inválida(s) ficaram em branco.")
    return " ".join(partes)


class BaseServidores:
    """Painel de situação e importação da base de servidores (planilha mensal enviada às unidades)."""

    def render(self):
        info = ProvedorServidoresLocal.info_base()
        vazia = info["total"] == 0

        if vazia:
            titulo = "🗂️ Base de servidores — nenhuma base importada"
        else:
            total = f"{info['total']:,}".replace(",", ".")
            titulo = f"🗂️ Base de servidores — {total} servidores, atualizada em {info['atualizada_em']:%d/%m/%Y}"

        # Aberto automaticamente só quando não há base (primeiro uso).
        with st.expander(titulo, expanded=vazia):
            mensagem = st.session_state.pop("_mensagem_importacao", None)
            if mensagem:
                st.success(mensagem)

            if vazia:
                st.info(
                    "Para a busca automática de servidores, importe a planilha de dados funcionais "
                    "enviada pela FHEMIG. Sem ela, os dados do servidor são preenchidos manualmente."
                )
            else:
                st.caption(f"Arquivo importado: {info['arquivo']}. Importar uma nova planilha substitui a base atual.")
                if info["resumo"]:
                    st.caption(f"Última importação: {_formatar_resumo(info['resumo'])}")

            arquivo = st.file_uploader(
                "Planilha de dados funcionais (.csv ou .xlsx)", type=["csv", "xlsx"], key="upload_base_servidores"
            )
            if arquivo is not None and st.button("Importar base", type="primary"):
                try:
                    resultado = ProvedorServidoresLocal.importar_planilha(arquivo.getvalue(), arquivo.name)
                except ErroImportacao as erro:
                    st.error(str(erro))
                    return

                st.session_state["_mensagem_importacao"] = (
                    f"Base importada: {_formatar_resumo(asdict(resultado))}"
                )
                st.rerun()
