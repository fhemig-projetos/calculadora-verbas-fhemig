from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos
from data import ProvedorDadosFhemig


class CalculadoraGRS13(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: Valor GRS ÷ 12 × Nº de Meses"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["grs_risco", "numero_meses"]

    def calcular(self, grs_risco: str, numero_meses: int) -> ResultadoCalculo:
        valor_grs = ProvedorDadosFhemig.obter_valor_grs(grs_risco)

        valor = (valor_grs / 12) * numero_meses
        memoria = [
            f"GRS ({grs_risco}): {FormatadorCampos.brl(valor_grs)}",
            f"÷ 12 = {FormatadorCampos.brl(valor_grs/12)}/mês",
            f"× {numero_meses} meses",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)
