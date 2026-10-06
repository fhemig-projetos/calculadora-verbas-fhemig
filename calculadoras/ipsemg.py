from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos


class CalculadoraIPSEMG(CalculadoraVerba):
    """1411/7801 (titular) e 816/8116 (cônjuge, pais e irmãos dependentes): mesma fórmula, só muda tipo/código."""
    @property
    def descricao_formula(self) -> str:
        return ("Fórmula: (Venc. Básico + Grat. Fim Semana + Ab. Emergência + GIEFS + "
                "Ad. Noturno + GRS) × 3,2% (sem o 13º, que tem verba própria)")

    @property
    def campos_necessarios(self) -> list[str]:
        return [
            "vencimento_basico", "grat_final_semana", "abono_emergencia",
            "valor_giefs", "adicional_noturno", "valor_grs",
        ]

    def calcular(
        self,
        vencimento_basico: float,
        grat_final_semana: float,
        abono_emergencia: float,
        valor_giefs: float,
        adicional_noturno: float,
        valor_grs: float,
    ) -> ResultadoCalculo:
        # Soma dos componentes que compõem a base de incidência
        base = (
            vencimento_basico + grat_final_semana + abono_emergencia +
            valor_giefs + adicional_noturno + valor_grs
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
            f"─────────────────────",
            f"BASE de Incidência: {FormatadorCampos.brl(base)}",
            f"× 3,2% = {FormatadorCampos.brl(valor)}",
            "Obs.: mínimo (R$ 60), máximo (R$ 500), adicional de 1% (59+ anos) e regra de renda baixa não aplicados.",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)
