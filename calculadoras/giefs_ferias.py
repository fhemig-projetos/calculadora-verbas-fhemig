#GIEFS — 1/3 de Férias

from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraGIEFSFerias(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: Valor GIEFS ÷ 3"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_giefs"]

    def calcular(self, valor_giefs: float) -> ResultadoCalculo:
        valor = valor_giefs / 3
        memoria = [
            f"Valor GIEFS: {FormatadorCampos.brl(valor_giefs)}",
            f"÷ 3 = {FormatadorCampos.brl(valor_giefs/3)}"
        ]
        return ResultadoCalculo(valor=round(valor,2),memoria_calculo=memoria)