from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraDecimoTerceiro(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: (Venc. Básico + Ab. Emergência + Grat. Fim Semana + Ad. Noturno + GRS) ÷ 12 × Nº de Meses"

    @property
    def campos_necessarios(self):
        return ["vencimento_basico", "abono_emergencia",
                "grat_final_semana", "adicional_noturno", "valor_grs", "numero_meses"]

    def calcular(self, vencimento_basico: float, abono_emergencia: float, grat_final_semana: float, adicional_noturno: float, valor_grs: float, numero_meses: int) -> ResultadoCalculo:
        # Fórmula
        base = (vencimento_basico + abono_emergencia +
        grat_final_semana + adicional_noturno + valor_grs)
        valor = (base / 12) * numero_meses

        memoria = [
            f"Venc. Básico: {FormatadorCampos.brl(vencimento_basico)}",
            f"Abono Emergência: {FormatadorCampos.brl(abono_emergencia)}",
            f"Grat. Fim Semana: {FormatadorCampos.brl(grat_final_semana)}",
            f"Ad. Noturno: {FormatadorCampos.brl(adicional_noturno)}",
            f"GRS: {FormatadorCampos.brl(valor_grs)}",
            f"─────────────────────",
            f"BASE: {FormatadorCampos.brl(base)}",
            f"÷ 12 × {numero_meses} meses",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)
