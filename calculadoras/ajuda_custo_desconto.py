from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraDescontoAjudaCusto(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: Valor da Ajuda de Custo × 4%"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_ajuda_custo"]

    def calcular(self, valor_ajuda_custo: float) -> ResultadoCalculo:
        valor = valor_ajuda_custo * 0.04
        memoria = [
            f"Valor da Ajuda de Custo: {FormatadorCampos.brl(valor_ajuda_custo)}",
            f"× 4% = {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)