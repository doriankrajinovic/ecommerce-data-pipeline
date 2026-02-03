# 📚 Python Osnove za Data Engineering

Ovaj dokument pokriva Python koncepte koje koristimo u projektu.

---

## 1. Varijable i tipovi podataka

```python
# String (tekst)
name = "Ivan"

# Integer (cijeli broj)
age = 25

# Float (decimalni broj)
price = 19.99

# Boolean (true/false)
is_active = True

# List (lista - može sadržavati više vrijednosti)
fruits = ["jabuka", "kruška", "banana"]

# Dictionary (rječnik - parovi ključ:vrijednost)
person = {
    "name": "Ivan",
    "age": 25,
    "city": "Zagreb"
}
```

---

## 2. Liste

Lista je kolekcija više vrijednosti.

```python
# Kreiranje liste
numbers = [1, 2, 3, 4, 5]

# Pristup elementu (indeksi kreću od 0!)
first = numbers[0]   # 1
second = numbers[1]  # 2

# Dodavanje elementa
numbers.append(6)    # [1, 2, 3, 4, 5, 6]

# Duljina liste
length = len(numbers)  # 6
```

---

## 3. Dictionary (rječnik)

Rječnik sprema podatke kao parove ključ:vrijednost.

```python
# Kreiranje
customer = {
    "id": "CUST-001",
    "name": "Ivan",
    "email": "ivan@example.com"
}

# Pristup vrijednosti po ključu
customer_name = customer["name"]  # "Ivan"

# Dodavanje novog ključa
customer["phone"] = "091-123-4567"

# Provjera da li ključ postoji
if "email" in customer:
    print("Email postoji")
```

---

## 4. For petlja

Prolazi kroz sve elemente liste.

```python
# Jednostavna petlja
fruits = ["jabuka", "kruška", "banana"]

for fruit in fruits:
    print(fruit)
# Ispisuje:
# jabuka
# kruška
# banana

# Petlja s brojačem (range)
for i in range(5):
    print(i)
# Ispisuje: 0, 1, 2, 3, 4

# Petlja kad nam ne treba varijabla
for _ in range(3):
    print("Hello")
# Ispisuje "Hello" 3 puta
```

---

## 5. Funkcije

Funkcije su blokovi koda koje možemo ponovno koristiti.

```python
# Definicija funkcije
def greet(name):
    """Ovo je docstring - opisuje što funkcija radi."""
    message = f"Hello, {name}!"
    return message

# Poziv funkcije
result = greet("Ivan")
print(result)  # "Hello, Ivan!"


# Funkcija s više parametara
def add(a, b):
    return a + b

total = add(5, 3)  # 8


# Funkcija s default vrijednošću
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Ivan")           # "Hello, Ivan!"
greet("Ivan", "Hi")     # "Hi, Ivan!"
```

---

## 6. f-string (formatiranje teksta)

Jednostavan način za umetanje varijabli u tekst.

```python
name = "Ivan"
age = 25

# Stari način (komplicirano)
message = "Name: " + name + ", Age: " + str(age)

# f-string način (jednostavno)
message = f"Name: {name}, Age: {age}"

# Možeš i računati unutar {}
price = 100
tax = 0.25
message = f"Total: {price * (1 + tax)}"  # "Total: 125.0"
```

---

## 7. Import (uvoz modula)

Koristimo kod iz drugih datoteka ili biblioteka.

```python
# Import cijele biblioteke
import pandas

# Import s kraćim imenom
import pandas as pd

# Import specifične funkcije
from datetime import datetime

# Import iz vlastite datoteke
from models import Customer, Order
```

---

## 8. Klase i objekti

Klasa je "nacrt" za kreiranje objekata.

```python
# Definicija klase
class Dog:
    def __init__(self, name, age):
        """__init__ se poziva kad kreiramo novi objekt."""
        self.name = name
        self.age = age
    
    def bark(self):
        """Metoda - funkcija unutar klase."""
        print(f"{self.name} says: Woof!")

# Kreiranje objekta (instance)
my_dog = Dog("Rex", 3)

# Pristup atributima
print(my_dog.name)  # "Rex"
print(my_dog.age)   # 3

# Poziv metode
my_dog.bark()  # "Rex says: Woof!"
```

---

## 9. if __name__ == "__main__"

Ovaj blok se izvršava samo ako direktno pokreneš datoteku.

```python
# file: helper.py

def calculate(x, y):
    return x + y

# Ovo se izvršava SAMO ako pokreneš: python helper.py
# NE izvršava se ako importaš: from helper import calculate
if __name__ == "__main__":
    result = calculate(5, 3)
    print(f"Test: {result}")
```

**Zašto?** Omogućava testiranje datoteke, a da se test kod ne pokreće kad importaš funkcije drugdje.

---

## 10. Type hints (tipovi)

Označavaju koji tip podatka očekujemo. Python ih ne forsira, ali pomažu razumijevanju.

```python
# Bez type hints
def greet(name):
    return f"Hello, {name}"

# S type hints - jasnije je što funkcija očekuje i vraća
def greet(name: str) -> str:
    return f"Hello, {name}"

# Lista stringova
def process_names(names: list[str]) -> int:
    return len(names)

# Type hints su OPCIONALNI - kod radi isto s njima i bez njih
```

---

## 11. List comprehension (naprednije)

Kraći način za kreiranje liste. Ne moraš ovo koristiti - for petlja radi isto.

```python
# For petlja (duži, jasniji način)
squares = []
for i in range(5):
    squares.append(i * i)
# [0, 1, 4, 9, 16]

# List comprehension (kraći način)
squares = [i * i for i in range(5)]
# [0, 1, 4, 9, 16]

# Oba načina daju ISTI rezultat!
# Koristi onaj koji ti je jasniji.
```

---

## 12. Lambda funkcije (naprednije)

Kratke jednokratne funkcije. Ne moraš ih koristiti - obična funkcija radi isto.

```python
# Obična funkcija
def double(x):
    return x * 2

# Lambda verzija (ista stvar, kraće)
double = lambda x: x * 2

# Obje verzije rade isto:
double(5)  # 10
```

---

## Korisni resursi za učenje Pythona

- [Python Tutorial (službeni)](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com/) - odlični tutoriali
- [W3Schools Python](https://www.w3schools.com/python/) - jednostavni primjeri
