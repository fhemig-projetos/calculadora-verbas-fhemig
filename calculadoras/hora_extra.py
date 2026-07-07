from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraHoraExtra(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: (Venc. Básico + Ad. Desempenho) ÷ Carga Horária Mensal × Horas Realizadas × 1,50"

    @property
    def campos_necessarios(self):
        return ["vencimento_basico", "ad_desempenho", "carga_horaria_mensal", "horas_realizadas"]

    def calcular(self, vencimento_basico: float, ad_desempenho: float, carga_horaria_mensal: float, horas_realizadas: float) -> ResultadoCalculo:
        # Tratamento de erro básico para não quebrar o app
        if carga_horaria_mensal <= 0:
            return ResultadoCalculo(0.0, ["Erro: Carga horária deve ser maior que zero."])

        # Fórmula            
        base = vencimento_basico + ad_desempenho
        valor = (base / carga_horaria_mensal) * horas_realizadas * 1.5
        
        # Memória de cálculo
        memoria = [
            f"Base: {FormatadorCampos.brl(base)}", 
            f"Valor/hora: {FormatadorCampos.brl(base/carga_horaria_mensal)}",
            f"× {horas_realizadas:.0f} horas realizadas × 1,50", 
            f"= {FormatadorCampos.brl(valor)}"
        ]
        return ResultadoCalculo(valor=valor, memoria_calculo=memoria)

