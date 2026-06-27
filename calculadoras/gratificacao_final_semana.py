from calculadoras import CalculadoraVerba, ResultadoCalculo
from utils import FormatadorCampos

class CalculadoraGratificacaoFinalSemana(CalculadoraVerba):
    
    @property
    def descricao_formula(self) -> str:
        return "Fórmula: (Venc. Básico + Ad. Desempenho) ÷ Carga Horária × Horas Realizadas × 0,5"

    @property
    def campos_necessarios(self) -> list[str]:
        return ["vencimento", "ad_desempenho", "carga_horaria", "horas_realizadas"]

    def calcular(self, vencimento: float, ad_desempenho: float, carga_horaria: float, horas_realizadas: float) -> ResultadoCalculo:
        # Trava de segurança para divisão por zero
        if carga_horaria <= 0:
            return ResultadoCalculo(0.0, ["Erro: Carga horária deve ser maior que zero."])
            
        # Passo a passo da matemática
        base = vencimento + ad_desempenho
        valor_hora = base / carga_horaria
        
        # Fórmula
        resultado_final = valor_hora * horas_realizadas * 0.5
        
        # Construção do "Extrato"
        memoria = [
            f"Base (Venc + Ad. Desempenho): {FormatadorCampos.brl(base)}",
            f"Valor/hora: {FormatadorCampos.brl(valor_hora)}",
            f"× {horas_realizadas:.0f} horas realizadas × fator 0,5",
            f"= {FormatadorCampos.brl(resultado_final)}"
        ]
        
        return ResultadoCalculo(valor=resultado_final, memoria_calculo=memoria)