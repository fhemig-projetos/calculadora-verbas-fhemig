- Abono Emergência é valor fixo (150r)? 
- GIEFS 13o: valor a sofrer incidência é o próprio valor da giefs? 

## Piso enfermagem - 13º
- Definir regra vinculando p/ aparecer piso somente se carreira selecionada for penf?
- O valor do piso é fixo? Faz sentido criar regra pra puxar o piso de forma automática? Ou deixar como campo aberto mesmo?
- Parece que há uma tabela que informa o piso: checar.

## INSS - 13º
- A alíquota e a dedução consideram o valor só do 13o, ou a soma do 13o e a GIEFs do 13o? (a IA diz que é a soma dos dois)

## Aumento salarial
- Como deve funcionar no caso de alíquotas combinadas? Aplicar sequencialmente 2024 e 2026? É a soma das porcentagens? Ou aplicaria a primeira e depois aplicaria a segunda? 

## Desconto sobre ajuda de custo
- Faz sentido implementar funcionalidade de busca do valor da ajuda de custo mensal calculada em passo anterior para o valor base do desconto de custeio sobre ajuda de custo? 
- Checar dúvida da Iza: "essa calculadora é do CUSTEIO ALIMENTAÇÃO?"

## Piso enfermagem
- Lembrar da regra do piso da enfermagem: é um valor fixo? Faz sentido trazer pré preenchido?

## Descontos de faltas e atrasos
- O atraso em horas ou dias afeta o valor do campo da GRS que é considerada na fórmula de cálculo? 

## Investigar diferença entre numero_meses e numero_parcelas em config.py
## Diferença entre `numero_meses` e `numero_parcelas`

Ambos são campos numéricos inteiros (1–12) que multiplicam um valor base, mas representam **conceitos de negócio diferentes** e são usados em **verbas diferentes**:

### `numero_meses` — "Nº de Meses de Direito"
Usado em **4 calculadoras**, sempre com divisão por **12** (proporcional ao ano):

| Calculadora | Fórmula |
|---|---|
| `giefs_13.py` | `Valor GIEFS ÷ 12 × meses` |
| `piso_enfermagem_13.py` | `Valor Piso ÷ 12 × meses` |
| `decimo_terceiro.py` | `Base ÷ 12 × meses` |
| `grs_meses.py` | `Valor GRS × meses` |

Representa **quantos meses** o servidor tem direito àquela verba (ex: 13º proporcional a 6 meses trabalhados).

### `numero_parcelas` — "Nº de Parcelas"
Usado em **apenas 1 calculadora**, com divisão por **6**:

| Calculadora | Fórmula |
|---|---|
| `giefs_meses.py` | `Valor Base ÷ 6 × parcelas` |

Representa **quantas parcelas** de uma verba que é paga em 6 parcelas (a GIEFS — Meses é dividida em 6, e o usuário informa quantas parcelas quer calcular).

## Resumo

| | `numero_meses` | `numero_parcelas` |
|---|---|---|
| **Label** | Nº de Meses de Direito | Nº de Parcelas |
| **Divisor** | 12 (ano) | 6 (parcelamento) |
| **Usado em** | 4 verbas (GIEFS 13º, Piso 13º, 13º, GRS Meses) | 1 verba (GIEFS — Meses) |
| **Conceito** | Meses de direito à verba | Parcelas de um pagamento |

São campos **semanticamente distintos** — não são intercambiáveis, pois cada um reflete uma regra de negócio específica da verba em que é usado.

## GIEFS - MESES
- Qual seria a fórmula de cálculo de GIEFS meses? Não localizei na planilha