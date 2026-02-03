# 📚 Faker - Generiranje Realističnih Podataka

## Gdje smo u projektu?

```
[1. Pydantic] → [2. FAKER] → [3. Parquet] → [4. BigQuery] → [5. dbt] → [6. Airflow]
     ✅            👈 TU SMO
```

## Zašto ovaj korak?

**Problem:** Trebamo podatke za testiranje pipeline-a, ali:
- Nemamo pristup pravim e-commerce podacima
- Ne smijemo koristiti prave korisničke podatke (GDPR)
- Ručno pisanje test podataka je sporo i nerealistično

**Rješenje:** Faker generira realistične podatke automatski.

## Veza s prethodnim korakom (Pydantic)

Pydantic definira **strukturu** podataka (koja polja, koji tipovi).
Faker **popunjava** tu strukturu realističnim vrijednostima.

```python
# Pydantic kaže: "Customer ima first_name koji je string"
# Faker kaže: "Evo ti first_name = 'Ivan'"
```

## Što slijedi? (Parquet)

Generirani podaci su trenutno samo u memoriji. Sljedeći korak ih **sprema** u Parquet format za trajno čuvanje i učitavanje u BigQuery.

---

## Što je Faker?

Python biblioteka za generiranje **realističnih lažnih podataka** - imena, emailovi, adrese, datumi, itd.

## Zašto ga koristimo?

- **Testiranje** - trebamo podatke koji izgledaju kao pravi
- **Razvoj** - ne koristimo prave korisničke podatke (GDPR!)
- **Demonstracija** - portfolio projekti s realističnim podacima

## Ključni koncepti

### 1. Seed za reproducibilnost

```python
Faker.seed(42)
random.seed(42)
```

Isti seed = isti podaci svaki put. Korisno za:
- Testove koji očekuju određene vrijednosti
- Debugging - možeš reproducirati problem

### 2. Faker metode

| Metoda | Primjer outputa |
|--------|-----------------|
| `fake.first_name()` | "Ivan", "Ana" |
| `fake.last_name()` | "Horvat", "Smith" |
| `fake.email()` | "ivan.horvat@example.com" |
| `fake.country()` | "Croatia", "Germany" |
| `fake.date_time_between("-2y", "now")` | Random datum u zadnje 2 godine |
| `fake.uuid4()` | Unique identifier |

### 3. Lokalizacija

```python
fake = Faker('hr_HR')  # Hrvatski podaci
fake = Faker(['en_US', 'de_DE'])  # Mix jezika
```

## Veza s ostatkom projekta

```
Faker (generira) → Pydantic (validira) → Parquet (sprema)
```

## Korisni linkovi

- [Faker dokumentacija](https://faker.readthedocs.io/)
- [Lista providera](https://faker.readthedocs.io/en/master/providers.html)
