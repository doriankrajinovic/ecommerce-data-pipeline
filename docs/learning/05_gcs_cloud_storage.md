# 📚 GCS (Google Cloud Storage) - Cloud File Storage

## Gdje smo u projektu?

```
[1. Pydantic] → [2. Faker] → [3. Parquet] → [4. BigQuery] → [5. GCS] → [6. dbt]
     ✅            ✅            ✅             ✅          👈 TU SMO
```

## Zašto ovaj korak?

**Problem:** Parquet datoteke su samo na tvom računalu:
- Ako ti crkne laptop = podaci izgubljeni
- Kolege ne mogu pristupiti
- Nema verzioniranja

**Rješenje:** Upload u GCS (Cloud Storage):
- Backup u cloudu
- Pristup s bilo kojeg računala
- Verzije po datumu
- BigQuery može čitati direktno iz GCS-a

## Veza s prethodnim korakom (BigQuery)

Prije smo učitavali Parquet direktno u BigQuery s lokalnog diska.
Sada imamo staging layer:

```
PRIJE:  Lokalno → BigQuery

SADA:   Lokalno → GCS → BigQuery
                   ↑
            Backup/Staging
```

## Što slijedi? (dbt)

S podacima u BigQuery-u, dbt će raditi transformacije:
- Staging modeli (čišćenje)
- Mart modeli (business logika)

---

## Ključni koncepti

### 1. Bucket

**Bucket** = kontejner za datoteke u cloudu (kao folder).

```
gs://ecommerce-raw-dorian/           ← Bucket
├── 2024-01-25/                      ← "Folder" (prefix)
│   ├── customers.parquet
│   └── orders.parquet
└── 2024-01-26/
    └── ...
```

### 2. Object (Blob)

Svaka datoteka u bucketu je **object** (ili blob).

```python
# Object path
gs://bucket-name/folder/file.parquet
```

### 3. gsutil vs Python SDK

Dva načina za rad s GCS-om:

```bash
# gsutil (command line)
gsutil cp file.parquet gs://bucket-name/

# Python SDK
from google.cloud import storage
blob.upload_from_filename("file.parquet")
```

### 4. Particioniranje po datumu

Standardni pattern - organiziraj podatke po datumu:

```
gs://bucket/raw/2024-01-25/customers.parquet
gs://bucket/raw/2024-01-26/customers.parquet
```

Prednosti:
- Lako pronaći podatke za određeni dan
- Možeš obrisati stare podatke
- BigQuery može čitati samo određene particije

---

## Python kod za GCS

```python
from google.cloud import storage

# Kreiraj klijent
client = storage.Client.from_service_account_json("credentials.json")

# Dohvati bucket
bucket = client.bucket("ecommerce-raw-dorian")

# Upload datoteke
blob = bucket.blob("raw/customers.parquet")
blob.upload_from_filename("data/raw/customers.parquet")
```

---

## Korisni linkovi

- [GCS Python dokumentacija](https://cloud.google.com/storage/docs/reference/libraries#client-libraries-install-python)
- [gsutil dokumentacija](https://cloud.google.com/storage/docs/gsutil)
