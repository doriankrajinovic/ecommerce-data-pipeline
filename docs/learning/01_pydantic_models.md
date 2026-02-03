# 📚 Pydantic - Data Validation u Pythonu

## Gdje smo u projektu?

```
[1. PYDANTIC] → [2. Faker] → [3. Parquet] → [4. BigQuery] → [5. dbt] → [6. Airflow]
  👈 TU SMO
```

## Zašto ovaj korak PRVI?

**Problem:** U data pipeline-ima greške u podacima se otkrivaju kasno:
- Krivi tip podatka → dbt model pukne
- Nedostajuće polje → Dashboard prikazuje NULL
- Debugging je noćna mora jer ne znaš gdje je greška nastala

**Rješenje:** Pydantic validira podatke **na ulazu** - greške se hvataju odmah.

## Što slijedi? (Faker)

Pydantic definira strukturu (Customer ima email, price je Decimal).
Faker koristi tu strukturu za generiranje realističnih podataka.

```
Pydantic: "Customer ima polje email tipa EmailStr"
Faker: "OK, generiram email = 'ivan@example.com'"
```

---

## Što je Pydantic?

**Pydantic** je Python biblioteka za **validaciju podataka** korištenjem Python type hints.
Glavna prednost: hvata greške u podacima **odmah**, ne kasnije u pipeline-u.

## Zašto koristimo Pydantic u ovom projektu?

### Problem bez validacije

```python
# Bez validacije - greške prolaze neprimijećeno
customer = {
    "customer_id": "123",
    "email": "nije-validan-email",    # ❌ Krivi format
    "price": -50.00                    # ❌ Negativna cijena
}
# Greška se otkrije tek u dbt-u ili dashboardu = teško debugiranje
```

### Rješenje s Pydantic-om

```python
from pydantic import BaseModel, EmailStr, Field

class Customer(BaseModel):
    customer_id: str
    email: EmailStr                    # ✅ Mora biti validan email
    price: float = Field(gt=0)         # ✅ Mora biti > 0

# Pydantic ODMAH javlja grešku ako podaci nisu validni
customer = Customer(customer_id="123", email="bad", price=-50)
# ValidationError: value is not a valid email address
```

---

## Ključni koncepti koje koristimo

### 1. BaseModel

Osnovna klasa iz koje nasljeđujemo sve naše modele.

```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
```

**Što dobijamo automatski:**
- Validacija tipova (`name` mora biti string)
- `__init__` metoda (ne trebamo je pisati)
- `model_dump()` za pretvaranje u dictionary
- `model_dump_json()` za pretvaranje u JSON

---

### 2. Field - Dodatna ograničenja

`Field()` omogućuje definiranje dodatnih pravila za polje.

```python
from pydantic import Field

class Product(BaseModel):
    name: str = Field(min_length=1, max_length=200)  # Dužina stringa
    price: float = Field(gt=0)                        # Greater than 0
    stock: int = Field(ge=0)                          # Greater or equal 0
```

**Česti Field parametri:**

| Parametar | Značenje | Primjer |
|-----------|----------|---------|
| `gt` | Greater than (>) | `Field(gt=0)` → mora biti > 0 |
| `ge` | Greater or equal (>=) | `Field(ge=0)` → mora biti >= 0 |
| `lt` | Less than (<) | `Field(lt=100)` → mora biti < 100 |
| `le` | Less or equal (<=) | `Field(le=100)` → mora biti <= 100 |
| `min_length` | Min dužina stringa | `Field(min_length=1)` |
| `max_length` | Max dužina stringa | `Field(max_length=100)` |
| `pattern` | Regex pattern | `Field(pattern=r"^\d{4}$")` |

---

### 3. Enum - Ograničene vrijednosti

`Enum` koristimo kada polje može imati samo **određene vrijednosti**.

```python
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Order(BaseModel):
    status: OrderStatus  # Može biti SAMO jedna od gornjih vrijednosti
```

**Zašto `str, Enum`?**
- `str` omogućuje da se vrijednost serializa kao string ("pending"), ne kao objekt
- Bez `str`: `{"status": <OrderStatus.PENDING>}` ❌
- S `str`: `{"status": "pending"}` ✅

---

### 4. EmailStr - Validacija email formata

Pydantic ima ugrađene tipove za česte formate.

```python
from pydantic import EmailStr

class Customer(BaseModel):
    email: EmailStr  # Automatski provjerava email format
```

**Primjeri:**
- `"john@example.com"` ✅ Validan
- `"john@example"` ❌ Nevalidan (nedostaje TLD)
- `"john.example.com"` ❌ Nevalidan (nedostaje @)

---

### 5. field_validator - Custom validacija

Kada trebamo kompleksniju logiku validacije.

```python
from pydantic import field_validator

class Customer(BaseModel):
    country: str
    
    @field_validator('country')
    @classmethod
    def validate_country(cls, v: str) -> str:
        # Ukloni razmake i capitalize
        return v.strip().title()
```

**Objašnjenje dekoratora:**
- `@field_validator('country')` - validira polje 'country'
- `@classmethod` - metoda pripada klasi, ne instanci
- `cls` - referenca na klasu (umjesto `self`)
- `v` - vrijednost koja se validira

---

### 6. Decimal vs float

Za novčane vrijednosti koristimo `Decimal`, ne `float`.

```python
from decimal import Decimal

# ❌ Float ima probleme s preciznošću
>>> 0.1 + 0.2
0.30000000000000004

# ✅ Decimal je precizan
>>> Decimal('0.1') + Decimal('0.2')
Decimal('0.3')
```

**U našem modelu:**
```python
from decimal import Decimal
from pydantic import Field

class Product(BaseModel):
    price: Decimal = Field(gt=0, decimal_places=2)
```

---

### 7. Optional - Opcionalna polja

Kada polje ne mora uvijek postojati.

```python
from typing import Optional

class Customer(BaseModel):
    name: str                           # Obavezno
    phone: Optional[str] = None         # Opcionalno, default None
```

---

## Praktični primjer iz našeg projekta

```python
class Order(BaseModel):
    order_id: str = Field(..., description="Unique order identifier")
    customer_id: str
    order_date: datetime
    status: OrderStatus        # Enum - samo dozvoljene vrijednosti
    total_amount: Decimal = Field(ge=0, decimal_places=2)
```

**Raščlamba:**
- `Field(...)` - tri točke znače da je polje **obavezno**
- `description` - dokumentacija za polje (vidljiva u JSON schema)
- `OrderStatus` - Enum osigurava da status može biti samo pending/confirmed/...
- `Decimal` - preciznost za novčane iznose
- `ge=0` - total ne može biti negativan

---

## Kako testirati Pydantic modele

```python
# Uspješno kreiranje
product = Product(
    product_id="PROD-001",
    name="Laptop",
    category=ProductCategory.ELECTRONICS,
    price=Decimal("999.99"),
    stock_quantity=50,
    created_at=datetime.now()
)

# Pretvaranje u dictionary
print(product.model_dump())

# Pretvaranje u JSON
print(product.model_dump_json())
```

---

## Veze s ostatkom projekta

```
Pydantic Models (validacija) 
       ↓
Faker Generator (koristi modele za kreiranje podataka)
       ↓
Parquet Files (spremanje validiranih podataka)
       ↓
BigQuery/Snowflake (sigurni da su podaci čisti)
       ↓
dbt (transformacije na kvalitetnim podacima)
```

---

## Korisni linkovi

- [Pydantic dokumentacija](https://docs.pydantic.dev/)
- [Field Types](https://docs.pydantic.dev/latest/concepts/fields/)
- [Validators](https://docs.pydantic.dev/latest/concepts/validators/)
