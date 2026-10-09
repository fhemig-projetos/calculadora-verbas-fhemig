import io
import json
import re
import unicodedata
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional

import pandas as pd

from .armazenamento_local import conexao

NIVEL_ROMANO_PARA_ARABICO = {"I": "1", "II": "2", "III": "3", "IV": "4", "V": "5", "VI": "6"}

# Cabeçalhos da planilha enviada às unidades (mesmo layout do CSV de dados funcionais).
# "Masp/Admissão" não é obrigatória: é sempre recalculada (MASP + Nº Admissão).
COLUNAS_OBRIGATORIAS = (
    "Nome Servidor", "MASP", "Nº Admissão", "Data Inicio",
    "Data Fim Efetiva", "Cod Carreira", "Símbolo Vencimento", "Nivel", "Grau",
    "Carga Horária Pagamento",
)
COLUNA_REFERENCIA = "Ano/Mês Referência"  # só existe na aba/relatório que traz a CH de cada competência
_FORMATOS_DATA = ("%Y/%m/%d", "%Y-%m-%d", "%d/%m/%Y")


@dataclass
class ResultadoImportacao:
    total: int              # registros (contratos) gravados
    servidores: int         # MASPs distintos
    linhas_ignoradas: int   # sem MASP/Nº de admissão
    datas_invalidas: int    # viraram campo vazio
    linhas_malformadas: int = 0  # CSV com número de campos diferente do cabeçalho
    tem_aba_ch: bool = False     # planilha trouxe o relatório de CH para mesclar
    ch_corrigida: int = 0   # CH ausente (#MULTIVALUE/vazia) preenchida pelo relatório de CH
    ch_ambigua: int = 0     # relatório de CH com mais de uma CH para o mesmo contrato (fica sem CH)
    ch_indefinida: int = 0  # contrato sem correspondência no relatório de CH (fica sem CH)


class ErroImportacao(Exception):
    """Planilha inválida (mensagem pronta para exibir ao usuário)."""


def _texto(valor) -> str:
    return "" if valor is None else str(valor).strip()


def _numero_inteiro_como_texto(valor) -> str:
    """MASP/Nº de admissão: o Excel pode entregar '1234567.0' para células numéricas."""
    return re.sub(r"\.0+$", "", _texto(valor))


def _parse_data(valor) -> tuple[Optional[str], bool]:
    """Retorna (data ISO ou None, houve_erro). Aceita 'AAAA/MM/DD', 'AAAA-MM-DD' e 'DD/MM/AAAA',
    com ou sem horário depois."""
    bruto = _texto(valor)
    if not bruto:
        return None, False
    parte_data = bruto.split(" ")[0].split("T")[0]
    for formato in _FORMATOS_DATA:
        try:
            return datetime.strptime(parte_data, formato).date().isoformat(), False
        except ValueError:
            continue
    return None, True


def _parse_carga_horaria(valor) -> float:
    """CH numérica ou 0.0 (vazia, '#MULTIVALUE' ou qualquer valor não numérico)."""
    try:
        return float(_texto(valor).replace(",", ".") or 0)
    except ValueError:
        return 0.0


def _sem_acento(texto: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", texto) if not unicodedata.combining(c))


def _chave_cabecalho(nome) -> str:
    return " ".join(_sem_acento(str(nome)).casefold().split())


_CABECALHOS_CANONICOS = {_chave_cabecalho(c): c for c in (*COLUNAS_OBRIGATORIAS, COLUNA_REFERENCIA)}


def _padronizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    """Aceita variações de acento/caixa/espaços (ex.: 'Data Início' → 'Data Inicio')."""
    df.columns = [_CABECALHOS_CANONICOS.get(_chave_cabecalho(c), str(c).strip()) for c in df.columns]
    return df


def _ler_planilha(conteudo: bytes, nome_arquivo: str) -> tuple[pd.DataFrame, Optional[pd.DataFrame], int]:
    """Retorna (base, relatório de CH ou None, linhas malformadas).

    No .xlsx, a aba com a coluna 'Ano/Mês Referência' é o relatório de CH por competência;
    a outra é a base de contratos. CSV é sempre só a base.
    """
    extensao = nome_arquivo.lower().rsplit(".", 1)[-1] if "." in nome_arquivo else ""
    malformadas = 0
    try:
        if extensao in ("xlsx", "xlsm"):
            abas = pd.read_excel(io.BytesIO(conteudo), sheet_name=None, dtype=str, keep_default_na=False)
            abas = [_padronizar_colunas(df) for df in abas.values()]
        elif extensao == "csv":
            def _ignorar(_linha):
                return None  # descarta a linha em vez de recusar o arquivo

            # sep=None detecta ';' ou ','; utf-8-sig remove o BOM de CSV exportado do Excel.
            df = pd.read_csv(
                io.BytesIO(conteudo), dtype=str, keep_default_na=False,
                sep=None, engine="python", encoding="utf-8-sig",
                skipinitialspace=True, on_bad_lines=_ignorar,
            )
            # O pandas descarta algumas linhas ruins (ex.: aspas quebradas) sem avisar: a conta é
            # linhas com conteúdo no arquivo (menos o cabeçalho) − linhas lidas.
            linhas_arquivo = sum(1 for l in conteudo.splitlines() if l.strip())
            abas, malformadas = [_padronizar_colunas(df)], max(0, linhas_arquivo - 1 - len(df))
        else:
            raise ErroImportacao("Formato não suportado. Envie um arquivo .csv ou .xlsx.")
    except ErroImportacao:
        raise
    except Exception as erro:
        raise ErroImportacao(f"Não foi possível ler o arquivo: {erro}") from erro

    relatorios_ch = [df for df in abas if COLUNA_REFERENCIA in df.columns]
    bases = [df for df in abas if COLUNA_REFERENCIA not in df.columns]
    if not bases:
        raise ErroImportacao("A planilha não tem a aba com os dados funcionais dos servidores.")
    return bases[0], (relatorios_ch[0] if relatorios_ch else None), malformadas


def _chave_contrato(linha: dict) -> tuple[str, str, Optional[str]]:
    """Mesmo MASP + mesmo Nº de admissão + mesma data de início = mesmo contrato
    (a data fim muda em prorrogações e ajustes de lançamento e não entra na chave)."""
    return (
        _numero_inteiro_como_texto(linha["MASP"]),
        _numero_inteiro_como_texto(linha["Nº Admissão"]),
        _parse_data(linha["Data Inicio"])[0],
    )


def _mapa_carga_horaria(relatorio: pd.DataFrame) -> dict[tuple, set[float]]:
    """(MASP, admissão, início) → CHs numéricas informadas no relatório de CH."""
    mapa: dict[tuple, set[float]] = {}
    for linha in relatorio.to_dict("records"):
        ch = _parse_carga_horaria(linha["Carga Horária Pagamento"])
        if ch > 0:
            mapa.setdefault(_chave_contrato(linha), set()).add(ch)
    return mapa


def _validar_colunas(df: pd.DataFrame, nome: str):
    faltando = [c for c in COLUNAS_OBRIGATORIAS if c not in df.columns]
    if faltando:
        raise ErroImportacao(f"Colunas ausentes na planilha ({nome}): " + ", ".join(faltando))


class ProvedorServidoresLocal:
    """Base de servidores no SQLite local, atualizada por importação de planilha."""

    @staticmethod
    def buscar_servidor(masp: str, numero_admissao: str) -> Optional[dict]:
        """Busca um servidor pelo MASP e Nº de Admissão. None se não achar ou a base estiver vazia.

        O campo `nivel` vem em algarismo romano na base (ex: "II"), enquanto
        `tabela_cargos` (data/tabelas.json) usa algarismo arábico — convertido
        aqui para que a busca de cargo (ProvedorDadosFhemig.buscar_cargo) funcione.
        Sem cache de propósito: a base pode ser reimportada a qualquer momento.

        A base guarda um registro por contrato, então o mesmo MASP + admissão pode ter vários.
        Enquanto o técnico não escolhe o contrato (ver 29.5 do contexto.md), devolve
        o de maior data fim (contrato sem data fim vale como o mais recente).
        """
        with conexao() as con:
            linha = con.execute(
                "SELECT * FROM servidores WHERE masp = ? AND numero_admissao = ? "
                "ORDER BY COALESCE(NULLIF(data_fim_efetiva, ''), '9999-12-31') DESC, "
                "data_inicio DESC, id DESC LIMIT 1",
                (masp.strip(), numero_admissao.strip()),
            ).fetchone()
        if linha is None:
            return None
        servidor = dict(linha)
        servidor["nivel"] = NIVEL_ROMANO_PARA_ARABICO.get(servidor["nivel"], servidor["nivel"])
        return servidor

    @staticmethod
    def info_base() -> dict:
        """Situação da base: servidores, contratos, data da última importação, arquivo e resumo da importação."""
        with conexao() as con:
            total, registros = con.execute("SELECT COUNT(DISTINCT masp), COUNT(*) FROM servidores").fetchone()
            meta = {l["chave"]: l["valor"] for l in con.execute("SELECT chave, valor FROM meta")}
        atualizada = meta.get("base_atualizada_em")
        resumo = meta.get("base_resumo")
        return {
            "total": total,
            "registros": registros,
            "atualizada_em": datetime.fromisoformat(atualizada) if atualizada else None,
            "arquivo": meta.get("base_arquivo"),
            "resumo": json.loads(resumo) if resumo else None,
        }

    @staticmethod
    def importar_planilha(conteudo: bytes, nome_arquivo: str) -> ResultadoImportacao:
        """Substitui TODA a base de servidores pelo conteúdo da planilha (CSV ou XLSX).

        A base guarda as linhas da consulta como vieram, um registro por contrato (inclusive vários
        para o mesmo MASP + admissão). No .xlsx com dois relatórios, a CH ausente ('#MULTIVALUE' ou
        vazia) do primeiro é preenchida pela CH do segundo, casando por MASP + admissão + data de início.

        Tudo ou nada: se a planilha for inválida, a base atual permanece intacta.
        """
        df, relatorio_ch, malformadas = _ler_planilha(conteudo, nome_arquivo)
        _validar_colunas(df, "dados funcionais")
        mapa_ch = None
        if relatorio_ch is not None:
            _validar_colunas(relatorio_ch, "relatório de carga horária")
            mapa_ch = _mapa_carga_horaria(relatorio_ch)

        registros: list[tuple] = []
        ignoradas = datas_invalidas = corrigidas = ambiguas = indefinidas = 0
        for linha in df.to_dict("records"):
            masp, admissao, data_inicio = _chave_contrato(linha)
            if not masp or not admissao:
                ignoradas += 1
                continue

            _, erro_inicio = _parse_data(linha["Data Inicio"])
            data_fim, erro_fim = _parse_data(linha["Data Fim Efetiva"])
            datas_invalidas += erro_inicio + erro_fim

            carga_horaria = _parse_carga_horaria(linha["Carga Horária Pagamento"])
            if carga_horaria <= 0 and mapa_ch is not None:
                opcoes = mapa_ch.get((masp, admissao, data_inicio), set())
                if len(opcoes) == 1:
                    carga_horaria = next(iter(opcoes))
                    corrigidas += 1
                elif opcoes:
                    ambiguas += 1
                else:
                    indefinidas += 1

            registros.append((
                f"{masp}{admissao}", _texto(linha["Nome Servidor"]), masp, admissao, data_inicio, data_fim,
                _texto(linha["Cod Carreira"]), _texto(linha["Símbolo Vencimento"]),
                _texto(linha["Nivel"]), _texto(linha["Grau"]), carga_horaria,
            ))

        if not registros:
            raise ErroImportacao("A planilha não tem nenhum servidor válido (MASP e Nº de Admissão preenchidos).")

        resultado = ResultadoImportacao(
            total=len(registros), servidores=len({r[2] for r in registros}),
            linhas_ignoradas=ignoradas, datas_invalidas=datas_invalidas, linhas_malformadas=malformadas,
            tem_aba_ch=mapa_ch is not None, ch_corrigida=corrigidas, ch_ambigua=ambiguas,
            ch_indefinida=indefinidas,
        )
        with conexao() as con:  # transação única: erro no meio desfaz tudo
            con.execute("DELETE FROM servidores")
            con.executemany(
                "INSERT INTO servidores (masp_admissao, nome, masp, numero_admissao, data_inicio, "
                "data_fim_efetiva, cod_carreira, simbolo_vencimento, nivel, grau, carga_horaria) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                registros,
            )
            con.executemany(
                "INSERT INTO meta (chave, valor) VALUES (?, ?) "
                "ON CONFLICT(chave) DO UPDATE SET valor = excluded.valor",
                [
                    ("base_atualizada_em", datetime.now().isoformat(timespec="seconds")),
                    ("base_arquivo", nome_arquivo),
                    ("base_resumo", json.dumps(asdict(resultado))),
                ],
            )
        return resultado
