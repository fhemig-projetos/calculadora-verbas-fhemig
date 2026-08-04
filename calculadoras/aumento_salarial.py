from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos
from data import ProvedorDadosFhemig

class CalculadoraAumentoSalarial(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: Venc. Básico × alíquota de reajuste"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["ano_reajuste", "vencimento_basico"]

    def calcular(self, ano_reajuste: str, vencimento_basico: float) -> ResultadoCalculo:
        aliquota = ProvedorDadosFhemig.obter_aliquota_reajuste(ano_reajuste)
        aumento = vencimento_basico * aliquota
        novo_valor = vencimento_basico + aumento
        memoria = [
            f"Valor atual: {FormatadorCampos.brl(vencimento_basico)}",
            f"× {aliquota*100:.2f}% = {FormatadorCampos.brl(aumento)}",
            f"Novo valor: {FormatadorCampos.brl(novo_valor)}",
        ]
        return ResultadoCalculo(valor=round(aumento, 2), memoria_calculo=memoria)