from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos
from data import ProvedorDadosFhemig

class CalculadoraFaltasDias(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: (Venc. Básico + Ad. Desempenho + Ab. Emergência + GRS) ÷ Carga Horária × Dias Descontados" # no documento fala p somar também 1154 - COMPLEMENTO PISO ENFERMAGEM LEI 14434/22 (CPE) e dividir por 30 * quantidade dias falta


    @property
    def campos_necessarios(self) -> list[str]:
        return ["vencimento_basico", "carga_horaria_mensal", "dias_falta", "ad_desempenho", "abono_emergencia", "grs_risco"]

    def calcular(self, vencimento_basico: float, carga_horaria_mensal: int, dias_falta: int, ad_desempenho: float, abono_emergencia: float, grs_risco: str) -> ResultadoCalculo:
        nivel = self._parser_nivel_grs(grs_risco)
        valor_grs = ProvedorDadosFhemig.obter_valor_grs(nivel)
        base = vencimento_basico + ad_desempenho + abono_emergencia + valor_grs
        valor = base / carga_horaria_mensal * dias_falta
        memoria = [
            f"Venc. Básico: {FormatadorCampos.brl(vencimento_basico)}",
            f"Ad. Desempenho: {FormatadorCampos.brl(ad_desempenho)}",
            f"Abono Emergência: {FormatadorCampos.brl(abono_emergencia)}",
            f"GRS ({grs_risco}): {FormatadorCampos.brl(valor_grs)}",
            f"─────────────────────",
            f"BASE: {FormatadorCampos.brl(base)}",
            f"÷ {carga_horaria_mensal} = {FormatadorCampos.brl(base / carga_horaria_mensal)}",
            f"× {dias_falta} dias de falta",
            f"= {FormatadorCampos.brl(valor)}"
        ]
        return ResultadoCalculo(valor=round(valor,2), memoria_calculo=memoria)