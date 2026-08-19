from calculadoras import CalculadoraVerba, ResultadoCalculo
from data import ProvedorDadosFhemig
from utils import FormatadorCampos

class CalculadoraINSSDecimoTerceiro(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: (13º + GIEFS 13º) × Alíquota − Dedução (Tabela Progressiva)"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_13_salario", "giefs_13_salario", "ano_referencia"]
    
    def calcular(self, valor_13_salario: float, giefs_13_salario: float, ano_referencia: int) -> ResultadoCalculo:
        # Soma o 13º salário com a GIEFS do 13º
        base = valor_13_salario + giefs_13_salario

        # Pega a tabela do ano escolhido pelo usuário
        tabela = ProvedorDadosFhemig.obter_tabela_inss(ano_referencia)

        # Percorre as faixas em ordem crescente (usa a última faixa se acima do teto)
        faixa = None
        for f in tabela:
            if base <= f["limite"]:
                faixa = f
                break
        if faixa is None:
            faixa = tabela[-1]

        valor = base * faixa["aliq"] - faixa["deducao"]

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