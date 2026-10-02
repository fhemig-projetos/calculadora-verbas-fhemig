from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraAbonoEmergenciaMeses(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: Abono de Emergência × Nº de Meses"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["abono_emergencia", "numero_meses"]

    def calcular(self, abono_emergencia: float, numero_meses: int) -> ResultadoCalculo:
        valor = abono_emergencia * numero_meses
        memoria = [
            f"Abono de Emergência: {FormatadorCampos.brl(abono_emergencia)}",
            f"x {numero_meses} meses",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)
