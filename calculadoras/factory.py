from .hora_extra import CalculadoraHoraExtra
from .adicional_noturno import CalculadoraAdicionalNoturno
from .gratificacao_final_semana import CalculadoraGratificacaoFinalSemana
from .inss_mensal import CalculadoraINSS
from .grs_dias import CalculadoraGRSDias
from .decimo_terceiro import CalculadoraDecimoTerceiro
from .giefs_13 import CalculadoraGIEFS13
from .piso_enfermagem_13 import CalculadoraPisoEnfermagem13

# Registro (Factory) para conectar a UI às Classes
REGISTRO_CALCULADORAS = {
    "Hora Extra": CalculadoraHoraExtra(),
    "Adicional Noturno": CalculadoraAdicionalNoturno(),
    "Gratificação de Final de Semana": CalculadoraGratificacaoFinalSemana(),
    "GRS — Dias": CalculadoraGRSDias(),
    "13º Salário": CalculadoraDecimoTerceiro(),
    "INSS Mensal (tabela progressiva)": CalculadoraINSS(),
    "GIEFS — 13º Salário": CalculadoraGIEFS13(),
    "Piso Enfermagem — 13º Salário": CalculadoraPisoEnfermagem13(),
}