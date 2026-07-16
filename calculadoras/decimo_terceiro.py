from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos
from data import ProvedorDadosFhemig

class CalculadoraDecimoTerceiro(CalculadoraVerba):
    @property
    def descricao_formula(self):
        return "13º = (Venc + Ad.Desemp + Ab.Emerg + GFS + Ad.Noturno + GRS) ÷ 12 × Nº Meses"
    
    @property
    def campos_necessarios(self):
        return ["vencimento_basico", "ad_desempenho", "abono_emergencia",
                "grat_final_semana", "adicional_noturno", "grs_risco", "numero_meses"]
    
    def _parser_nivel_grs(self, grs_risco: str):
        if "Médio" in grs_risco:
            nivel = "risco_medio"
        elif "Alto" in grs_risco:
            nivel = "risco_alto"
        else:
            nivel = "nao_faz_jus"
        return nivel

    def calcular(self, vencimento_basico: float, ad_desempenho: float, abono_emergencia: float, grat_final_semana: float, adicional_noturno: float, grs_risco: str, numero_meses: int) -> ResultadoCalculo:
        # Determina o valor conforme seleção
        nivel = self._parser_nivel_grs(grs_risco)
        valor_grs = ProvedorDadosFhemig.obter_valor_grs(nivel)

        # Fórmula
        base = (vencimento_basico + ad_desempenho + abono_emergencia +
        grat_final_semana + adicional_noturno + valor_grs)
        valor = (base / 12) * numero_meses

        memoria = [
            f"Venc. Básico: {FormatadorCampos.brl(vencimento_basico)}",
            f"Ad. Desempenho: {FormatadorCampos.brl(ad_desempenho)}",
            f"Abono Emergência: {FormatadorCampos.brl(abono_emergencia)}",
            f"Grat. Fim Semana: {FormatadorCampos.brl(grat_final_semana)}",
            f"Ad. Noturno: {FormatadorCampos.brl(adicional_noturno)}",
            f"GRS ({grs_risco}): {FormatadorCampos.brl(valor_grs)}",
            f"─────────────────────",
            f"BASE: {FormatadorCampos.brl(base)}",
            f"÷ 12 × {numero_meses} meses",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)
