# 🛒 E-commerce Data Pipeline

Advanced data pipeline za e-commerce analitiku - demonstracija modernih data engineering praksi.

## 🎯 Cilj projekta

Produbiti znanje data engineering tehnologija kroz kompleksniji projekt:
- **Python:** Pandas, Polars, Pydantic, Great Expectations
- **PySpark:** Batch processing velikih datasetova
- **dbt:** Incremental models, snapshots, macros
- **Airflow:** Advanced orkestracija s alertingom
- **Vizualizacija:** Looker Studio + Streamlit

## 🏗️ Arhitektura

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Faker Data     │ ──► │ Python Processing│ ──► │ Cloud Storage   │
│  Generator      │     │ (Pandas/Polars)  │     │ (Parquet)       │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
┌─────────────────┐     ┌──────────────────┐              │
│  PySpark        │ ──► │ BigQuery/        │ ◄────────────┘
│  (Large Data)   │     │ Snowflake        │
└─────────────────┘     └────────┬─────────┘
                                 │
                        ┌────────▼─────────┐
                        │ dbt Transform    │
                        │ (Staging→Marts)  │
                        └────────┬─────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Looker Studio   │     │ Streamlit       │     │ Airflow         │
│ (Business BI)   │     │ (Technical)     │     │ (Orchestration) │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## 📁 Struktura projekta

```
ecommerce-data-pipeline/
├── src/                    # Python source kod
│   ├── ingestion/         # Data generation i loading
│   ├── processing/        # Pandas, Polars, PySpark
│   └── utils/             # Pomoćne funkcije
├── dbt/                    # dbt projekt
│   ├── models/
│   │   ├── staging/       # Čišćenje podataka
│   │   └── marts/         # Business logic
│   ├── tests/
│   └── macros/
├── airflow/                # Airflow DAGs
│   └── dags/
├── dashboards/             # Streamlit aplikacija
├── tests/                  # Python unit tests
├── .github/workflows/      # CI/CD
└── requirements.txt
```

## 🛠️ Tech Stack

| Layer | Tehnologija |
|-------|-------------|
| Data Generation | Faker |
| Processing | Pandas, Polars, PySpark |
| Validation | Pydantic, Great Expectations |
| Storage | BigQuery, Snowflake |
| Transformation | dbt |
| Orchestration | Apache Airflow |
| Visualization | Looker Studio, Streamlit |
| CI/CD | GitHub Actions |

## 🚀 Quick Start

```bash
# Clone repo
git clone https://github.com/doriankrajinovic/ecommerce-data-pipeline.git
cd ecommerce-data-pipeline

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 👤 Autor

**Dorian Krajinovic**
- GitHub: [@doriankrajinovic](https://github.com/doriankrajinovic)
