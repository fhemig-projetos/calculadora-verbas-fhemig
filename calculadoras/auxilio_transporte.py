from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraAuxilioTransporte(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Campo livre — valor do auxílio transporte informado diretamente"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_auxilio_transporte"]

    def calcular(self, valor_auxilio_transporte: float) -> ResultadoCalculo:
        memoria = [
            f"Valor do Auxílio Transporte: {FormatadorCampos.brl(valor_auxilio_transporte)}",
        ]
        return ResultadoCalculo(valor=round(valor_auxilio_transporte, 2), memoria_calculo=memoria)
