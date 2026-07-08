from calculadoras import CalculadoraVerba, ResultadoCalculo
from data import ProvedorDadosFhemig
class CalculadoraINSS(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "INSS = Vencimento Básico × Alíquota - Dedução (tabela progressiva)"

    @property
    def campos_necessarios(self):
        return ["vencimento_basico"]
    
    def calcular(self, vencimento_basico: float) -> ResultadoCalculo:
        # Pega a tabela do ano corrente
        tabela = ProvedorDadosFhemig.obter_tabela_inss(2026)
