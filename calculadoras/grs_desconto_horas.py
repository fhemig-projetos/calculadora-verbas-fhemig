from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraGRSDescontoHoras(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: GRS ÷ Carga Horária × Horas de Falta"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_grs", "carga_horaria_mensal", "faltas_horas"]

    def calcular(self, valor_grs: float, carga_horaria_mensal: int, faltas_horas: int) -> ResultadoCalculo:
        # Previne divisão por zero
        ch = carga_horaria_mensal if carga_horaria_mensal > 0 else 1

        valor = (valor_grs / ch) * faltas_horas

        memoria = [
            f"GRS: {FormatadorCampos.brl(valor_grs)}",
            f"÷ CH {ch}h = {FormatadorCampos.brl(valor_grs/ch)}/h",
            f"× {faltas_horas} horas de falta",
            f"= {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)