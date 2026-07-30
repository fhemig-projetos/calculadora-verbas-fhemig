from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos
from data import ProvedorDadosFhemig

class CalculadoraFeriasIndenizadas(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: (Venc. Básico + GIEFS + Ab. Emergência + GRS + Ad. Noturno) ÷ 30 × Nº de Dias de Férias Indenizadas" # no documento não fala para somar GIEFS

    @property
    def campos_necessarios(self) -> list[str]:
        return ["vencimento_basico", "valor_giefs", "abono_emergencia", "grs_risco", "adicional_noturno", "dias_ferias_indenizadas"]

    def _parser_nivel_grs(self, grs_risco: str) -> str:
        if "Médio" in grs_risco:
            return "risco_medio"
        elif "Alto" in grs_risco:
            return "risco_alto"
        return "nao_faz_jus"

    def calcular(self, vencimento_basico: float, valor_giefs: float, abono_emergencia: float, grs_risco: str, adicional_noturno: float, dias_ferias_indenizadas: int) -> ResultadoCalculo:
        nivel = self._parser_nivel_grs(grs_risco)
        valor_grs = ProvedorDadosFhemig.obter_valor_grs(nivel)
        base = (vencimento_basico + valor_giefs + abono_emergencia + valor_grs + adicional_noturno)
        valor = base / 30 * dias_ferias_indenizadas
        memoria = [
            f"Venc. Básico: {FormatadorCampos.brl(vencimento_basico)}",
            f"GIEFS: {FormatadorCampos.brl(valor_giefs)}",
            f"Abono Emergência: {FormatadorCampos.brl(abono_emergencia)}",
            f"GRS ({grs_risco}): {FormatadorCampos.brl(valor_grs)}",
            f"Ad. Noturno: {FormatadorCampos.brl(adicional_noturno)}",
            f"─────────────────────",
            f"BASE: {FormatadorCampos.brl(base)}",
            f"÷ 30 = {FormatadorCampos.brl(base / 30)}/dia",
            f"× {dias_ferias_indenizadas} dias de férias indenizadas",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)
