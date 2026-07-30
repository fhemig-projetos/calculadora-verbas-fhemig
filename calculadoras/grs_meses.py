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

    def _parser_nivel_grs(self, grs_risco: str) -> str:
        if "Médio" in grs_risco:
            return "risco_medio"
        elif "Alto" in grs_risco:
            return "risco_alto"
        return "nao_faz_jus"

    def calcular(self, grs_risco: str, numero_meses: int) -> ResultadoCalculo:
        # Determinar o valor conforme seleção
        nivel = self._parser_nivel_grs(grs_risco)
        valor_grs = ProvedorDadosFhemig.obter_valor_grs(nivel)

        valor_meses = valor_grs * numero_meses
        memoria = [
            f"GRS ({grs_risco}): {FormatadorCampos.brl(valor_grs)}",
            f"x {numero_meses} meses",
            f"= {FormatadorCampos.brl(valor_meses)}",
        ]
        return ResultadoCalculo(valor=round(valor_meses,2), memoria_calculo=memoria)