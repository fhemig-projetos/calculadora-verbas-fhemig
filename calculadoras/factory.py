from .vencimento_basico_dias import CalculadoraVencimentoBasicoDias
from .abono_emergencia_dias import CalculadoraAbonoEmergenciaDias
from .vencimento_basico_meses import CalculadoraVencimentoBasicoMeses
from .abono_emergencia_meses import CalculadoraAbonoEmergenciaMeses
from .plantao_medico_complementar import CalculadoraPlantaoMedicoComplementar
from .piso_enfermagem_dias import CalculadoraPisoEnfermagemDias
from .piso_enfermagem_meses import CalculadoraPisoEnfermagemMeses
from .piso_enfermagem_desconto import CalculadoraPisoEnfermagemDesconto
from .ipsemg_filho import CalculadoraIPSEMGFilho
from .auxilio_transporte import CalculadoraAuxilioTransporte
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
from .giefs_terco_ferias import CalculadoraGIEFSTercoFerias
from .grs_meses import  CalculadoraGRSMeses
from .grs_13 import CalculadoraGRS13
from .grs_desconto_horas import CalculadoraGRSDescontoHoras
from .ferias_terco import CalculadoraTercoFerias
from .ferias_indenizadas import CalculadoraFeriasIndenizadas
from .faltas_horas import CalculadoraFaltasHoras
from .faltas_dias import CalculadoraFaltasDias
from .ajuda_custo import CalculadoraAjudaCustoFixa, CalculadoraAjudaCustoVariavel
from .ajuda_custo_desconto import CalculadoraDescontoAjudaCusto
from .aumento_salarial import CalculadoraAumentoSalarial
from .ipsemg import CalculadoraIPSEMG
from .licenca_maternidade import CalculadoraLicencaMaternidade

# Registro (Factory) para conectar a UI às Classes
REGISTRO_CALCULADORAS = {
    # 2400 (pagamento retroativo, Vantagem) e 7400 (reposição de pagamento a maior, Desconto):
    # mesma fórmula, só muda tipo/código em tabelas.json — por isso compartilham a calculadora.
    "Vencimento Básico — Dias (Atraso)": CalculadoraVencimentoBasicoDias(),
    "Vencimento Básico — Dias (Reposição)": CalculadoraVencimentoBasicoDias(),
    "Vencimento Básico — Meses (Atraso)": CalculadoraVencimentoBasicoMeses(),
    "Vencimento Básico — Meses (Reposição)": CalculadoraVencimentoBasicoMeses(),
    # 2435 (Vantagem) e 7435 (reposição, Desconto): mesma fórmula, só muda tipo/código em tabelas.json
    "Abono de Emergência — Dias (Atraso)": CalculadoraAbonoEmergenciaDias(),
    "Abono de Emergência — Dias (Reposição)": CalculadoraAbonoEmergenciaDias(),
    "Abono de Emergência — Meses (Atraso)": CalculadoraAbonoEmergenciaMeses(),
    "Abono de Emergência — Meses (Reposição)": CalculadoraAbonoEmergenciaMeses(),
    "Plantão Médico Complementar (PMC)": CalculadoraPlantaoMedicoComplementar(),
    "Piso Enfermagem — Dias": CalculadoraPisoEnfermagemDias(),
    "Piso Enfermagem — Meses": CalculadoraPisoEnfermagemMeses(),
    "Piso Enfermagem — Desconto": CalculadoraPisoEnfermagemDesconto(),
    "IPSEMG Filho 21 a 39 anos": CalculadoraIPSEMGFilho(),
    # Auxílio Transporte: campo livre (regra de cálculo ainda não definida pela unidade — ver contexto.md)
    "Auxílio Transporte (Atraso)": CalculadoraAuxilioTransporte(),
    "Auxílio Transporte (Reposição)": CalculadoraAuxilioTransporte(),
    "Hora Extra": CalculadoraHoraExtra(),
    # 2773 (Vantagem) e 7773 (reposição, Desconto): mesma fórmula, só muda tipo/código em tabelas.json
    "Adicional Noturno (Atraso)": CalculadoraAdicionalNoturno(),
    "Adicional Noturno (Reposição)": CalculadoraAdicionalNoturno(),
    # 2416 (Vantagem) e 7416 (reposição, Desconto): mesma fórmula, só muda tipo/código em tabelas.json
    "Gratificação de Final de Semana (Atraso)": CalculadoraGratificacaoFinalSemana(),
    "Gratificação de Final de Semana (Reposição)": CalculadoraGratificacaoFinalSemana(),
    # 2491 (Vantagem) e 7491 (reposição, Desconto): mesma fórmula, só muda tipo/código em tabelas.json
    "13º Salário (Atraso)": CalculadoraDecimoTerceiro(),
    "13º Salário (Reposição)": CalculadoraDecimoTerceiro(),
    "INSS Mensal (tabela progressiva)": CalculadoraINSS(),
    # 3171 (Vantagem) e 9171 (reposição, Desconto): mesma fórmula, só muda tipo/código em tabelas.json
    "GIEFS — 13º Salário (Atraso)": CalculadoraGIEFS13(),
    "GIEFS — 13º Salário (Reposição)": CalculadoraGIEFS13(),
    # 3164 (Vantagem) e 9164 (reposição, Desconto): mesma fórmula, só muda tipo/código em tabelas.json
    "Piso Enfermagem — 13º Salário (Atraso)": CalculadoraPisoEnfermagem13(),
    "Piso Enfermagem — 13º Salário (Reposição)": CalculadoraPisoEnfermagem13(),
    "INSS sobre 13º Salário": CalculadoraINSSDecimoTerceiro(),
    "GRS — 13º Salário": CalculadoraGRS13(),
    # 2417 (Vantagem) e 5812 (reposição, Desconto): mesma fórmula, só muda tipo/código em tabelas.json
    "GIEFS — Dias (Atraso)": CalculadoraGIEFSDias(),
    "GIEFS — Dias (Reposição)": CalculadoraGIEFSDias(),
    "GIEFS — Meses (Atraso)": CalculadoraGIEFSMeses(),
    "GIEFS — Meses (Reposição)": CalculadoraGIEFSMeses(),
    # 2774 (Vantagem) e 7774 (reposição, Desconto): mesma fórmula, só muda tipo/código em tabelas.json
    "GRS — Dias (Atraso)": CalculadoraGRSDias(),
    "GRS — Dias (Reposição)": CalculadoraGRSDias(),
    "GRS — Meses (Atraso)": CalculadoraGRSMeses(),
    "GRS — Meses (Reposição)": CalculadoraGRSMeses(),
    "GRS — Desconto de Horas": CalculadoraGRSDescontoHoras(),
    # 2492 (Vantagem) e 7492 (reposição, Desconto): mesma fórmula, só muda tipo/código em tabelas.json
    "1/3 de Férias (Atraso)": CalculadoraTercoFerias(),
    "1/3 de Férias (Reposição)": CalculadoraTercoFerias(),
    # 3242 (Vantagem) e 9242 (reposição, Desconto): mesma fórmula, só muda tipo/código em tabelas.json
    "GIEFS — 1/3 de Férias (Atraso)": CalculadoraGIEFSTercoFerias(),
    "GIEFS — 1/3 de Férias (Reposição)": CalculadoraGIEFSTercoFerias(),
    "Férias Indenizadas": CalculadoraFeriasIndenizadas(),
    "Perda Sexto/Oitavo": CalculadoraFaltasHoras(),
    "Faltas — Dias": CalculadoraFaltasDias(),
    # 3198/9198 (fixa) e 2070/8070 (variável): atraso (Vantagem) e reposição (Desconto) com a mesma fórmula
    "Ajuda de Custo Fixa (Atraso)": CalculadoraAjudaCustoFixa(),
    "Ajuda de Custo Fixa (Reposição)": CalculadoraAjudaCustoFixa(),
    "Ajuda de Custo Variável (Atraso)": CalculadoraAjudaCustoVariavel(),
    "Ajuda de Custo Variável (Reposição)": CalculadoraAjudaCustoVariavel(),
    "Devolução Custeio Ajuda de Custo": CalculadoraDescontoAjudaCusto(),
    "Aumento Salarial": CalculadoraAumentoSalarial(),
    "Desconto de IPSEMG (3,2%)": CalculadoraIPSEMG(),
    "Licença Maternidade": CalculadoraLicencaMaternidade(),
}
