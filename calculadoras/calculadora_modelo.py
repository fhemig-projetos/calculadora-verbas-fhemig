from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos
from data import ProvedorDadosFhemig

class CalculadoraGRSDescontoHoras(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return ""

    @property
    def campos_necessarios(self) -> list[str]:
        return ["", ""]

    def calcular(self) -> ResultadoCalculo:
        valor = ""
        memoria = []
        return ResultadoCalculo(valor=round(valor,2), memoria_calculo=memoria)