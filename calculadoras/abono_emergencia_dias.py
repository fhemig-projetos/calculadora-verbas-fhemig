from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraAbonoEmergenciaDias(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: (Abono de Emergência ÷ 30) × Dias"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["abono_emergencia", "dias_trabalhados"]

    def calcular(self, abono_emergencia: float, dias_trabalhados: int) -> ResultadoCalculo:
        valor = (abono_emergencia / 30) * dias_trabalhados
        memoria = [
            f"Abono de Emergência: {FormatadorCampos.brl(abono_emergencia)}",
            f"÷ 30 = {FormatadorCampos.brl(abono_emergencia/30)}",
            f"x {dias_trabalhados} dias",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)
