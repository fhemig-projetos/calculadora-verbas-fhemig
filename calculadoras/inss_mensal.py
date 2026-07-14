from calculadoras import CalculadoraVerba, ResultadoCalculo
from data import ProvedorDadosFhemig
from utils import FormatadorCampos

class CalculadoraINSS(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "INSS = Vencimento Básico × Alíquota - Dedução (tabela progressiva)"

    @property
    def campos_necessarios(self):
        return ["vencimento_basico", "ano_referencia"]
    
    def calcular(self, vencimento_basico: float, ano_referencia: int) -> ResultadoCalculo:
        # Pega a tabela do ano escolhido pelo usuário
        tabela = ProvedorDadosFhemig.obter_tabela_inss(ano_referencia)

        # Percorre as faixas em ordem crescente
        for faixa in tabela:
            if vencimento_basico <= faixa["limite"]:
                # Fórmula
                valor = vencimento_basico * faixa["aliq"] - faixa["deducao"]
                # Memória de cálculo
                memoria = [
                    f"Vencimento: {FormatadorCampos.brl(vencimento_basico)}",
                    f"Faixa de {FormatadorCampos.brl(faixa['limite'])}: {faixa['aliq']*100:.1f}%",
                    f"Dedução: {FormatadorCampos.brl(faixa['deducao'])}",
                    f"= {FormatadorCampos.brl(valor)}",
                ]
                return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)
        
        # Se passou de todas (acima do teto) utiliza a última faixa
        ultima = tabela[-1]
        # Fórmula
        valor = vencimento_basico * ultima["aliq"] - ultima["deducao"]
        # Memória de cálculo
        memoria = [
            f"Vencimento: {FormatadorCampos.brl(vencimento_basico)}",
            f"Faixa de {FormatadorCampos.brl(ultima['limite'])}: {ultima['aliq']*100:.1f}%",
            f"Dedução: {FormatadorCampos.brl(ultima['deducao'])}",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)

