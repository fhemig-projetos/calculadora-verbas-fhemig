# Código das verbas
- Código das verbas incorreta (código das verbas em atraso e checar se os códigos presentes estão corretos) (Arthur Vieira Gomes Alcantara)
- Confimar código das verbas via consulta no b.o (encaminhar para o HEM também, quando conseguir) 

# Horário no doc PDF
- Horário printado no PDF c/ discrepância (Lia da Silva Vicente)

# Ajuda de custo
- Ajuste do cálculo de ajuda de custo: acrescentar carga horária e percentual de faltas; separação entre parcela fixa e variável (Juliane Martins de Almeida)
- "A verba de ajuda de custo quando a gente lança no resumo funcional, tem que separar ajuda de custo fixa e ajuda de custo variável" (Leudmarlen Rubia Gusmao Figueiredo).
> Parece que será preciso desmembrar esse cálculo em dois: ajuda de custo fixo e ajuda de custo variável. 

# Verbas independentes 
- Algumas verbas precisam ser verbas independentes para registro no histórico, pois pode haver possibilidade de o técnico pagar somente elas: hoje na calculadora aparecem apenas como variável de input em outras verbas (ex. vencimento básico, abono serv. emergenc., etc)
> Sobre esse ponto preciso que você faça os ajustes, considerando se vai afetar a lógica já existente na calculadora de pré preenchimento de campos para outras verbas

# Campo Adicional de Desempenho v
- "Ao usar a calculadora não estou conseguindo colocar o Ad, desempenho" (Luana Cristina da Silva Correa): recebi essa reclamação de um usuário. Acho que podemos então desabilitar a renderização do adicional de desempenho para não confundir os usuários, tendo em vista que essa variável não entra no cálculo dos contratados, que é para quem a calculadora se destina. Entra apenas para os efetivos.
  
# Ajustes das regras de negócio das verbas (Leudmarlen Rubia Gusmao Figueiredo)

- 2400 - VENCIMENTO BASICO: basicamente preciso informar quantos dias tenho que pagar. Então VB/30*quant. dias= 
> Incluir como verba independente.
- 2435 - ABONO SERV.EMERGENC.: basicamente preciso informar quantos dias tenho que pagar. Então ABONO/30*quant. dias=
> Incluir como verba independente.
- 2961 - PLANTAO MEDICO COMPLEMENTAR - PMC
> Validar a fórmula com a área???: se não conseguir, deixar como campo livre.
- 3198 - AJ.CUST/ALIMENT.FIXA: mesmo jeito da que já esta lançada
> Validar se vai ter que separar mesmo e como fazer essa separação ???
3154 - COMPLEMENTO PISO ENFERMAGEM: preciso informar quantos dias tenho que pagar. Então valor do PISO/30*quant. dias=
> Inserir o piso como verba independente.
> Falas do usuário sobre o piso: 
```
"complemento do piso tbm nao tem (tem so piso 13º)"
"O ideal é que no cabeçalho agente consiga marcar se o PISO se aplica, e já inserir o valor pra que ele fique predefinido depois, ou se der que ele já entenda o valor do piso a partir do salario inserido no cabeçalho."
```
> Esclarecer que da forma com o que a lógica da calculadora funciona, assim que for informado o piso uma vez, vai puxar para os outros campos esse valor. Confirmar se dessa forma atende???
> Agora, outra coisa que não entendi é a vinculação do piso ao vencimento básico: tem alguma regra de cálculo? E se sim, qual é??? 
- 9154 - REPOSIÇÃO COMP.PISO ENFERMAGEM: pode deixar livre por enquanto, pra inserir só o valor (verba negativa)
- 7810 - PERDA SEXTO/OITAVO: Esse seria o Atraso, creio que você lançou ele na calculadora como falta horas
> Confirmar com a área sobre essa verba??? 

- IPSEMG FILHO 21 A 39 ANOS - NÃO SEI A VERBA, e o desconto tbm acho que não é padrão, qualquer coisa deixa livre ate agente descobrir so pra inserir algum valor, quase nao aparece.
> Adicionar como campo livre por enquanto, mas marcar como pendência o código e a fórmula. 
- 7701 - IPSEMG ASSIST. MED. 13º SALARIO: formula é a mesma 
> Essa não entendi. É a mesma verba que já está prevista de desconto do IPSEMG só que com outro código???
- desconto do ipsemg para dependente ??? 
> Foi citada em msg anterior que estava faltando, mas não foi relacionado o detalhamento.  
 

