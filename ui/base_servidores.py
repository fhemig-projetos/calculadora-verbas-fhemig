import streamlit as st
from data import ProvedorServidoresLocal, ErroImportacao


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

            arquivo = st.file_uploader(
                "Planilha de dados funcionais (.csv ou .xlsx)", type=["csv", "xlsx"], key="upload_base_servidores"
            )
            if arquivo is not None and st.button("Importar base", type="primary"):
                try:
                    resultado = ProvedorServidoresLocal.importar_planilha(arquivo.getvalue(), arquivo.name)
                except ErroImportacao as erro:
                    st.error(str(erro))
                    return

                aviso = ""
                if resultado.linhas_ignoradas:
                    aviso += f" {resultado.linhas_ignoradas} linha(s) sem MASP/Nº de admissão foram ignoradas."
                if resultado.datas_invalidas:
                    aviso += f" {resultado.datas_invalidas} data(s) inválida(s) ficaram em branco."
                st.session_state["_mensagem_importacao"] = (
                    f"Base importada: {resultado.total} servidores.{aviso}"
                )
                st.rerun()
