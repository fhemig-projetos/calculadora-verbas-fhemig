from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraGIEFSDias(CalculadoraVerba):
    @property
    def descricao_formula(self):
        return "Fórmula: GIEFS Dias = (Valor Base ÷ 30) × Dias"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_base", "dias_trabalhados"]

    def calcular(self, valor_base: float, dias_trabalhados: int) -> ResultadoCalculo:
        valor = (valor_base/30)* dias_trabalhados
        memoria = [
            f"Valor GIEFS: {FormatadorCampos.brl(valor_base)}",
            f"÷ 30 = {FormatadorCampos.brl(valor_base/30)}",
            f"x {dias_trabalhados} dias",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor,2), memoria_calculo=memoria)
    