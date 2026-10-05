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


class CalculadoraRestituicaoAuxilioTransporte(CalculadoraVerba):
    """Código 948 — Vantagem. Campo livre (regra de cálculo ainda não definida pela unidade)."""
    @property
    def descricao_formula(self) -> str:
        return "Campo livre — valor da restituição informado diretamente"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_restituicao_aux_transporte"]

    def calcular(self, valor_restituicao_aux_transporte: float) -> ResultadoCalculo:
        memoria = [
            f"Valor da Restituição: {FormatadorCampos.brl(valor_restituicao_aux_transporte)}",
        ]
        return ResultadoCalculo(valor=round(valor_restituicao_aux_transporte, 2), memoria_calculo=memoria)


class CalculadoraCusteioAuxilioTransporte(CalculadoraVerba):
    """Código 8849 — Desconto. Campo livre (regra de cálculo ainda não definida pela unidade)."""
    @property
    def descricao_formula(self) -> str:
        return "Campo livre — valor do desconto informado diretamente"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_custeio_aux_transporte"]

    def calcular(self, valor_custeio_aux_transporte: float) -> ResultadoCalculo:
        memoria = [
            f"Valor do Desconto: {FormatadorCampos.brl(valor_custeio_aux_transporte)}",
        ]
        return ResultadoCalculo(valor=round(valor_custeio_aux_transporte, 2), memoria_calculo=memoria)
