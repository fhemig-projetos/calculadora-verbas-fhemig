from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraTercoFerias(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: (Venc. Básico + Ab. Emergência + Ad. Noturno + GRS) ÷ 3"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["vencimento_basico", "abono_emergencia",
                "adicional_noturno", "valor_grs"]

    def calcular(self, vencimento_basico: float, abono_emergencia: float, adicional_noturno: float, valor_grs: float) -> ResultadoCalculo:
        # Fórmula
        base = (vencimento_basico + abono_emergencia +
                adicional_noturno + valor_grs)
        valor = base / 3

        memoria = [
            f"Venc. Básico: {FormatadorCampos.brl(vencimento_basico)}",
            f"Abono Emergência: {FormatadorCampos.brl(abono_emergencia)}",
            f"Ad. Noturno: {FormatadorCampos.brl(adicional_noturno)}",
            f"GRS: {FormatadorCampos.brl(valor_grs)}",
            f"─────────────────────",
            f"BASE: {FormatadorCampos.brl(base)}",
            f"÷ 3 = {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)