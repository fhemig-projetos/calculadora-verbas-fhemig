from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraFaltasHoras(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: (Venc. Básico + Ab. Emergência + GRS + Piso Enfermagem) ÷ Carga Horária Mensal × Horas Descontadas"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["vencimento_basico", "abono_emergencia", "valor_grs", "valor_piso", "carga_horaria_mensal", "faltas_horas"]

    def calcular(self, vencimento_basico: float, abono_emergencia: float, valor_grs: float, valor_piso: float, carga_horaria_mensal: int, faltas_horas: int) -> ResultadoCalculo:
        base = vencimento_basico + abono_emergencia + valor_grs + valor_piso
        valor = base / carga_horaria_mensal * faltas_horas
        memoria = [
            f"Venc. Básico: {FormatadorCampos.brl(vencimento_basico)}",
            f"Abono Emergência: {FormatadorCampos.brl(abono_emergencia)}",
            f"GRS: {FormatadorCampos.brl(valor_grs)}",
            f"Piso Enfermagem: {FormatadorCampos.brl(valor_piso)}",
            f"─────────────────────",
            f"BASE: {FormatadorCampos.brl(base)}",
            f"÷ {carga_horaria_mensal} = {FormatadorCampos.brl(base / carga_horaria_mensal)}",
            f"× {faltas_horas} horas de falta",
            f"= {FormatadorCampos.brl(valor)}"
        ]
        return ResultadoCalculo(valor=round(valor,2), memoria_calculo=memoria)