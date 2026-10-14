Prezados, boa tarde!

Segue resumo das últimas implementações realizadas na Calculadora de Verbas Remuneratórias para validação (link de download: [inserir link do novo CalculadoraVerbasFhemig.zip]).

Resumo das implementações
Nova base de servidores: o cálculo é feito sobre servidores com contrato encerrado, e a base anterior reunia em sua maioria contratos em aberto. A planilha de dados funcionais foi substituída por uma nova consulta, voltada a contratos encerrados.
Reimportação: ao abrir a nova versão pela primeira vez, a planilha precisa ser importada novamente (o formato interno da base mudou).
Escolha do contrato: o mesmo MASP + admissão pode ter mais de um contrato. Ao informar o MASP e a admissão, o nome é preenchido e aparece uma lista dos contratos encontrados (ex.: 13/09/2016 → 31/01/2021 · PENF4). Ao escolher, são preenchidos datas, cargo, nível, grau e carga horária, todos editáveis. Também é possível digitar a data de admissão ou usar "Outra data" para preenchimento manual. Se o contrato não tem carga horária, a tela avisa.
Contratos com datas fim diferentes: quando o mesmo contrato (mesmo início) tem datas fim diferentes, a lista mostra um contrato só, com a maior data fim. 
Implementação de verbas de IPSEMG, conforme especificações definidas pelas equipes de taxação da ADC e do HEM.
IPSEMG titular (1411/7801) e dependentes cônjuge, pais e irmãos (816/8116).
IPSEMG 13º (1549/7701).
IPSEMG filhos: menor de 21 anos (1419/9619, R$ 60,00) e de 21 a 39 anos (815/8115, R$ 90,00).
Filtro "Piso Enfermagem": novo filtro ao lado de Vantagens e Descontos, que lista só as verbas do Piso (dias, meses, 13º e desconto, em atraso e reposição).
A calculadora tem 71 verbas registradas e 36 módulos de cálculo.
Reimportação: ao abrir a nova versão pela primeira vez, a planilha precisa ser importada novamente (o formato interno da base mudou).

Pontos que precisam de validação
Bases de cálculo verbas do IPSEMG titular e 13º.
Regras de cálculo de INSS.
Foi definido em conversa com a equipe de taxação da ADC, que o INSS será calculado a parte. 
Conferência dos pares de verbas de atraso / reposição (algumas verbas atualmente não possuem par, pois não foi indicada a correspondência).
Mais especificamente, as verbas GRS 13º, Piso Enfermagem — Desconto, Devolução Custeio Ajuda de Custo. 

Fico à disposição para qualquer dúvida.

Att.,