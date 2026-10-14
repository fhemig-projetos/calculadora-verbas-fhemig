import streamlit as st
from data import ProvedorDadosFhemig, ProvedorServidoresLocal
from utils import FormatadorCampos, on_change_masp, on_change_normalizar_masp, on_change_maiusculo_strip, on_change_strip
import datetime

SEM_CONTRATO = "Selecione o contrato..."
OUTRA_DATA = "Outra data (digite abaixo)"


def _data_br(iso):
    return datetime.date.fromisoformat(iso).strftime("%d/%m/%Y") if iso else "sem data fim"


def _rotulo_contrato(contrato: dict) -> str:
    """Ex.: '13/09/2016 → 31/01/2021 · PENF4'."""
    inicio = _data_br(contrato["data_inicio"]) if contrato["data_inicio"] else "sem data de início"
    simbolo = contrato["simbolo_vencimento"] or contrato["cod_carreira"]
    return f"{inicio} → {_data_br(contrato['data_fim_efetiva'])}" + (f" · {simbolo}" if simbolo else "")


def _contrato_da_data(contratos: list, data) -> dict | None:
    """Contrato cuja data de início é a data informada (None se não houver)."""
    iso = data.isoformat() if data else None
    return next((c for c in contratos if iso and c["data_inicio"] == iso), None)


def _aplicar_contrato(ds: dict, contrato: dict):
    ds["dt_admissao"] = datetime.date.fromisoformat(contrato["data_inicio"]) if contrato["data_inicio"] else None
    ds["dt_fim_efetiva"] = (
        datetime.date.fromisoformat(contrato["data_fim_efetiva"]) if contrato["data_fim_efetiva"] else None
    )
    ds["cargo_classe"] = contrato["cod_carreira"]
    ds["cargo_nivel"] = contrato["nivel"]
    ds["cargo_grau"] = contrato["grau"]
    ds["ch_semanal"] = int(contrato["carga_horaria"] or 0)


def _limpar_contrato(ds: dict):
    """Esvazia tudo que vem do contrato (o nome do servidor fica)."""
    ds["dt_admissao"] = None
    ds["dt_fim_efetiva"] = None
    ds["cargo_classe"] = ""
    ds["cargo_nivel"] = ""
    ds["cargo_grau"] = ""
    ds["ch_semanal"] = 0


def _trocar_contrato(rotulo_selecao: str):
    """Usado pelos callbacks: nonce novo recria os campos (que leem o ds) e o seletor já nasce posicionado."""
    st.session_state["servidor_nonce"] += 1
    st.session_state[f"{st.session_state['servidor_nonce']}::contrato"] = rotulo_selecao


def _ao_escolher_contrato(key: str):
    ds = st.session_state["dados_servidor"]
    escolha = st.session_state[key]
    contratos = ProvedorServidoresLocal.buscar_contratos(st.session_state["masp"], st.session_state["admissao"])
    escolhido = next((c for c in contratos if _rotulo_contrato(c) == escolha), None)
    if escolhido:
        _aplicar_contrato(ds, escolhido)
    elif escolha == OUTRA_DATA:  # preenchimento manual: só esvazia as datas, o resto fica para editar
        ds["dt_admissao"] = None
        ds["dt_fim_efetiva"] = None
    else:
        _limpar_contrato(ds)
    _trocar_contrato(escolha)


def _ao_digitar_data_admissao(key: str):
    """Data digitada que é o início de um contrato da base seleciona e aplica esse contrato."""
    ds = st.session_state["dados_servidor"]
    data = st.session_state[key]
    contratos = ProvedorServidoresLocal.buscar_contratos(st.session_state["masp"], st.session_state["admissao"])
    contrato = _contrato_da_data(contratos, data)
    if contrato:
        _aplicar_contrato(ds, contrato)
    else:
        ds["dt_admissao"] = data
    _trocar_contrato(_rotulo_contrato(contrato) if contrato else OUTRA_DATA)


class FormularioServidor:
    """Formulário de Dados do Servidor.

    Encapsula o estado e a renderização do cabeçalho com dados funcionais
    do servidor (nome, MASP, cargo, vencimento, carga horária, etc.).
    """

    def __init__(self):
        # Carrega o session_state["dados_servidor"] se não houver análise salva no SQLite local
        if "dados_servidor" not in st.session_state:
            st.session_state["dados_servidor"] = {
                "nome": "",
                "masp": "",
                "admissao": "",
                "dt_admissao": None,
                "dt_fim_efetiva": None,
                "cargo_classe": "",
                "cargo_nivel": "",
                "cargo_grau": "",
                "ch_semanal": 0,
                "ch_mensal": 0,
                "vencimento_basico": 0.0,
                "piso_enfermagem": 0.0,
                "servidor_encontrado": None,
            }
        if "servidor_nonce" not in st.session_state:
            st.session_state["servidor_nonce"] = 0

        if "ultima_busca_servidor" not in st.session_state:
            st.session_state["ultima_busca_servidor"] = None

    def render(self):
        with st.expander("Dados do Servidor", expanded=True):
            # Carrega os dados do cabeçalho com os dados do session_state["dados_servidor"]
            ds = st.session_state["dados_servidor"] 

            c1, c2, c3 = st.columns(3)
            bloco_contrato = st.container()  # seletor de contrato, entre a linha do MASP e a das datas
            c4, c5 = st.columns(2)

            # Sem value=: o widget tem on_change (que reescreve o valor); o estado inicial vem da análise salva.
            if "masp" not in st.session_state:
                st.session_state["masp"] = ds["masp"]
            ds["masp"]     = c1.text_input(
                "MASP", placeholder="Ex: 12345678", key="masp",
                on_change=on_change_normalizar_masp, args=("masp",),
                help="Somente números, com o dígito verificador. Pontos, traços e espaços são removidos. "
                     "Zeros à esquerda são ignorados: o MASP pode ter 7 ou 8 dígitos (ex.: 0847104-7 → 8471047).",
            )
            ds["admissao"] = c2.text_input("Nº de Admissão", value=ds["admissao"], help="Somente números.", placeholder="Ex: 1, 2", key="admissao")

            contratos = []
            if ds["masp"] and ds["admissao"]:
                busca_atual = (ds["masp"], ds["admissao"])
                contratos = ProvedorServidoresLocal.buscar_contratos(ds["masp"], ds["admissao"])

                if busca_atual != st.session_state["ultima_busca_servidor"]:
                    """
                    - Lógica de alteração da busca por masp e admissão.
                    - Ativa nova consulta quando altera o masp ou admissão: preenche só o NOME; datas, cargo,
                    nível, grau e CH ficam vazios até o técnico escolher o contrato (ou digitar a data).
                    - Na linha `ds["servidor_encontrado"] = bool(contratos)`,
                    ds["servidor_encontrado"] aponta para o mesmo endereço da memória que
                    st.session_state["dados_servidor"]["servidor_encontrado"]. Por isso,
                    essa atribuição já reflete diretamente na variável de session_state.
                    """
                    st.session_state["ultima_busca_servidor"] = busca_atual

                    # Incrementa o nonce que será usado nas chaves dos campos (evita bugs de preenchimento)
                    st.session_state["servidor_nonce"] += 1

                    # Marca no session_state bool referente a se encontrou servidor ou não.
                    # Usado abaixo para corrigir bug de display da mensagem de busca
                    ds["servidor_encontrado"] = bool(contratos)

                    _limpar_contrato(ds)
                    # Não encontrado: limpa também o nome, para não deixar dados de outro
                    # servidor associados ao MASP/Admissão atual
                    ds["nome"] = contratos[0]["nome"] if contratos else ""

                with bloco_contrato:
                    if contratos:
                        # A key tem o nonce: o seletor é recriado a cada busca/troca de contrato. Na primeira
                        # renderização (ex.: análise restaurada) a posição vem da data de admissão do cabeçalho.
                        key_contrato = f"{st.session_state['servidor_nonce']}::contrato"
                        if key_contrato not in st.session_state:
                            atual = _contrato_da_data(contratos, ds["dt_admissao"])
                            st.session_state[key_contrato] = (
                                _rotulo_contrato(atual) if atual else (OUTRA_DATA if ds["dt_admissao"] else SEM_CONTRATO)
                            )
                        st.selectbox(
                            "Contrato (data de admissão)",
                            [SEM_CONTRATO, *[_rotulo_contrato(c) for c in contratos], OUTRA_DATA],
                            key=key_contrato, on_change=_ao_escolher_contrato, args=(key_contrato,),
                            help="Contratos deste MASP e Nº de admissão na base. Ao escolher, preenche datas, cargo, "
                                 "nível, grau e carga horária. Prorrogações (mesmo início, outra data fim) aparecem "
                                 "como um contrato só, com a maior data fim.",
                        )

                    # Mensagem refletindo o resultado da última busca feita
                    if ds.get("servidor_encontrado"):
                        if _contrato_da_data(contratos, ds["dt_admissao"]):
                            st.success("✅ Servidor encontrado na base — dados do contrato preenchidos automaticamente")
                        else:
                            st.info("ℹ️ Servidor encontrado na base. Escolha o contrato acima (ou digite a data de "
                                    "admissão) para preencher os dados; ou preencha manualmente.")
                    else:
                        st.info("ℹ️ Servidor não encontrado na base. Preencha os dados manualmente.")

            # Lido só após o bloco de busca, já com o nonce incrementado nesta
            # rodada (se houve busca nova) — os campos abaixo nascem com key
            # nova e aceitam o value= atualizado sem esperar mais um rerun.
            nonce = st.session_state.get("servidor_nonce")
            ds["nome"] = c3.text_input("Nome Completo do Servidor", value=ds["nome"], key=f"{nonce}::nome")

            # Define padrão de data explicitamente
            ds["dt_admissao"] = c4.date_input(
                "Data de Admissão", value=ds["dt_admissao"], format="DD/MM/YYYY",
                min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today(),
                key=f"{nonce}::dt_admissao",
                on_change=_ao_digitar_data_admissao, args=(f"{nonce}::dt_admissao",),
            )
            ds["dt_fim_efetiva"] = c5.date_input(
                "Data Fim Efetiva", value=ds["dt_fim_efetiva"], format="DD/MM/YYYY",
                min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today(),
                key=f"{nonce}::dt_fim_efetiva"
            )

            st.divider()

            st.caption("**Cargo** — preencha para busca automática do vencimento básico e carga horária mensal")
            c6, c7, c8 = st.columns(3)

            # Campos com on_change não podem receber value= (Streamlit acusa
            # warning de conflito entre os dois). O valor é escrito
            # direto em session_state[key], só na primeira vez que a key existe
            # (ou seja, só quando o nonce muda) — por isso o formato abaixo.
            key_cargo_classe = f"{nonce}::cargo_classe"
            key_cargo_nivel = f"{nonce}::cargo_nivel"
            key_cargo_grau = f"{nonce}::cargo_grau"

            if key_cargo_classe not in st.session_state:
                st.session_state[key_cargo_classe] = ds["cargo_classe"]

            if key_cargo_nivel not in st.session_state:
                st.session_state[key_cargo_nivel] = ds["cargo_nivel"]

            if key_cargo_grau not in st.session_state:
                st.session_state[key_cargo_grau] = ds["cargo_grau"]

            ds["cargo_classe"] = c6.text_input("Cargo", placeholder="Ex: PENF", key=key_cargo_classe, on_change=on_change_maiusculo_strip, args=(key_cargo_classe,))
            ds["cargo_nivel"]  = c7.text_input("Nível",          placeholder="Ex: 2", key=key_cargo_nivel, on_change=on_change_strip, args=(key_cargo_nivel,))
            ds["cargo_grau"]   = c8.text_input("Grau",           placeholder="Ex: A", key=key_cargo_grau, on_change=on_change_maiusculo_strip, args=(key_cargo_grau,))

            c9, c10 = st.columns(2)
            ds["ch_semanal"] = c9.number_input(
                "Carga Horária Semanal", value=ds["ch_semanal"], min_value=0, step=1,
                key=f"{nonce}::ch_semanal")

            contrato_atual = _contrato_da_data(contratos, ds["dt_admissao"])
            if contrato_atual and not contrato_atual["carga_horaria"] and not ds["ch_semanal"]:
                c9.warning("⚠️ Este contrato está sem carga horária na base. Informe manualmente.")

            # Calcula a ch mensal com base na ch semanal informada
            ds["ch_mensal"] = int(ds["ch_semanal"] / 5 * 30)

            # CH semanal entra na key p/ o campo ch mensal atualizar ao trocar a ch semanal 
            # manualmente (correção de bug do campo ch mensal ficar travado)
            key_ch_mensal = f"{nonce}::ch_mensal::{ds['ch_semanal']}"
            c10.number_input("Carga Horária Mensal", value=ds["ch_mensal"], disabled=True, key=key_ch_mensal)

            cargo_encontrado = None
            ds["piso_enfermagem"] = 0.0  # só vira > 0 se o cargo encontrado tiver piso (PENF II/IV contratados)
            # Se campos preenchidos
            if ds["cargo_classe"] and ds["cargo_nivel"] and ds["cargo_grau"] and ds["ch_semanal"]:
                # Busca o cargo
                cargo_encontrado = ProvedorDadosFhemig.buscar_cargo(ds["cargo_classe"], ds["cargo_nivel"], ds["cargo_grau"], ds["ch_semanal"])

                # Combinação de cargo/nível/grau/CH entra na key p/ o vencimento atualizar ao 
                # trocar qualquer um dos campos (resolve bug de não ser disparada nova busca
                # do valor do vencimento básico)  
                key_vencimento = f"{nonce}::vencimento_basico::{ds['cargo_classe']}::{ds['cargo_nivel']}::{ds['cargo_grau']}::{ds['ch_semanal']}"

                # Se cargo encontrado retorna valor do vencimento básico e deixa o campo editável
                if cargo_encontrado:
                    ds["piso_enfermagem"] = cargo_encontrado.get("piso_enfermagem", 0.0)
                    mensagem_cargo = "✅ Cargo encontrado. Vencimento básico pré-preenchido!"
                    if ds["piso_enfermagem"]:
                        mensagem_cargo += f" Piso de Enfermagem ({FormatadorCampos.brl(ds['piso_enfermagem'])}) pré-preenchido nas verbas de piso."
                    st.success(mensagem_cargo)
                    ds["vencimento_basico"] = st.number_input("Vencimento Básico (R$)", value=cargo_encontrado["vencimento_basico"], format="%.2f", key=key_vencimento)
                # Se cargo não encontrado abre campos para preenchimento
                else:
                    st.warning("⚠️ Cargo não encontrado na tabela. Preencha o vencimento básico manualmente abaixo.")
                    ds["vencimento_basico"] = st.number_input("Vencimento Básico (R$)", value=0.0, format="%.2f", key=key_vencimento)