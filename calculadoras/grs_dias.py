from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraGRSDias(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: Valor GRS ÷ 30 × Dias Trabalhados no Mês"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_grs", "dias_trabalhados"]

    def calcular(self, valor_grs: float, dias_trabalhados: int) -> ResultadoCalculo:
        valor_diario = valor_grs / 30
        valor = valor_diario * dias_trabalhados
        memoria = [
            f"GRS: {FormatadorCampos.brl(valor_grs)}",
            f"÷ 30 = {FormatadorCampos.brl(valor_diario)}/dia",
            f"× {dias_trabalhados} dias",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)