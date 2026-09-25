from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraPlantaoMedicoComplementar(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Campo livre — valor do PMC informado diretamente"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_pmc"]

    def calcular(self, valor_pmc: float) -> ResultadoCalculo:
        memoria = [
            f"Valor do PMC: {FormatadorCampos.brl(valor_pmc)}",
        ]
        return ResultadoCalculo(valor=round(valor_pmc, 2), memoria_calculo=memoria)
