from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraHoraExtra(CalculadoraVerba):
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: (Venc. Básico + Ad. Desempenho) ÷ Carga Horária × Horas Realizadas × 1,50"

    @property
    def campos_necessarios(self):
        return ["vencimento", "ad_desempenho", "carga_horaria", "horas_realizadas"]

    def calcular(self, vencimento: float, ad_desempenho: float, carga_horaria: float, horas_realizadas: float) -> ResultadoCalculo:
        # Tratamento de erro básico para não quebrar o app
        if carga_horaria <= 0:
            return ResultadoCalculo(0.0, ["Erro: Carga horária deve ser maior que zero."])

        # Fórmula            
        base = vencimento + ad_desempenho
        valor = (base / carga_horaria) * horas_realizadas * 1.5
        
        # Memória de cálculo
        memoria = [
            f"Base: {FormatadorCampos.brl(base)}", 
            f"Valor/hora: {FormatadorCampos.brl(base/carga_horaria)}",
            f"× {horas_realizadas:.0f} horas realizadas × 1,50", 
            f"= {FormatadorCampos.brl(valor)}"
        ]
        return ResultadoCalculo(valor=valor, memoria_calculo=memoria)

