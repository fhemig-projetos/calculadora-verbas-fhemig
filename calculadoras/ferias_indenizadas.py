from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos
from data import ProvedorDadosFhemig


class CalculadoraFeriasIndenizadas(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: (Venc. Básico + Ab. Emergência + GRS + Ad. Noturno) ÷ 30 × Nº de Dias de Férias Indenizadas"

    @property
    def campos_necessarios(self) -> list[str]:
        return [
            "vencimento_basico",
            "abono_emergencia",
            "grs_risco",
            "adicional_noturno",
            "dias_ferias_indenizadas",
        ]

    def calcular(
        self,
        vencimento_basico: float,
        abono_emergencia: float,
        grs_risco: str,
        adicional_noturno: float,
        dias_ferias_indenizadas: int,
    ) -> ResultadoCalculo:
        valor_grs = ProvedorDadosFhemig.obter_valor_grs(grs_risco)
        base = vencimento_basico + abono_emergencia + valor_grs + adicional_noturno
        valor = base / 30 * dias_ferias_indenizadas
        memoria = [
            f"Venc. Básico: {FormatadorCampos.brl(vencimento_basico)}",
            f"Abono Emergência: {FormatadorCampos.brl(abono_emergencia)}",
            f"GRS ({grs_risco}): {FormatadorCampos.brl(valor_grs)}",
            f"Ad. Noturno: {FormatadorCampos.brl(adicional_noturno)}",
            f"─────────────────────",
            f"BASE: {FormatadorCampos.brl(base)}",
            f"÷ 30 = {FormatadorCampos.brl(base / 30)}/dia",
            f"× {dias_ferias_indenizadas} dias de férias indenizadas",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)
