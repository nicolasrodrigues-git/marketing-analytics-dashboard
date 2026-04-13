# ◈ Marketing Analytics Dashboard

> Dashboard interativo de análise de campanhas de marketing digital com insights estratégicos baseados em dados reais.

**🔗 [Acesse o Dashboard ao Vivo](https://marketing-analytics-dashboard-anvjbu5e9cfuqppdapw5zy.streamlit.app/)**

![Dashboard Preview](https://img.shields.io/badge/Streamlit-Cloud-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?style=flat&logo=postgresql&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Visualização-3F4F75?style=flat&logo=plotly&logoColor=white)

---

## 📌 Sobre o Projeto

Este projeto analisa **72.613 campanhas de marketing digital** distribuídas em **5 canais** (Display, Mobile, Search, Social e Video) ao longo de **8 meses** (Maio a Dezembro de 2022), com investimento total de **$858 mil**.

O objetivo foi transformar dados brutos exportados do PostgreSQL em um dashboard executivo capaz de responder às perguntas que mais importam para um time de marketing:

- Onde meu dinheiro rende mais?
- Aumentar o budget realmente traz mais resultado?
- Qual canal tem o melhor custo por clique?
- Quando é o melhor momento para anunciar?

---

## 🛠 Stack Tecnológica

| Ferramenta | Uso |
|---|---|
| **PostgreSQL** | Armazenamento e extração dos dados via SQL |
| **Python 3.11** | Processamento e cálculo de métricas |
| **Pandas** | Manipulação e limpeza do DataFrame |
| **Plotly** | Visualizações interativas |
| **Streamlit** | Interface web e deploy em nuvem |
| **GitHub** | Versionamento do código |

---

## 📊 Métricas Implementadas

### Primeira Dobra — Visão Executiva (C-Level)

| Métrica | Descrição | Fórmula |
|---|---|---|
| **Investimento Total** | Soma do custo real de mídia de todas as campanhas | `SUM(media_cost_usd)` |
| **ROAS Global** | Retorno sobre o investimento em anúncios | `Receita Estimada / Investimento Total` |
| **Receita Estimada** | Projeção de receita com base em CVR e ticket médio simulados | `Conversões × Ticket Médio` |
| **CPA Médio** | Custo médio para gerar uma conversão | `Investimento / Conversões` |
| **Correlação de Pearson** | Força da relação entre orçamento aprovado e cliques gerados | `CORR(approved_budget, clicks)` |
| **Conversões Estimadas** | Total de conversões baseado na taxa de conversão simulada | `Cliques × CVR` |
| **Alcance Total** | Total de impressões geradas pelas campanhas | `SUM(impressions)` |
| **CTR Médio Global** | Taxa média de cliques sobre impressões | `(Cliques / Impressões) × 100` |
| **Funil de Conversão** | Visualização das etapas Impressões → Cliques → Conversões → Receita | Percentual acumulado por estágio |

### Segunda Dobra — Análise Operacional

| Análise | Descrição |
|---|---|
| **CPC Mensal** | Evolução do Custo por Clique ao longo dos 8 meses, com anotação automática do pico e mínimo histórico |
| **CTR × CPC por Canal** | Comparativo de eficiência de engajamento e custo entre os 5 canais simultaneamente |
| **Pareto de Campanhas** | Curva acumulada de cliques por ranking de campanha — comprova a regra 80/20 |
| **Weekday vs Weekend** | Comparativo de gasto total e média de cliques entre dias úteis e finais de semana |
| **CPC Setembro por Canal** | Destaque do mês de maior eficiência histórica, quebrado por canal |
| **Fadiga de Criativo** | Análise do CTR e CPC médio segmentado pelo tempo de exposição do anúncio (0–7d, 8–15d, +15d) |

---

## 🔍 Principais Insights Encontrados

### 1. Princípio de Pareto Confirmado (81,7%)
> Apenas **10% das campanhas** são responsáveis por **81,7% de todos os cliques**. O foco estratégico não deve ser em aumentar o volume de anúncios, mas em identificar e replicar os padrões das campanhas vencedoras.

### 2. Correlação Orçamento × Cliques: 0,11
> A análise de correlação de Pearson revelou índice de **0,1115** — praticamente inexistente. **Aumentar o budget não garante mais cliques.** O que determina o sucesso é a qualidade do criativo e da segmentação, não o valor investido.

### 3. Janela de Oportunidade Mobile (Setembro)
> Em setembro/2022, o canal Mobile atingiu **$0,13 por clique** — o menor CPC histórico de toda a análise, **15% mais barato que o Display** no mesmo período. Uma janela sazonal que não estava sendo explorada.

### 4. Weekend Subutilizado
> A empresa gasta **5,7× mais em dias úteis** ($731k) do que nos finais de semana ($127k), porém a **média de cliques é praticamente igual** (52,85 vs 51,74). O final de semana apresenta eficiência financeira superior.

### 5. Fadiga de Criativo — Ciclo de Vida Ideal: 15 dias
> Anúncios no período de **8 a 15 dias** apresentam o melhor CTR (2,06%) e CPC equilibrado ($0,43). Após 15 dias, o CTR cai 23% — sinal claro de fadiga do público com o mesmo criativo.

---

## ⚙️ Como Usar

### Pré-requisitos
```bash
pip install streamlit pandas plotly numpy
```

### Rodando Localmente
```bash
streamlit run app.py
```

### Exportando o CSV do PostgreSQL
```sql
\COPY marketing_campaign TO 'marketing_raw.csv' CSV HEADER DELIMITER ','
```

### Estrutura do Dataset
O dashboard aceita qualquer CSV com as seguintes colunas:

| Coluna | Tipo | Descrição |
|---|---|---|
| `media_cost_usd` | NUMERIC | Custo real da campanha |
| `clicks` | INTEGER | Total de cliques |
| `impressions` | INTEGER | Total de impressões |
| `approved_budget` | NUMERIC | Orçamento aprovado |
| `channel_name` | TEXT | Nome do canal (Display, Mobile, etc.) |
| `time` | TIMESTAMP | Data/hora da campanha |
| `weekday_cat` | TEXT | Categoria do dia da semana |
| `no_of_days` | INTEGER | Duração da campanha em dias |
| `campaign_item_id` | INTEGER | ID único da campanha |

---

## 📁 Estrutura do Projeto

```
marketing-analytics-dashboard/
│
├── app.py              # Aplicação principal Streamlit
├── requirements.txt    # Dependências do projeto
└── README.md           # Documentação
```

---

## 👤 Autor

**Nicolas Rodrigues**
Estudante de Análise e Desenvolvimento de Sistemas | Transição para Data Analytics

[![LinkedIn] www.linkedin.com/in/nicolas-rodrigues-dev
[![GitHub] https://github.com/nicolasrodrigues-git

---
---

# ◈ Marketing Analytics Dashboard

> Interactive dashboard for digital marketing campaign analysis with strategic insights based on real data.

**🔗 [Access the Live Dashboard](https://marketing-analytics-dashboard-anvjbu5e9cfuqppdapw5zy.streamlit.app/)**

---

## 📌 About the Project

This project analyzes **72,613 digital marketing campaigns** across **5 channels** (Display, Mobile, Search, Social, and Video) over **8 months** (May to December 2022), with a total investment of **$858k**.

The goal was to transform raw data exported from PostgreSQL into an executive dashboard capable of answering the questions that matter most to a marketing team:

- Where does my money go further?
- Does increasing the budget actually bring more results?
- Which channel has the best cost per click?
- When is the best time to advertise?

---

## 🛠 Tech Stack

| Tool | Usage |
|---|---|
| **PostgreSQL** | Data storage and extraction via SQL |
| **Python 3.11** | Processing and metric calculation |
| **Pandas** | DataFrame manipulation and cleaning |
| **Plotly** | Interactive visualizations |
| **Streamlit** | Web interface and cloud deployment |
| **GitHub** | Code versioning |

---

## 📊 Implemented Metrics

### First Fold — Executive View (C-Level)

| Metric | Description | Formula |
|---|---|---|
| **Total Investment** | Sum of actual media cost across all campaigns | `SUM(media_cost_usd)` |
| **Global ROAS** | Return on advertising spend | `Estimated Revenue / Total Investment` |
| **Estimated Revenue** | Revenue projection based on simulated CVR and average ticket | `Conversions × Average Ticket` |
| **Average CPA** | Average cost to generate one conversion | `Investment / Conversions` |
| **Pearson Correlation** | Strength of relationship between approved budget and clicks generated | `CORR(approved_budget, clicks)` |
| **Estimated Conversions** | Total conversions based on simulated conversion rate | `Clicks × CVR` |
| **Total Reach** | Total impressions generated by campaigns | `SUM(impressions)` |
| **Global Average CTR** | Average click-through rate over impressions | `(Clicks / Impressions) × 100` |
| **Conversion Funnel** | Visualization of stages: Impressions → Clicks → Conversions → Revenue | Cumulative percentage per stage |

### Second Fold — Operational Analysis

| Analysis | Description |
|---|---|
| **Monthly CPC** | Cost Per Click evolution over 8 months, with automatic annotation of peak and historical minimum |
| **CTR × CPC by Channel** | Efficiency comparison of engagement and cost across all 5 channels simultaneously |
| **Campaign Pareto** | Cumulative click curve by campaign ranking — confirms the 80/20 rule |
| **Weekday vs Weekend** | Comparison of total spend and average clicks between weekdays and weekends |
| **September CPC by Channel** | Highlight of the most efficient month in history, broken down by channel |
| **Creative Fatigue** | Analysis of average CTR and CPC segmented by ad exposure time (0–7d, 8–15d, +15d) |

---

## 🔍 Key Insights Found

### 1. Pareto Principle Confirmed (81.7%)
> Only **10% of campaigns** are responsible for **81.7% of all clicks**. The strategic focus should not be on increasing ad volume, but on identifying and replicating the patterns of winning campaigns.

### 2. Budget × Clicks Correlation: 0.11
> The Pearson correlation analysis revealed an index of **0.1115** — practically nonexistent. **Increasing the budget does not guarantee more clicks.** What determines success is the quality of the creative and targeting, not the amount invested.

### 3. Mobile Opportunity Window (September)
> In September 2022, the Mobile channel reached **$0.13 per click** — the lowest historical CPC in the entire analysis, **15% cheaper than Display** in the same period. A seasonal window that was not being explored.

### 4. Underutilized Weekend
> The company spends **5.7× more on weekdays** ($731k) than on weekends ($127k), yet the **average clicks are practically the same** (52.85 vs 51.74). The weekend shows superior financial efficiency.

### 5. Creative Fatigue — Ideal Lifecycle: 15 days
> Ads in the **8 to 15 day** period show the best CTR (2.06%) and balanced CPC ($0.43). After 15 days, CTR drops 23% — a clear signal of audience fatigue with the same creative.

---

## ⚙️ How to Use

### Prerequisites
```bash
pip install streamlit pandas plotly numpy
```

### Running Locally
```bash
streamlit run app.py
```

### Exporting CSV from PostgreSQL
```sql
\COPY marketing_campaign TO 'marketing_raw.csv' CSV HEADER DELIMITER ','
```

### Dataset Structure
The dashboard accepts any CSV with the following columns:

| Column | Type | Description |
|---|---|---|
| `media_cost_usd` | NUMERIC | Actual campaign cost |
| `clicks` | INTEGER | Total clicks |
| `impressions` | INTEGER | Total impressions |
| `approved_budget` | NUMERIC | Approved budget |
| `channel_name` | TEXT | Channel name (Display, Mobile, etc.) |
| `time` | TIMESTAMP | Campaign date/time |
| `weekday_cat` | TEXT | Day of week category |
| `no_of_days` | INTEGER | Campaign duration in days |
| `campaign_item_id` | INTEGER | Unique campaign ID |

---

## 📁 Project Structure

```
marketing-analytics-dashboard/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Project dependencies
└── README.md           # Documentation
```

---

## 👤 Author

**Nicolas Rodrigues**
Systems Analysis and Development Student | Transitioning to Data Analytics

[![LinkedIn] www.linkedin.com/in/nicolas-rodrigues-dev
[![GitHub] https://github.com/nicolasrodrigues-git
