from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraGIEFSDias(CalculadoraVerba):
    @property
    def descricao_formula(self):
        return "Fórmula: (Valor GIEFS ÷ 30) × Dias"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_giefs", "dias_trabalhados"]

    def calcular(self, valor_giefs: float, dias_trabalhados: int) -> ResultadoCalculo:
        valor = (valor_giefs/30)* dias_trabalhados
        memoria = [
            f"Valor GIEFS: {FormatadorCampos.brl(valor_giefs)}",
            f"÷ 30 = {FormatadorCampos.brl(valor_giefs/30)}",
            f"x {dias_trabalhados} dias",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor,2), memoria_calculo=memoria)