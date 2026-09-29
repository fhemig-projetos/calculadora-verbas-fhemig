Calculadora de Verbas Remuneratórias — Entrega da 2ª Versão (Login, Persistência e Novas Regras de Negócio)
Antonio Marcel Sotero Dias de Oliveira

Prezados(as),

Dando continuidade ao e-mail encaminhado em 16/09 de detalhamento do Marco Atual do projeto, informo a entrega de uma nova versão da Calculadora de Verbas Remuneratórias, disponível no mesmo link já utilizado pela equipe:

https://calculadora-verbas-fhemig.streamlit.app/

Esta versão conclui o módulo de login e persistência de dados — que, no documento de status anterior, constava como item ainda em desenvolvimento — e incorpora um conjunto de ajustes de regras de negócio identificados a partir dos testes práticos reportados pelas unidades da rede.

1. Login e persistência de dados (novo)
Cada servidor passa a ter acesso identificado à ferramenta, com criação de conta própria e recuperação de senha por e-mail, em caso de esquecimento.
Os dados preenchidos e o histórico de cálculos de cada usuário agora são preservados entre acessos — anteriormente, uma atualização de página fazia o usuário perder o que estava calculando.
2. Ajustes de regras de negócio a partir dos apontamentos da rede

A equipe de desenvolvimento recebeu e tratou um conjunto de observações práticas enviadas pelos servidores que testaram a ferramenta. Entre os principais ajustes:
Passaram a ser lançadas como verbas independentes — e não apenas como valores embutidos em outros cálculos — o Vencimento Básico proporcional a dias, o Abono de Serviço Emergencial proporcional a dias, e o Complemento do Piso da Enfermagem (por dias, por meses e como desconto), atendendo à necessidade relatada de registrar essas verbas isoladamente quando forem as únicas devidas no período.
Foram incluídos campos para lançamento do Plantão Médico Complementar (PMC) e do desconto de IPSEMG referente a filho de 21 a 39 anos.
Esta versão foi testada em ambiente de homologação, isolado do ambiente de produção, antes de sua liberação.
3. Necessidade de validação pela Administração Central

Para dar prosseguimento à finalização desta etapa inicial do projeto, destacamos a necessidade de validação, junto à equipe técnica de taxação da Administração Central, de um conjunto de regras que foram implementadas com base na interpretação da equipe de desenvolvimento a partir dos relatos das unidades — ainda sem confirmação formal quanto ao código oficial de rubrica ou à fórmula de cálculo aplicável. Entre os pontos que solicitamos atenção prioritária:
Confirmação dos códigos de rubrica oficiais das novas verbas de Piso da Enfermagem, do Plantão Médico Complementar e do desconto de IPSEMG referente a filho, assim como das verbas já implementadas anteriormente.
Revisão específica das regras de cálculo de INSS Mensal/13º atualmente implementadas: quais verbas devem de fato compor a base de incidência, se a apuração deve considerar apenas os valores lançados dentro da competência do cálculo, e como as novas verbas lançadas nesta versão devem entrar nessa base, evitando dupla contagem.
Esclarecimento sobre a verba "Perda Sexto/Oitavo" — se corresponde à verba já tratada na ferramenta como desconto por faltas em horas — e sobre a verba "IPSEMG Assistência Médica sobre o 13º", quanto à sua equivalência (ou não) com o desconto de IPSEMG já implementado.
Detalhamento do desconto de IPSEMG para dependente, apontado como necessário pelas unidades, mas ainda sem informações suficientes para implementação.
Avaliação sobre a real necessidade de desmembrar o cálculo da Ajuda de Custo em parcela fixa e parcela variável, conforme relato recebido de mais de uma unidade.
Ficamos à disposição para apresentar o detalhamento técnico completo desses pontos, caso seja útil para a validação.

Agradecemos, mais uma vez, o engajamento das unidades no envio de apontamentos práticos, essencial para o amadurecimento da ferramenta.

Atenciosamente,

Antonio Marcel Sotero Dias de Oliveira

Assessoria RH +Simples
Diretoria de Gestão de Pessoas

(31) 3915-8475

FHEMIG/DIGEPE/RHMAISSIMPLES

Prédio Gerais | 13º andar
Cidade Administrativa de Minas Gerais
