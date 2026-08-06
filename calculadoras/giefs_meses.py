from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraGIEFSMeses(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Valor total da GIEFS para o período"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_giefs"]

    def calcular(self, valor_giefs: float) -> ResultadoCalculo:
        memoria = [
            f"Valor da GIEFS: {FormatadorCampos.brl(valor_giefs)}",
        ]
        return ResultadoCalculo(valor=round(valor_giefs, 2), memoria_calculo=memoria)