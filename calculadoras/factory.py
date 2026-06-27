from .hora_extra import CalculadoraHoraExtra
from .adicional_noturno import CalculadoraAdicionalNoturno
from .gratificacao_final_semana import CalculadoraGratificacaoFinalSemana

# Registro (Factory) para conectar a UI às Classes
REGISTRO_CALCULADORAS = {
    "Hora Extra": CalculadoraHoraExtra(),
    "Adicional Noturno": CalculadoraAdicionalNoturno(),
    "Gratificação de Final de Semana": CalculadoraGratificacaoFinalSemana(),
}