from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos
from data import ProvedorDadosFhemig

class CalculadoraGRSMeses(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: Valor GRS x Meses"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["grs_risco", "numero_meses"]

    def calcular(self, grs_risco: str, numero_meses: int) -> ResultadoCalculo:
        # Determinar o valor conforme seleção
        nivel =  "risco_medio" if "Médio" in grs_risco else "risco_alto"
        valor_grs = ProvedorDadosFhemig.obter_valor_grs(nivel)

        valor_meses = valor_grs * numero_meses
        memoria = [
            f"GRS ({grs_risco}): {FormatadorCampos.brl(valor_grs)}",
            f"x {numero_meses} meses",
            f"= {FormatadorCampos.brl(valor_meses)}",
        ]
        return ResultadoCalculo(valor=round(valor_meses,2), memoria_calculo=memoria)