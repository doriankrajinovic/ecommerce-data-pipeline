# 📚 Parquet - Columnar Storage Format

## Gdje smo u projektu?

```
[1. Pydantic] → [2. Faker] → [3. PARQUET] → [4. BigQuery] → [5. dbt] → [6. Airflow]
     ✅            ✅           👈 TU SMO
```

## Zašto ovaj korak?

**Problem:** Faker generira podatke u memoriji - kad se skripta završi, podaci nestaju.

**Rješenje:** Spremamo podatke u Parquet datoteke koje:
- Ostaju na disku trajno
- BigQuery može direktno učitati
- Čuvaju tipove podataka (ne kao CSV gdje je sve string)

## Veza s prethodnim korakom (Faker)

Faker je generirao `List[Customer]`, `List[Order]`, itd. u memoriji.
Parquet exporter pretvara te liste u DataFrame i sprema na disk.

```
RAM: [Customer objects] → DataFrame → Disk: customers.parquet
```

## Što slijedi? (BigQuery/Snowflake)

Parquet datoteke učitavamo u cloud data warehouse (BigQuery ili Snowflake) gdje će dbt raditi transformacije.

---

## Što je Parquet?

**Columnar (stupčani) format** za spremanje podataka, optimiziran za analitiku.

## Zašto Parquet umjesto CSV?

| CSV | Parquet |
|-----|---------|
| Čita sve stupce | Čita samo potrebne stupce |
| Nema kompresiju | 2-10x manja veličina |
| Sve je string | Čuva tipove (int, date, decimal) |
| Nema schema | Schema ugrađena u file |

## Kada koristiti?

✅ **Parquet:** Analitika, data warehouse, veliki dataseti
❌ **CSV:** Jednostavna razmjena podataka, Excel kompatibilnost

## Ključni koncepti

### 1. Columnar vs Row storage

```
ROW (CSV):        COLUMN (Parquet):
id,name,age       id: [1,2,3]
1,Ivan,25         name: [Ivan,Ana,Pero]
2,Ana,30          age: [25,30,28]
3,Pero,28
```

Ako trebaš samo `age` stupac:
- CSV: učitaj cijeli file
- Parquet: učitaj samo `age` blok

### 2. Kompresija

Parquet koristi kompresiju (snappy, gzip). Isti podaci = manje prostora.

### 3. Schema

Parquet "zna" da je `price` Decimal, `created_at` DateTime. Nema parsiranja stringova.

## Pandas + Parquet

```python
# Spremanje
df.to_parquet("file.parquet")

# Čitanje
df = pd.read_parquet("file.parquet")

# Čitanje samo nekih stupaca
df = pd.read_parquet("file.parquet", columns=["id", "name"])
```

## Korisni linkovi

- [Apache Parquet](https://parquet.apache.org/)
- [Pandas Parquet docs](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_parquet.html)
