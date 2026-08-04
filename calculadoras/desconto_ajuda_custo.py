from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraDescontoAjudaCusto(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: Valor que gerou o desconto × 4%"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_base_desconto"]

    def calcular(self, valor_base_desconto: float) -> ResultadoCalculo:
        valor = valor_base_desconto * 0.04
        memoria = [
            f"Valor base: {FormatadorCampos.brl(valor_base_desconto)}",
            f"× 4% = {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)