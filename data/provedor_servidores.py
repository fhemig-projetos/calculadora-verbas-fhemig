import io
import re
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

import pandas as pd

from .armazenamento_local import conexao

NIVEL_ROMANO_PARA_ARABICO = {"I": "1", "II": "2", "III": "3", "IV": "4", "V": "5", "VI": "6"}

# Cabeçalhos da planilha enviada às unidades (mesmo layout do CSV de dados funcionais).
COLUNAS_OBRIGATORIAS = (
    "Nome Servidor", "MASP", "Nº Admissão", "Masp/Admissão", "Data Inicio",
    "Data Fim Efetiva", "Cod Carreira", "Símbolo Vencimento", "Nivel", "Grau",
    "Carga Horária Pagamento",
)
_FORMATOS_DATA = ("%Y/%m/%d", "%Y-%m-%d", "%d/%m/%Y")


@dataclass
class ResultadoImportacao:
    total: int
    linhas_ignoradas: int  # sem MASP/Nº de admissão
    datas_invalidas: int   # viraram campo vazio


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
    try:
        return float(_texto(valor).replace(",", ".") or 0)
    except ValueError:
        return 0.0


def _ler_planilha(conteudo: bytes, nome_arquivo: str) -> pd.DataFrame:
    extensao = nome_arquivo.lower().rsplit(".", 1)[-1] if "." in nome_arquivo else ""
    try:
        if extensao in ("xlsx", "xlsm"):
            df = pd.read_excel(io.BytesIO(conteudo), dtype=str, keep_default_na=False)
        elif extensao == "csv":
            # sep=None detecta ';' ou ','; utf-8-sig remove o BOM de CSV exportado do Excel.
            df = pd.read_csv(
                io.BytesIO(conteudo), dtype=str, keep_default_na=False,
                sep=None, engine="python", encoding="utf-8-sig",
            )
        else:
            raise ErroImportacao("Formato não suportado. Envie um arquivo .csv ou .xlsx.")
    except ErroImportacao:
        raise
    except Exception as erro:
        raise ErroImportacao(f"Não foi possível ler o arquivo: {erro}") from erro
    df.columns = [str(c).strip() for c in df.columns]
    return df


class ProvedorServidoresLocal:
    """Base de servidores no SQLite local, atualizada por importação de planilha."""

    @staticmethod
    def buscar_servidor(masp: str, numero_admissao: str) -> Optional[dict]:
        """Busca um servidor pelo MASP e Nº de Admissão. None se não achar ou a base estiver vazia.

        O campo `nivel` vem em algarismo romano na base (ex: "II"), enquanto
        `tabela_cargos` (data/tabelas.json) usa algarismo arábico — convertido
        aqui para que a busca de cargo (ProvedorDadosFhemig.buscar_cargo) funcione.
        Sem cache de propósito: a base pode ser reimportada a qualquer momento.
        """
        with conexao() as con:
            linha = con.execute(
                "SELECT * FROM servidores WHERE masp = ? AND numero_admissao = ? LIMIT 1",
                (masp.strip(), numero_admissao.strip()),
            ).fetchone()
        if linha is None:
            return None
        servidor = dict(linha)
        servidor["nivel"] = NIVEL_ROMANO_PARA_ARABICO.get(servidor["nivel"], servidor["nivel"])
        return servidor

    @staticmethod
    def info_base() -> dict:
        """Situação da base: total de servidores, data da última importação e arquivo de origem."""
        with conexao() as con:
            total = con.execute("SELECT COUNT(*) FROM servidores").fetchone()[0]
            meta = {l["chave"]: l["valor"] for l in con.execute("SELECT chave, valor FROM meta")}
        atualizada = meta.get("base_atualizada_em")
        return {
            "total": total,
            "atualizada_em": datetime.fromisoformat(atualizada) if atualizada else None,
            "arquivo": meta.get("base_arquivo"),
        }

    @staticmethod
    def importar_planilha(conteudo: bytes, nome_arquivo: str) -> ResultadoImportacao:
        """Substitui TODA a base de servidores pelo conteúdo da planilha (CSV ou XLSX).

        Tudo ou nada: se a planilha for inválida, a base atual permanece intacta.
        """
        df = _ler_planilha(conteudo, nome_arquivo)

        faltando = [c for c in COLUNAS_OBRIGATORIAS if c not in df.columns]
        if faltando:
            raise ErroImportacao("Colunas ausentes na planilha: " + ", ".join(faltando))

        registros: dict[str, tuple] = {}
        ignoradas = datas_invalidas = 0
        for linha in df.to_dict("records"):
            masp = _numero_inteiro_como_texto(linha["MASP"])
            admissao = _numero_inteiro_como_texto(linha["Nº Admissão"])
            if not masp or not admissao:
                ignoradas += 1
                continue

            data_inicio, erro_inicio = _parse_data(linha["Data Inicio"])
            data_fim, erro_fim = _parse_data(linha["Data Fim Efetiva"])
            datas_invalidas += erro_inicio + erro_fim

            chave = _texto(linha["Masp/Admissão"]) or f"{masp}/{admissao}"
            registros[chave] = (  # chave repetida: vale a última linha
                chave, _texto(linha["Nome Servidor"]), masp, admissao, data_inicio, data_fim,
                _texto(linha["Cod Carreira"]), _texto(linha["Símbolo Vencimento"]),
                _texto(linha["Nivel"]), _texto(linha["Grau"]),
                _parse_carga_horaria(linha["Carga Horária Pagamento"]),
            )

        if not registros:
            raise ErroImportacao("A planilha não tem nenhum servidor válido (MASP e Nº de Admissão preenchidos).")

        with conexao() as con:  # transação única: erro no meio desfaz tudo
            con.execute("DELETE FROM servidores")
            con.executemany(
                "INSERT INTO servidores (masp_admissao, nome, masp, numero_admissao, data_inicio, "
                "data_fim_efetiva, cod_carreira, simbolo_vencimento, nivel, grau, carga_horaria) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                list(registros.values()),
            )
            con.executemany(
                "INSERT INTO meta (chave, valor) VALUES (?, ?) "
                "ON CONFLICT(chave) DO UPDATE SET valor = excluded.valor",
                [
                    ("base_atualizada_em", datetime.now().isoformat(timespec="seconds")),
                    ("base_arquivo", nome_arquivo),
                ],
            )
        return ResultadoImportacao(len(registros), ignoradas, datas_invalidas)
