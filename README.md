# Calculadora de Verbas Remuneratórias — FHEMIG / DIGEPE

Aplicação Streamlit para cálculo e conferência de verbas remuneratórias
nos Resumos Funcionais da FHEMIG.

## Aplicação publicada

🔗 **[https://calculadora-verbas-fhemig.streamlit.app/](https://calculadora-verbas-fhemig.streamlit.app/)**

## Verbas implementadas

- Hora Extra
- Adicional Noturno
- Gratificação de Final de Semana
- GRS — Dias
- GRS — Meses
- GRS — 13º Salário
- GRS — Desconto de Horas
- 13º Salário
- GIEFS — 13º Salário
- Piso Enfermagem — 13º Salário
- INSS sobre 13º Salário
- GIEFS — Dias
- GIEFS — Meses
- GIEFS — 1/3 de Férias
- 1/3 de Férias
- Férias Indenizadas
- Perda Sexto/Oitavo (desconto)
- Faltas — Dias (desconto)
- Ajuda de Custo Fixa (3198)
- Ajuda de Custo Variável (2070)
- Devolução Custeio Ajuda de Custo
- Aumento Salarial (multi-alíquotas)
- IPSEMG: titular (1411/7801), dependentes 3,2% (816/8116), 13º (1549/7701) e filhos (1419/9619 e 815/8115)
- INSS Mensal (tabela progressiva 2024/2025/2026)
- Licença Maternidade

## Como rodar localmente

```bash
pip install -r requirements.txt
streamlit run main.py
```

## Estrutura do projeto

Ver `contexto.md` (seção 1) para a árvore completa do repositório e o detalhamento de cada pacote (`calculadoras/`, `data/`, `ui/`, `utils/`).

## Status e pendências

O andamento do projeto, decisões de regra de negócio, dúvidas em aberto e a lista viva de pendências ficam registrados em `contexto.md` (seções 4, 6 e 14), em vez de duplicados aqui.
