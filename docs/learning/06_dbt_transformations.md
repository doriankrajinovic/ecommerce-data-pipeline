# 📚 dbt - Data Build Tool

## Gdje smo u projektu?

```
[1. Pydantic] → [2. Faker] → [3. Parquet] → [4. BigQuery] → [5. GCS] → [6. dbt]
     ✅            ✅            ✅             ✅            ✅       👈 TU SMO
```

## Zašto ovaj korak?

**Problem:** Podaci u BigQuery-u su "sirovi":
- Nema čišćenja (duplikati, null vrijednosti)
- Nema business logike (revenue, metrics)
- Teško za analitičare razumjeti

**Rješenje:** dbt transformira sirove podatke u čiste, analizirane tablice.

## Veza s prethodnim korakom (BigQuery/GCS)

Sirovi podaci su učitani u BigQuery (`ecommerce_raw` dataset).
dbt čita te podatke i kreira nove tablice s transformacijama.

```
BigQuery: ecommerce_raw (sirovi)
              ↓
         dbt transformacije
              ↓
BigQuery: ecommerce_staging (očišćeno)
              ↓
BigQuery: ecommerce_marts (business logic)
```

## Što slijedi? (Airflow)

Airflow će orkestrirati cijeli pipeline:
1. Pokreni Python generatore
2. Upload u GCS
3. Load u BigQuery
4. Pokreni dbt transformacije

---

## Ključni koncepti

### 1. Što je dbt?

dbt = "Data Build Tool" - alat za **transformaciju podataka** u data warehouse-u.

- Pišeš SQL
- dbt ga pokreće u pravom redoslijedu
- Automatski prati dependencies

### 2. Model

**Model** = SQL file koji definira jednu tablicu/view.

```sql
-- models/staging/stg_customers.sql
SELECT 
    customer_id,
    first_name,
    last_name,
    email
FROM {{ source('raw', 'customers') }}
```

dbt pretvara ovaj SQL u tablicu `stg_customers` u BigQuery-u.

### 3. Source

**Source** = vanjska tablica koju dbt čita (naši sirovi podaci).

```yaml
# models/sources.yml
sources:
  - name: raw
    database: crypto-data-pipline-484511
    schema: ecommerce_raw
    tables:
      - name: customers
      - name: products
      - name: orders
```

### 4. Staging vs Marts

```
STAGING (stg_)           MARTS (fct_, dim_)
─────────────            ──────────────────
Čišćenje podataka        Business logika
1:1 s izvorom            Agregirano
Rename stupaca           Izračuni (revenue, metrics)
Cast tipova              Za analitičare/dashboard
```

**Primjer:**
- `stg_customers` - očišćeni customer podaci
- `dim_customers` - customer dimenzija s dodatnim info
- `fct_orders` - order fact tablica s metrikama

### 5. ref() funkcija

`ref()` = referencira drugi model. dbt automatski zna redoslijed izvršavanja.

```sql
-- fct_orders koristi stg_orders
SELECT * FROM {{ ref('stg_orders') }}
```

### 6. Jinja templating

dbt koristi Jinja ({{ }}) za dinamički SQL:

```sql
{{ source('raw', 'customers') }}  -- Referencira source
{{ ref('stg_customers') }}         -- Referencira model
{{ var('start_date') }}            -- Varijabla
```

---

## dbt projekt struktura

```
dbt/
├── dbt_project.yml      # Konfiguracija projekta
├── profiles.yml         # Credentials (NE COMMITAJ!)
├── models/
│   ├── sources.yml      # Definicija izvora
│   ├── staging/         # Staging modeli
│   │   ├── stg_customers.sql
│   │   └── stg_orders.sql
│   └── marts/           # Mart modeli
│       ├── dim_customers.sql
│       └── fct_orders.sql
└── tests/               # Data quality testovi
```

---

## dbt naredbe

```bash
dbt run          # Pokreni sve modele
dbt run --select stg_customers  # Pokreni jedan model
dbt test         # Pokreni testove
dbt build        # run + test
dbt docs generate  # Generiraj dokumentaciju
```

---

## Korisni linkovi

- [dbt dokumentacija](https://docs.getdbt.com/)
- [dbt BigQuery setup](https://docs.getdbt.com/docs/core/connect-data-platform/bigquery-setup)
