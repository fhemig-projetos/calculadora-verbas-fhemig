from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraGRSMeses(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: Valor GRS x Meses"
    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_grs", "numero_meses"]

    def calcular(self, valor_grs: float, numero_meses: int) -> ResultadoCalculo:
        valor_meses = valor_grs * numero_meses
        memoria = [
            f"GRS: {FormatadorCampos.brl(valor_grs)}",
            f"x {numero_meses} meses",
            f"= {FormatadorCampos.brl(valor_meses)}",
        ]
        return ResultadoCalculo(valor=round(valor_meses,2), memoria_calculo=memoria)