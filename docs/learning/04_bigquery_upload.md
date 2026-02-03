# 📚 BigQuery - Cloud Data Warehouse

## Gdje smo u projektu?

```
[1. Pydantic] → [2. Faker] → [3. Parquet] → [4. BIGQUERY] → [5. dbt] → [6. Airflow]
     ✅            ✅            ✅           👈 TU SMO
```

## Zašto ovaj korak?

**Problem:** Parquet datoteke su na lokalnom disku. Ne možemo:
- Pokretati SQL upite na njima
- Dijeliti podatke s timom
- Skalirati na velike datasete

**Rješenje:** Upload u BigQuery - cloud data warehouse koji:
- Omogućuje SQL upite
- Skalira automatski
- Integrira se s dbt-om

## Veza s prethodnim korakom (Parquet)

Parquet format je **optimalan za BigQuery**:
- BigQuery direktno čita Parquet
- Čuva tipove podataka (ne kao CSV)
- Brži upload od CSV-a

```
Lokalno: customers.parquet → BigQuery: projekt.dataset.customers
```

## Što slijedi? (dbt)

Kad su podaci u BigQuery, dbt može:
- Transformirati podatke (staging → marts)
- Kreirati business logiku
- Testirati kvalitetu podataka

---

## Ključni koncepti

### 1. Struktura BigQuery-a

```
GCP Projekt (npr. "my-project-123")
    └── Dataset (npr. "ecommerce_raw")
            ├── Tablica: customers
            ├── Tablica: products
            ├── Tablica: orders
            └── Tablica: order_items
```

- **Projekt** - tvoj GCP račun/projekt
- **Dataset** - grupa tablica (kao schema u SQL)
- **Tablica** - podaci

### 2. Service Account

JSON datoteka s kredencijalima za pristup BigQuery-u iz koda.

```python
from google.cloud import bigquery

# Kreira klijent koristeći credentials
client = bigquery.Client.from_service_account_json("credentials.json")
```

### 3. Load Job

BigQuery koristi "job" koncept za učitavanje podataka.

```python
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.PARQUET,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
)

# WRITE_TRUNCATE = obriši stare podatke, upiši nove
# WRITE_APPEND = dodaj na postojeće
# WRITE_EMPTY = upiši samo ako je tablica prazna
```

### 4. Table ID format

```
projekt.dataset.tablica

Primjer: my-project-123.ecommerce_raw.customers
```

---

## Korisni linkovi

- [BigQuery Python Client](https://cloud.google.com/python/docs/reference/bigquery/latest)
- [Loading Parquet data](https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet)
