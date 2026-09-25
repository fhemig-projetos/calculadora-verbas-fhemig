from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraGIEFSMeses(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: Valor GIEFS × Nº de Meses"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_giefs", "numero_meses"]

    def calcular(self, valor_giefs: float, numero_meses: int) -> ResultadoCalculo:
        valor = valor_giefs * numero_meses
        memoria = [
            f"Valor da GIEFS: {FormatadorCampos.brl(valor_giefs)}",
            f"x {numero_meses} meses",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)