from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos
from data import ProvedorDadosFhemig

class CalculadoraLicencaMaternidade(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: Venc. Básico + Valor GIEFS + Ab. Emergência + GRS"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["vencimento_basico", "valor_giefs", "abono_emergencia", "grs_risco"]

    def calcular(self, vencimento_basico: float, valor_giefs: float, abono_emergencia: float, grs_risco: str) -> ResultadoCalculo:
        valor_grs = ProvedorDadosFhemig.obter_valor_grs(grs_risco)
        valor = vencimento_basico + valor_giefs + abono_emergencia + valor_grs
        memoria = [
            f"Venc. Básico: {FormatadorCampos.brl(vencimento_basico)}",
            f"Valor GIEFS: {FormatadorCampos.brl(valor_giefs)}",
            f"Abono Emergência: {FormatadorCampos.brl(abono_emergencia)}",
            f"GRS ({grs_risco}): {FormatadorCampos.brl(valor_grs)}",
            f"─────────────────────",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)
