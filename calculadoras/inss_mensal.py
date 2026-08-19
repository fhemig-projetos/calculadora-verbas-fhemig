from calculadoras import CalculadoraVerba, ResultadoCalculo
from data import ProvedorDadosFhemig
from utils import FormatadorCampos

class CalculadoraINSS(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return ("Fórmula: (Venc. Básico + Outras Vantagens + Outras Verbas) × "
                "Alíquota - Dedução (Tabela Progressiva)")

    @property
    def campos_necessarios(self):
        return ["vencimento_basico", "valor_outras_vantagens", "outras_verbas", "ano_referencia"]

    def calcular(
        self,
        vencimento_basico: float,
        valor_outras_vantagens: float,
        outras_verbas: float,
        ano_referencia: int,
    ) -> ResultadoCalculo:
        # Base de incidência: vencimento + demais vantagens do histórico + outras verbas informadas manualmente
        base = vencimento_basico + valor_outras_vantagens + outras_verbas

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
            f"Venc. Básico: {FormatadorCampos.brl(vencimento_basico)}",
            f"Outras Vantagens (soma do histórico): {FormatadorCampos.brl(valor_outras_vantagens)}",
            f"Outras Verbas: {FormatadorCampos.brl(outras_verbas)}",
            f"─────────────────────",
            f"BASE de Incidência: {FormatadorCampos.brl(base)}",
            f"Faixa de {FormatadorCampos.brl(faixa['limite'])}: {faixa['aliq']*100:.1f}%",
            f"Dedução: {FormatadorCampos.brl(faixa['deducao'])}",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)
