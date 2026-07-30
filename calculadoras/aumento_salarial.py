from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraAumentoSalarial(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: Venc. Básico × 4,62%"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["vencimento_basico"]

    def calcular(self, vencimento_basico: float) -> ResultadoCalculo:
        aumento = vencimento_basico * 0.0462
        novo_valor = vencimento_basico + aumento
        memoria = [
            f"Valor atual: {FormatadorCampos.brl(vencimento_basico)}",
            f"× 4,62% = {FormatadorCampos.brl(aumento)}",
            f"Novo valor: {FormatadorCampos.brl(novo_valor)}",
        ]
        return ResultadoCalculo(valor=round(aumento, 2), memoria_calculo=memoria)