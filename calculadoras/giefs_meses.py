from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraGIEFSMeses(CalculadoraVerba):
    @property
    def descricao_formula(self):
        return "Fórmula: GIEFS Meses = (Valor Base ÷ 6) × Parcelas"
    
    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_base", "numero_parcelas"]

    def calcular(self, valor_base: float, numero_parcelas: int) -> ResultadoCalculo:
        valor = (valor_base/6) * numero_parcelas
        memoria = [
            f"Valor GIEFS: {FormatadorCampos.brl(valor_base)}",
            f"÷ 6 = {FormatadorCampos.brl(valor_base/6)}",
            f"x {numero_parcelas} parcelas",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor,2),memoria_calculo=memoria)