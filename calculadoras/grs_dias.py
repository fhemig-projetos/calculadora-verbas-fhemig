from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos
from data import ProvedorDadosFhemig

class CalculadoraGRSDias(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "GRS Proporcional aos Dias Trabalhados = Valor GRS ÷ 30 × Dias Trabalhados no Mês"
    
    @property
    def campos_necessarios(self) -> list[str]:
        return ["grs_risco", "dias_trabalhados"]
    
    def calcular(self, grs_risco: str, dias_trabalhados: int) -> ResultadoCalculo:
        # Determina o valor conforme seleção
        nivel = "risco_medio" if "Médio" in grs_risco else "risco_alto"
        valor_grs = ProvedorDadosFhemig.obter_valor_grs(nivel)

        valor_diario = valor_grs / 30
        valor = valor_diario * dias_trabalhados
        memoria = [
            f"GRS ({grs_risco}): {FormatadorCampos.brl(valor_grs)}",
            f"÷ 30 = {FormatadorCampos.brl(valor_diario)}/dia",
            f"× {dias_trabalhados} dias",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)


