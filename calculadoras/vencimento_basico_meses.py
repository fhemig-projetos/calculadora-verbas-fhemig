from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraVencimentoBasicoMeses(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: Venc. Básico × Nº de Meses"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["vencimento_basico", "numero_meses"]

    def calcular(self, vencimento_basico: float, numero_meses: int) -> ResultadoCalculo:
        valor = vencimento_basico * numero_meses
        memoria = [
            f"Venc. Básico: {FormatadorCampos.brl(vencimento_basico)}",
            f"x {numero_meses} meses",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)
