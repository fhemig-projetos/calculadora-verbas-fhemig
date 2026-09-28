from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos


class CalculadoraIPSEMG(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return ("Fórmula: (Venc. Básico + Grat. Fim Semana + Ab. Emergência + GIEFS + "
                "Ad. Noturno + GRS + 13º) × 3,2%")

    @property
    def campos_necessarios(self) -> list[str]:
        return [
            "vencimento_basico", "grat_final_semana", "abono_emergencia",
            "valor_giefs", "adicional_noturno", "valor_grs",
            "valor_13_salario",
        ]

    def calcular(
        self,
        vencimento_basico: float,
        grat_final_semana: float,
        abono_emergencia: float,
        valor_giefs: float,
        adicional_noturno: float,
        valor_grs: float,
        valor_13_salario: float,
    ) -> ResultadoCalculo:
        # Soma dos componentes que compõem a base de incidência
        base = (
            vencimento_basico + grat_final_semana + abono_emergencia +
            valor_giefs + adicional_noturno + valor_grs +
            valor_13_salario
        )

        # Fórmula: base × 3,2%
        valor = base * 0.032

        memoria = [
            f"Venc. Básico: {FormatadorCampos.brl(vencimento_basico)}",
            f"Grat. Fim Semana: {FormatadorCampos.brl(grat_final_semana)}",
            f"Abono Emergência: {FormatadorCampos.brl(abono_emergencia)}",
            f"GIEFS: {FormatadorCampos.brl(valor_giefs)}",
            f"Ad. Noturno: {FormatadorCampos.brl(adicional_noturno)}",
            f"GRS: {FormatadorCampos.brl(valor_grs)}",
            f"13º Salário: {FormatadorCampos.brl(valor_13_salario)}",
            f"─────────────────────",
            f"BASE de Incidência: {FormatadorCampos.brl(base)}",
            f"× 3,2% = {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)