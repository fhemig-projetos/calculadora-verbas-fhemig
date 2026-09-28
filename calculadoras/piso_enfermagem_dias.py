from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraPisoEnfermagemDias(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: (Valor do Piso ÷ 30) × Dias"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_piso", "dias_trabalhados"]

    def calcular(self, valor_piso: float, dias_trabalhados: int) -> ResultadoCalculo:
        valor = (valor_piso / 30) * dias_trabalhados
        memoria = [
            f"Valor do Piso: {FormatadorCampos.brl(valor_piso)}",
            f"÷ 30 = {FormatadorCampos.brl(valor_piso/30)}",
            f"x {dias_trabalhados} dias",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)
