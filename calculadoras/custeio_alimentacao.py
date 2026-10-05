from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraRestituicaoCusteioAlimentacao(CalculadoraVerba):
    """Código 3018 — Vantagem. Campo livre (regra de cálculo ainda não definida pela unidade)."""
    @property
    def descricao_formula(self) -> str:
        return "Campo livre — valor da restituição informado diretamente"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_restituicao_custeio_alimentacao"]

    def calcular(self, valor_restituicao_custeio_alimentacao: float) -> ResultadoCalculo:
        memoria = [
            f"Valor da Restituição: {FormatadorCampos.brl(valor_restituicao_custeio_alimentacao)}",
        ]
        return ResultadoCalculo(valor=round(valor_restituicao_custeio_alimentacao, 2), memoria_calculo=memoria)


class CalculadoraCusteioAlimentacao(CalculadoraVerba):
    """Código 9018 — Desconto. Campo livre (regra de cálculo ainda não definida pela unidade)."""
    @property
    def descricao_formula(self) -> str:
        return "Campo livre — valor do desconto informado diretamente"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_custeio_alimentacao"]

    def calcular(self, valor_custeio_alimentacao: float) -> ResultadoCalculo:
        memoria = [
            f"Valor do Desconto: {FormatadorCampos.brl(valor_custeio_alimentacao)}",
        ]
        return ResultadoCalculo(valor=round(valor_custeio_alimentacao, 2), memoria_calculo=memoria)
