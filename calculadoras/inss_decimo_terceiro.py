from calculadoras import CalculadoraVerba, ResultadoCalculo
from data import ProvedorDadosFhemig
from utils import FormatadorCampos

class CalculadoraINSSDecimoTerceiro(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "INSS s/ 13º = (13º + GIEFS 13º) × Alíquota − Dedução (tabela progressiva)"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_13_salario", "giefs_13_salario", "ano_referencia"]
    
    def calcular(self, valor_13_salario: float, giefs_13_salario: float, ano_referencia: int) -> ResultadoCalculo:
        # Soma o 13º salário com a GIEFS do 13º
        base = valor_13_salario + giefs_13_salario

        # Pega a tabela do ano escolhido pelo usuário
        tabela = ProvedorDadosFhemig.obter_tabela_inss(ano_referencia)

        # Percorre as faixas em ordem crescente
        for faixa in tabela:
            if base <= faixa["limite"]:
                # Fórmula
                valor = base * faixa["aliq"] - faixa["deducao"]
                # Memória de cálculo
                memoria = [
                    f"13º Salário: {FormatadorCampos.brl(valor_13_salario)}",
                    f"GIEFS 13º: {FormatadorCampos.brl(giefs_13_salario)}",
                    f"─────",
                    f"BASE: {FormatadorCampos.brl(base)}",
                    f"Faixa de {FormatadorCampos.brl(faixa['limite'])}: {faixa['aliq']*100:.1f}%",
                    f"Dedução: {FormatadorCampos.brl(faixa['deducao'])}",
                    f"= {FormatadorCampos.brl(valor)}",
                ]
                return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)
        
        # Se passou de todas (acima do teto) utiliza a última faixa
        ultima = tabela[-1]
        valor = base * ultima["aliq"] - ultima["deducao"]
        memoria = [
            f"13º Salário: {FormatadorCampos.brl(valor_13_salario)}",
            f"GIEFS 13º: {FormatadorCampos.brl(giefs_13_salario)}",
            f"─────",
            f"BASE: {FormatadorCampos.brl(base)}",
            f"Faixa de {FormatadorCampos.brl(ultima['limite'])}: {ultima['aliq']*100:.1f}%",
            f"Dedução: {FormatadorCampos.brl(ultima['deducao'])}",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)