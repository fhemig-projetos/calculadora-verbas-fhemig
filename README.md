# Calculadora de Verbas Remuneratórias — FHEMIG / DIGEPE

Aplicação Streamlit para cálculo e conferência de verbas remuneratórias 
nos Resumos Funcionais da FHEMIG.

## Verbas implementadas

- Gratificação de Final de Semana  
- Adicional Noturno  
- Hora Extra  
- 13º Salário  
- GIEFS — 13º Salário  
- INSS sobre 13º Salário  
- GIEFS — Dias  
- GIEFS — Meses (parcelas)  
- GIEFS — 1/3 de Férias  
- GRS — Dias  
- GRS — Meses  
- GRS — Desconto de Horas  
- 1/3 de Férias  
- Férias Indenizadas  
- Faltas — Horas (desconto)  
- Faltas — Dias (desconto)  
- Ajuda de Custo Mensal  
- Desconto de Custeio (4%)  
- Aumento Salarial (4,62%)  
- Desconto de IPSEMG (3,2%)  
- INSS Mensal (tabela progressiva 2024/2025/2026)  

## Como rodar localmente

```bash
pip install streamlit
streamlit run app.py
```

## Deploy no Streamlit Community Cloud

Ver instruções completas no guia de deploy.

---

### Próximos passos do Projeto

* **[ ] Refinamento da Interface (Layout Dinâmico):**
* Implementar a organização dos campos em colunas (estilo *grid*), mantendo a responsividade do layout original.
* Refinar o `Gerador de Formulários` para suportar agrupamento lógico de inputs.

* **[ ] Revisar a validação de campos**
* Mapear se a validação está fazendo sentido e se é necessário adicionar alguma nova regra.
* O MASP, por exemplo, acho que pode ser validado para forçar apenas inserção de dados numéricos.

* **[ ] Conclusão do Motor de Memória de Cálculo:**
* Padronizar a estrutura de dados da memória entre todas as classes de calculadoras.
* Implementar a exibição otimizada da memória no front-end, garantindo clareza e rastreabilidade dos cálculos.

* **[ ] Implementação do Cabeçalho e Identidade Visual:**
* Padronizar o cabeçalho com logo e informações institucionais.
* Aplicar estilos (CSS) para manter a interface alinhada com a identidade visual da instituição.

* **[ ] Funcionalidade de Exportação (PDF):**
* Integrar biblioteca de geração de documentos (ex: `ReportLab` ou `FPDF`).
* Criar o template de impressão que consolida os dados de entrada, o resultado final e a memória de cálculo.

* **[ ] Integração com Dados do Servidor:**
* Refatorar a busca de níveis/graus para injetar os dados externos diretamente na estrutura das calculadoras.

---

