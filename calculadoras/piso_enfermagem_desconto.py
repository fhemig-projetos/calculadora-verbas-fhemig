from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraPisoEnfermagemDesconto(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Campo livre — valor do desconto informado diretamente"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_piso"]

    def calcular(self, valor_piso: float) -> ResultadoCalculo:
        memoria = [
            f"Valor do Piso: {FormatadorCampos.brl(valor_piso)}",
        ]
        return ResultadoCalculo(valor=round(valor_piso, 2), memoria_calculo=memoria)
