from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraVencimentoBasicoDias(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: (Venc. Básico ÷ 30) × Dias"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["vencimento_basico", "dias_trabalhados"]

    def calcular(self, vencimento_basico: float, dias_trabalhados: int) -> ResultadoCalculo:
        valor = (vencimento_basico / 30) * dias_trabalhados
        memoria = [
            f"Venc. Básico: {FormatadorCampos.brl(vencimento_basico)}",
            f"÷ 30 = {FormatadorCampos.brl(vencimento_basico/30)}",
            f"x {dias_trabalhados} dias",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)
