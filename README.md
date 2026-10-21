# 📊 Pipeline de Ingestão e Análise de Indicadores Financeiros (Taxa SELIC)

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Git](https://img.shields.io/badge/Git-GitHub-F05032?style=for-the-badge&logo=git&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-ETL-150458?style=for-the-badge&logo=pandas&logoColor=white)

## Visão Geral do Projeto
Este projeto consiste em um pipeline automatizado de Engenharia de Dados focado na extração, tratamento e carga do histórico da **Taxa SELIC acumulada no mês**, disponibilizado via API REST pública do Banco Central do Brasil. 

Os dados brutos são ingeridos em Python, padronizados no ecossistema Pandas e persistidos em uma instância analítica do **PostgreSQL hospedada na nuvem (Supabase)**. Na camada de consumo, são disponibilizadas consultas SQL avançadas utilizando **Window Functions** e **CTEs** para análise temporal de juros.

---

## Arquitetura da Solução
```text
+-------------------------+
|   API REST              |
|   Banco Central do BR   |
+------------+------------+
             |  (Requisição HTTP GET / JSON)
             v
+-------------------------+
|   Pipeline Python (ETL) |
|   - Requests            |
|   - Pandas              |
|   - SQLAlchemy          |
+------------+------------+
             |  (Ingestão via Driver PostgreSQL)
             v
+-------------------------+
|   Database Supabase     |
|   PostgreSQL (Cloud)    |
|   - tb_taxa_selic       |
+------------+------------+
             |  (Consultas Analíticas)
             v
+-------------------------+
|   Análises SQL          |
|   - Window Functions    |
|   - CTEs & Ranking      |
+-------------------------+
```
## Tecnologias e Ferramentas
* **Linguagem:** Python 3.10+
* **Extração & Transformação (ETL):** requests, pandas, sqlalchemy, psycopg
* **Armazenamento / Data Warehouse:** PostgreSQL (Supabase Cloud)
* **Ambiente de Desenvolvimento:** GitHub Codespaces
* **Controle de Versão:** Git & GitHub

---

## Dicionário de Dados (tb_taxa_selic)

| Nome do Campo | Tipo de Dado | Descrição | Exemplo de Conteúdo |
| :--- | :--- | :--- | :--- |
| dt_posicao | DATE | Data de referência da apuração da taxa (Padrão ISO 8601). | 2023-12-01 |
| vl_taxa_selic | FLOAT | Percentual da taxa SELIC acumulada no mês. | 0.89 |
| dt_ingestao | TIMESTAMP | Carimbo de data/hora da execução do pipeline (Auditoria). | 2024-03-30 14:20:00 |

---

## Consultas Analíticas (SQL Avançado)

O projeto disponibiliza queries focadas em extrair inteligência da série temporal (arquivo queries_analiticas.sql):

1. **Média Móvel de 12 Meses (AVG OVER):** Suaviza flutuações sazonais para identificar a tendência real de médio/longo prazo da política monetária.
2. **Variação Mês a Mês (LAG):** Compara a taxa do mês atual com o mês imediatamente anterior sem custo computacional de JOINs.
3. **Picos Anuais da SELIC (CTE + DENSE_RANK):** Identifica o mês de maior taxa de juros registrada em cada ano do histórico.

---

## Como Executar o Projeto Localmente

### Pré-requisitos
* Python 3.10+ instalado.
* Instância do PostgreSQL no Supabase configurada.

### Passo a Passo

1. Clonar o repositório:
   ```git clone https://github.com/SEU_USUARIO/pipeline-ingestao-dados-financeiros.git```
   ```cd pipeline-ingestao-dados-financeiros```

2. Instalar as dependências:
   ```pip install -r requirements.txt```

3. Configurar a string de conexão:
   Edite o arquivo pipeline_selic.py inserindo a URI do seu banco no Supabase na variável DATABASE_URL.

4. Executar o pipeline:
   ```python pipeline_selic.py```

---

## ✒️ Autora
Desenvolvido por mim como projeto de consolidação prática de Engenharia de Dados.  
Conecte-se comigo no [LinkedIn](https://www.linkedin.com/in/carla-a-7a465214a)!
