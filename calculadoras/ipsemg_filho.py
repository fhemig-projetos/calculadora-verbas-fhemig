from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraIPSEMGFilhoMenor21(CalculadoraVerba):
    """1419 (restituição, Vantagem) e 9619 (atraso, Desconto): campo editável, regra geral R$ 60 por filho."""
    @property
    def descricao_formula(self) -> str:
        return "Campo editável — regra geral: R$ 60,00 por filho menor de 21 anos"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_ipsemg_filho_menor21"]

    def calcular(self, valor_ipsemg_filho_menor21: float) -> ResultadoCalculo:
        memoria = [f"Valor (filho menor de 21 anos): {FormatadorCampos.brl(valor_ipsemg_filho_menor21)}"]
        return ResultadoCalculo(valor=round(valor_ipsemg_filho_menor21, 2), memoria_calculo=memoria)


class CalculadoraIPSEMGFilho21a39(CalculadoraVerba):
    """815 (restituição, Vantagem) e 8115 (atraso, Desconto): campo editável, regra geral R$ 90 por filho."""
    @property
    def descricao_formula(self) -> str:
        return "Campo editável — regra geral: R$ 90,00 por filho de 21 a 39 anos"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_ipsemg_filho_21_39"]

    def calcular(self, valor_ipsemg_filho_21_39: float) -> ResultadoCalculo:
        memoria = [f"Valor (filho de 21 a 39 anos): {FormatadorCampos.brl(valor_ipsemg_filho_21_39)}"]
        return ResultadoCalculo(valor=round(valor_ipsemg_filho_21_39, 2), memoria_calculo=memoria)
