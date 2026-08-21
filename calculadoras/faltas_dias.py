from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos
from data import ProvedorDadosFhemig


class CalculadoraFaltasDias(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: (Venc. Básico + Ad. Desempenho + Ab. Emergência + GRS + Piso Enfermagem) ÷ 30 × Nº de Dias de Falta"

    @property
    def campos_necessarios(self) -> list[str]:
        return [
            "vencimento_basico",
            "ad_desempenho",
            "abono_emergencia",
            "grs_risco",
            "valor_piso",
            "faltas_dias",
        ]

    def calcular(
        self,
        vencimento_basico: float,
        ad_desempenho: float,
        abono_emergencia: float,
        grs_risco: str,
        valor_piso: float,
        faltas_dias: int,
    ) -> ResultadoCalculo:
        valor_grs = ProvedorDadosFhemig.obter_valor_grs(grs_risco)
        base = (
            vencimento_basico
            + ad_desempenho
            + abono_emergencia
            + valor_grs
            + valor_piso
        )
        valor = base / 30 * faltas_dias
        memoria = [
            f"Venc. Básico: {FormatadorCampos.brl(vencimento_basico)}",
            f"Ad. Desempenho: {FormatadorCampos.brl(ad_desempenho)}",
            f"Abono Emergência: {FormatadorCampos.brl(abono_emergencia)}",
            f"GRS ({grs_risco}): {FormatadorCampos.brl(valor_grs)}",
            f"Piso Enfermagem: {FormatadorCampos.brl(valor_piso)}",
            f"─────────────────────",
            f"BASE: {FormatadorCampos.brl(base)}",
            f"÷ 30 = {FormatadorCampos.brl(base / 30)}",
            f"× {faltas_dias} dias de falta",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)
