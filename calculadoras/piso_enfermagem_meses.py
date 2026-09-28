from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraPisoEnfermagemMeses(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: Valor do Piso × Nº de Meses"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_piso", "numero_meses"]

    def calcular(self, valor_piso: float, numero_meses: int) -> ResultadoCalculo:
        valor = valor_piso * numero_meses
        memoria = [
            f"Valor do Piso: {FormatadorCampos.brl(valor_piso)}",
            f"x {numero_meses} meses",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)
