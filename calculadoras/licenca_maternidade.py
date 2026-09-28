from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraLicencaMaternidade(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: Venc. Básico + Valor GIEFS + Ab. Emergência + GRS"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["vencimento_basico", "valor_giefs", "abono_emergencia", "valor_grs"]

    def calcular(self, vencimento_basico: float, valor_giefs: float, abono_emergencia: float, valor_grs: float) -> ResultadoCalculo:
        valor = vencimento_basico + valor_giefs + abono_emergencia + valor_grs
        memoria = [
            f"Venc. Básico: {FormatadorCampos.brl(vencimento_basico)}",
            f"Valor GIEFS: {FormatadorCampos.brl(valor_giefs)}",
            f"Abono Emergência: {FormatadorCampos.brl(abono_emergencia)}",
            f"GRS: {FormatadorCampos.brl(valor_grs)}",
            f"─────────────────────",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)
