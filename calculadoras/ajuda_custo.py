from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class _CalculadoraAjudaCusto(CalculadoraVerba):
    """Fórmula comum às parcelas fixa e variável da Ajuda de Custo: Valor Diário x Dias Trabalhados.

    As duas parcelas diferem só no campo do valor diário (cada uma com a própria chave, para o
    valor digitado numa não vazar para a outra ao trocar de verba) e no default dele (ver
    ui/selecao_verba.py).
    """
    campo_valor_diario: str  # definido nas subclasses

    @property
    def descricao_formula(self) -> str:
        return "Fórmula: Valor Diário x Dias Trabalhados"

    @property
    def campos_necessarios(self) -> list[str]:
        return [self.campo_valor_diario, "dias_trabalhados"]

    def calcular(self, **kwargs) -> ResultadoCalculo:
        ajuda_custo_diario = kwargs[self.campo_valor_diario]
        dias_trabalhados = kwargs["dias_trabalhados"]
        valor = ajuda_custo_diario * dias_trabalhados
        memoria = [
            f"Valor diário: {FormatadorCampos.brl(ajuda_custo_diario)}",
            f"x {dias_trabalhados} dias",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)


class CalculadoraAjudaCustoFixa(_CalculadoraAjudaCusto):
    """Código 3198 — valor diário previsto (default R$ 50,00, editável)."""
    campo_valor_diario = "ajuda_custo_fixa_diario"


class CalculadoraAjudaCustoVariavel(_CalculadoraAjudaCusto):
    """Código 2070 — valor diário livre (sem valor pré-definido)."""
    campo_valor_diario = "ajuda_custo_variavel_diario"
