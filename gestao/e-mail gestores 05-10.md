Prezados, bom dia! 

Segue resumo das últimas implementações realizadas na Calculadora de Verbas Remuneratórias para validação (link de download: ​CalculadoraVerbasFhemig.zip​).
Resumo das implementações
Aplicativo local: abre em janela própria, sem login. A base de servidores é carregada pela planilha de dados funcionais.
Ajustes a partir de reunião com equipe de taxação do HEM:
Ajuda de Custo dividida em Fixa (3198, valor diário sugerido de R$ 50,00) e Variável (2070).
Aumento Salarial acumulado.
Lista de verbas em ordem alfabética, com filtro por Vantagens e Descontos.
Códigos atualizados conforme a lista da unidade.
Cargos e Piso de Enfermagem: nova tabela de cargos preenche o vencimento básico automaticamente. Para PENF níveis II e IV (contratados), com 30 ou 40h, o valor do Piso também vem preenchido, e o campo continua editável.
Verbas de atraso e reposição: cada verba em atraso da lista da unidade agora tem seu par de reposição, com os códigos oficiais. Os nomes passaram a trazer (Atraso), (Reposição) ou Restituição. Foram criadas também as verbas de Auxílio Transporte, Custeio de Alimentação, IPSEMG 13º e as restituições de Faltas, INSS, INSS 13º e IPSEMG.
Vários meses de uma vez: nas verbas "Meses" de valor fixo (GRS, Piso, Vencimento Básico e Abono de Emergência), o usuário informa as competências de cada mês e o sistema gera um lançamento por mês. Antes era preciso repetir o lançamento.
Lista de cálculos: agora é possível selecionar e remover lançamentos específicos, e não só o último.
Pontos que precisam de validação
Nomes: os nomes novos das verbas estão claros para quem escolhe? (Lançamentos salvos antes mantêm o nome e o código antigos.)
Códigos repetidos: o 8070 aparece em "Ajuda de Custo Variável (Reposição)" e "Devolução Custeio Ajuda de Custo". O 9154 aparece nas reposições do Piso e no "Piso Enfermagem — Desconto". O 2400 aparece no Vencimento Básico e no Aumento Salarial. Está correto?
Verbas com valor digitado, sem fórmula: Auxílio Transporte (2979/7979), restituição e custeio do Aux. Transporte (948/8849), Custeio de Alimentação (3018/9018), IPSEMG 13º (1549/7701) e PMC (2961/8961). Existe fórmula a implementar?
Restituições: para Faltas (839), INSS (408), INSS 13º (548) e IPSEMG (1411) usamos a mesma fórmula do desconto. A restituição devolve exatamente esse valor?
Efeito nas bases do INSS: as reposições não abatem a base do INSS (mensal e 13º), e as restituições, por serem Vantagem, entram em "Outras Vantagens" do INSS Mensal. Isso está de acordo com a regra?
Variantes "Meses": são necessárias para Vencimento Básico, Abono de Emergência e Piso? Elas assumem o mesmo valor em todos os meses, o que pode não valer se houver reajuste ou progressão no período.
Piso de Enfermagem: confirmar a regra, o escopo (apenas PENF II e IV contratados) e os valores da tabela. O "Piso Enfermagem — Desconto" ainda é necessário?
Verbas sem par de atraso ou reposição: Hora Extra, Aumento Salarial, Licença Maternidade, Férias Indenizadas, GRS — 13º Salário, GRS — Desconto de Horas, Perda Sexto Oitavo (só reposição) e IPSEMG Filho. Está certo assim?
Devolução Custeio Ajuda de Custo: confirmar o que representa, o código oficial e sobre quais parcelas incide.
Divisão por mês: nos lançamentos de vários meses o valor é dividido igualmente. Se os meses tiverem valores diferentes, é preciso lançar separadamente. O GIEFS — Meses não usa essa função.

Fico à disposição para qualquer dúvida.

Att.,
 

