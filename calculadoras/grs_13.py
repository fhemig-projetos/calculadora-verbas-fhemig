from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraGRS13(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: Valor GRS ÷ 12 × Nº de Meses"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_grs", "numero_meses"]

    def calcular(self, valor_grs: float, numero_meses: int) -> ResultadoCalculo:
        valor = (valor_grs / 12) * numero_meses
        memoria = [
            f"GRS: {FormatadorCampos.brl(valor_grs)}",
            f"÷ 12 = {FormatadorCampos.brl(valor_grs/12)}/mês",
            f"× {numero_meses} meses",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)