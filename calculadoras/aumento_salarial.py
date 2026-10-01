from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos
from data import ProvedorDadosFhemig

class CalculadoraAumentoSalarial(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return (
            "Fórmula: Venc. Básico reajustado."
        )

    @property
    def campos_necessarios(self) -> list[str]:
        return ["ano_referencia_aumento", "vencimento_basico"]

    def calcular(self, ano_referencia_aumento: int, vencimento_basico: float) -> ResultadoCalculo:
        reajustes = ProvedorDadosFhemig.obter_reajustes_a_partir_de(ano_referencia_aumento)

        valor_atual = vencimento_basico
        memoria = [f"Valor atual: {FormatadorCampos.brl(vencimento_basico)}"]
        for ano, aliquota in reajustes:
            valor_reajustado = valor_atual * (1 + aliquota)
            memoria.append(
                f"Reajuste {ano}: {FormatadorCampos.brl(valor_atual)} × {aliquota*100:.2f}% "
                f"= {FormatadorCampos.brl(valor_reajustado - valor_atual)} "
                f"→ {FormatadorCampos.brl(valor_reajustado)}"
            )
            valor_atual = valor_reajustado

        aumento = valor_atual - vencimento_basico
        memoria.append(f"Novo valor: {FormatadorCampos.brl(valor_atual)}")
        memoria.append(f"Aumento (novo valor − atual): {FormatadorCampos.brl(aumento)}")
        return ResultadoCalculo(valor=round(aumento, 2), memoria_calculo=memoria)
