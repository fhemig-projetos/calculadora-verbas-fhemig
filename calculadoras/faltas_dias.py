from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraFaltasDias(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: (Venc. Básico + Ab. Emergência + GRS + Piso Enfermagem) ÷ 30 × Nº de Dias de Falta"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["vencimento_basico", "abono_emergencia", "valor_grs", "valor_piso", "faltas_dias"]

    def calcular(self, vencimento_basico: float, abono_emergencia: float, valor_grs: float, valor_piso: float, faltas_dias: int) -> ResultadoCalculo:
        base = vencimento_basico + abono_emergencia + valor_grs + valor_piso
        valor = base / 30 * faltas_dias
        memoria = [
            f"Venc. Básico: {FormatadorCampos.brl(vencimento_basico)}",
            f"Abono Emergência: {FormatadorCampos.brl(abono_emergencia)}",
            f"GRS: {FormatadorCampos.brl(valor_grs)}",
            f"Piso Enfermagem: {FormatadorCampos.brl(valor_piso)}",
            f"─────────────────────",
            f"BASE: {FormatadorCampos.brl(base)}",
            f"÷ 30 = {FormatadorCampos.brl(base / 30)}",
            f"× {faltas_dias} dias de falta",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor,2), memoria_calculo=memoria)