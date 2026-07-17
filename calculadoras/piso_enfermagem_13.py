from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraPisoEnfermagem13(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: Valor do Piso de Enfermagem ÷ 12 × Nº de Meses"
    
    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_piso", "numero_meses"]
    
    def calcular(self, valor_piso: float, numero_meses: int) -> ResultadoCalculo:
        valor = (valor_piso / 12) * numero_meses
        memoria = [
            f"Valor do Piso Enfermagem: {FormatadorCampos.brl(valor_piso)}",
            f"÷ 12 = {FormatadorCampos.brl(valor_piso/12)}/mês",
            f"× {numero_meses} meses",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor,2), memoria_calculo=memoria)