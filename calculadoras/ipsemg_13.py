from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraRestituicaoIPSEMG13(CalculadoraVerba):
    """Código 1549 — Vantagem. Campo livre (regra de cálculo ainda não definida pela unidade)."""
    @property
    def descricao_formula(self) -> str:
        return "Campo livre — valor da restituição informado diretamente"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_restituicao_ipsemg_13"]

    def calcular(self, valor_restituicao_ipsemg_13: float) -> ResultadoCalculo:
        memoria = [
            f"Valor da Restituição: {FormatadorCampos.brl(valor_restituicao_ipsemg_13)}",
        ]
        return ResultadoCalculo(valor=round(valor_restituicao_ipsemg_13, 2), memoria_calculo=memoria)


class CalculadoraIPSEMG13(CalculadoraVerba):
    """Código 7701 — Desconto. Campo livre (regra de cálculo ainda não definida pela unidade)."""
    @property
    def descricao_formula(self) -> str:
        return "Campo livre — valor do desconto informado diretamente"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_ipsemg_13"]

    def calcular(self, valor_ipsemg_13: float) -> ResultadoCalculo:
        memoria = [
            f"Valor do Desconto: {FormatadorCampos.brl(valor_ipsemg_13)}",
        ]
        return ResultadoCalculo(valor=round(valor_ipsemg_13, 2), memoria_calculo=memoria)
