from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos
from data import ProvedorDadosFhemig


class CalculadoraAjudaCusto(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: Valor Diário x Dias Trabalhados"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["ajuda_custo_diario", "dias_trabalhados"]

    def calcular(
        self, ajuda_custo_diario: float, dias_trabalhados: int
    ) -> ResultadoCalculo:
        valor = ajuda_custo_diario * dias_trabalhados
        memoria = [
            f"Valor diário: {FormatadorCampos.brl(ajuda_custo_diario)}",
            f"x {dias_trabalhados} dias",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)
