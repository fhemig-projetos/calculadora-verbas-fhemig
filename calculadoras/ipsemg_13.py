from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraIPSEMG13(CalculadoraVerba):
    """1549 (restituição, Vantagem) e 7701 (reposição, Desconto): mesma fórmula, só muda tipo/código."""
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: (13º Salário + GIEFS 13º + Piso Enfermagem 13º) × 3,2%"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["valor_13_salario", "giefs_13_salario", "piso_13_salario"]

    def calcular(self, valor_13_salario: float, giefs_13_salario: float, piso_13_salario: float) -> ResultadoCalculo:
        base = valor_13_salario + giefs_13_salario + piso_13_salario
        valor = base * 0.032
        memoria = [
            f"13º Salário: {FormatadorCampos.brl(valor_13_salario)}",
            f"GIEFS 13º: {FormatadorCampos.brl(giefs_13_salario)}",
            f"Piso Enfermagem 13º: {FormatadorCampos.brl(piso_13_salario)}",
            "─────────────────────",
            f"BASE de Incidência: {FormatadorCampos.brl(base)}",
            f"× 3,2% = {FormatadorCampos.brl(valor)}",
        ]
        return ResultadoCalculo(valor=round(valor, 2), memoria_calculo=memoria)
