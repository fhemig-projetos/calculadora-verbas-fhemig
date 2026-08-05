from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraGIEFSMeses(CalculadoraVerba):
    @property
    def descricao_formula(self):
        return "Fórmula: (Valor GIEFS ÷ 6) × Parcelas"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_giefs", "numero_parcelas"]

    def calcular(self, valor_giefs: float, numero_parcelas: int) -> ResultadoCalculo:
        valor = (valor_giefs/6) * numero_parcelas
        memoria = [
            f"Valor GIEFS: {FormatadorCampos.brl(valor_giefs)}",
            f"÷ 6 = {FormatadorCampos.brl(valor_giefs/6)}",
            f"x {numero_parcelas} parcelas",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor,2),memoria_calculo=memoria)