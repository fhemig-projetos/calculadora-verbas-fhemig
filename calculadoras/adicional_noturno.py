from .base import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraAdicionalNoturno(CalculadoraVerba):
    
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: Venc. Básico ÷ Carga Horária Mensal × Horas Realizadas × 0,20"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["vencimento_basico", "carga_horaria_mensal", "horas_realizadas"]
    
    def calcular(self, vencimento_basico: float, carga_horaria_mensal: float, horas_realizadas: float) -> ResultadoCalculo:
        if carga_horaria_mensal <= 0:
            return ResultadoCalculo(0.0, ["Erro: Carga horária deve ser maior que zero."])
            
        valor_hora = vencimento_basico / carga_horaria_mensal
        adicional_por_hora = valor_hora * 0.20
        resultado_final = adicional_por_hora * horas_realizadas
        
        memoria = [
            f"Valor/hora: {FormatadorCampos.brl(valor_hora)}", 
            f"Adicional 20%: {FormatadorCampos.brl(adicional_por_hora)}/h",
            f"× {horas_realizadas:.0f} horas realizadas", 
            f"= {FormatadorCampos.brl(resultado_final)}"
        ]
        
        return ResultadoCalculo(valor=resultado_final, memoria_calculo=memoria)