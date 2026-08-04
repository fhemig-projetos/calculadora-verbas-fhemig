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

## Centralização do parser de GRS
- Adaptar ainda em: 

### 📋 Próximas calculadoras que precisam da mesma alteração

Faltam **7 arquivos**, divididos em 3 grupos:

#### Grupo A — Têm `_parser_nivel_grs` local (remover método + trocar chamada)
| Arquivo | Ação |
|---|---|
| `grs_meses.py` | Remover `_parser_nivel_grs` + chamada direta |
| `grs_desconto_horas.py` | Remover `_parser_nivel_grs` + chamada direta |
| `ferias_indenizadas.py` | Remover `_parser_nivel_grs` + chamada direta |
| `terco_ferias.py` | Remover `_parser_nivel_grs` + chamada direta |

#### Grupo B — Parser inline (trocar por chamada direta)
| Arquivo | Ação |
|---|---|
| `grs_dias.py` | Trocar `"risco_medio" if "Médio" else "risco_alto"` por chamada direta (corrige "Não faz jus") |

#### Grupo C — Quebrados (chamam método inexistente)
| Arquivo | Ação |
|---|---|
| `faltas_dias.py` | Chamada direta + **nova fórmula** (Piso + ÷30 + `faltas_dias`) — tarefa principal |
| `faltas_horas.py` | Chamada direta (corrige `AttributeError`) |

#### Padrão de alteração em cada uma

**Antes:**
```python
nivel = self._parser_nivel_grs(grs_risco)   # ou parser inline
valor_grs = ProvedorDadosFhemig.obter_valor_grs(nivel)
```

**Depois:**
```python
valor_grs = ProvedorDadosFhemig.obter_valor_grs(grs_risco)
```

## Piso enfermagem
- Lembrar da regra do piso da enfermagem: é um valor fixo? Faz sentido trazer pré preenchido?

## Descontos de faltas e atrasos
- O atraso em horas ou dias afeta o valor do campo da GRS que é considerada na fórmula de cálculo? 