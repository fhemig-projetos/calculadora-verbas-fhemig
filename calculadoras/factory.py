from .hora_extra import CalculadoraHoraExtra
from .adicional_noturno import CalculadoraAdicionalNoturno
from .gratificacao_final_semana import CalculadoraGratificacaoFinalSemana
from .inss_mensal import CalculadoraINSS
from .grs_dias import CalculadoraGRSDias
from .decimo_terceiro import CalculadoraDecimoTerceiro
from .giefs_13 import CalculadoraGIEFS13
from .piso_enfermagem_13 import CalculadoraPisoEnfermagem13
from .inss_decimo_terceiro import CalculadoraINSSDecimoTerceiro
from .giefs_dias import CalculadoraGIEFSDias
from .giefs_meses import CalculadoraGIEFSMeses
from .giefs_ferias import CalculadoraGIEFSFerias
from .grs_meses import  CalculadoraGRSMeses
from .grs_desconto_horas import CalculadoraGRSDescontoHoras
from .terco_ferias import CalculadoraTercoFerias

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
    "INSS sobre 13º Salário": CalculadoraINSSDecimoTerceiro(),
    "GIEFS — Dias": CalculadoraGIEFSDias(),
    "GIEFS — Meses": CalculadoraGIEFSMeses(),
    "GIEFS — 1/3 de Férias": CalculadoraGIEFSFerias(),
    "GRS — Meses": CalculadoraGRSMeses(),
    "GRS — Desconto de Horas": CalculadoraGRSDescontoHoras(),
    "1/3 de Férias": CalculadoraTercoFerias(),
}
