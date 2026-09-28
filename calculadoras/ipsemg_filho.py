from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraIPSEMGFilho(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Campo livre — valor do desconto informado diretamente"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_ipsemg_filho"]

    def calcular(self, valor_ipsemg_filho: float) -> ResultadoCalculo:
        memoria = [
            f"Valor do Desconto: {FormatadorCampos.brl(valor_ipsemg_filho)}",
        ]
        return ResultadoCalculo(valor=round(valor_ipsemg_filho, 2), memoria_calculo=memoria)
