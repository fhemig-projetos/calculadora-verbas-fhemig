from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos
from data import ProvedorDadosFhemig


class CalculadoraGRSDias(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: Valor GRS ÷ 30 × Dias Trabalhados no Mês"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["grs_risco", "dias_trabalhados"]

    def calcular(self, grs_risco: str, dias_trabalhados: int) -> ResultadoCalculo:
        # Busca o valor conforme seleção
        valor_grs = ProvedorDadosFhemig.obter_valor_grs(grs_risco)

        valor_diario = valor_grs / 30
        valor = valor_diario * dias_trabalhados
        memoria = [
            f"GRS ({grs_risco}): {FormatadorCampos.brl(valor_grs)}",
            f"÷ 30 = {FormatadorCampos.brl(valor_diario)}/dia",
            f"× {dias_trabalhados} dias",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)
