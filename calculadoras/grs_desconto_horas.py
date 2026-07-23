from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos
from data import ProvedorDadosFhemig

class CalculadoraGRSDescontoHoras(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: GRS ÷ CH × horas_falta"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["grs_risco", "carga_horaria_mensal", "horas_realizadas"]
    
    def _parser_nivel_grs(self, grs_risco: str):
        if "Médio" in grs_risco:
            return "risco_medio"
        elif "Alto" in grs_risco:
            return "risco_alto"
        return "nao_faz_jus"
    
    def calcular(self, grs_risco: str, carga_horaria_mensal: int, horas_realizadas: int) -> ResultadoCalculo:
        nivel = self._parser_nivel_grs(grs_risco)
        valor_grs = ProvedorDadosFhemig.obter_valor_grs(nivel)

        # Previne divisão por zero
        ch = carga_horaria_mensal if carga_horaria_mensal > 0 else 1
        
        valor = (valor_grs / ch) * horas_realizadas

        memoria = [
            f"GRS ({grs_risco}): {FormatadorCampos.brl(valor_grs)}",
            f"÷ CH {ch}h = {FormatadorCampos.brl(valor_grs/ch)}/h",
            f"× {horas_realizadas} horas falta",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)