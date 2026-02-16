# 📚 Git - Version Control Osnove

## Što je Git?

Git je **sustav za praćenje promjena** u kodu. Zamišljaj ga kao "Save Game" za kod - možeš se vratiti na bilo koju prethodnu verziju.

---

## Zašto Git?

**Bez Gita:**
- `projekt_v1.py`
- `projekt_v2_final.py`
- `projekt_v2_final_FINAL.py`
- `projekt_STVARNO_FINAL.py`

**S Gitom:**
- Jedna datoteka `projekt.py`
- Git pamti SVE verzije
- Možeš se vratiti na bilo koju

---

## Ključni koncepti

### 1. Repository (Repo)

Folder koji Git prati. Ima skriveni `.git` folder s poviješću.

```bash
# Inicijaliziraj novi repo
git init

# Kloniraj postojeći repo
git clone https://github.com/user/repo.git
```

### 2. Working Directory → Staging Area → Repository

```
┌─────────────────┐    git add     ┌─────────────────┐    git commit    ┌─────────────────┐
│                 │ ─────────────► │                 │ ────────────────► │                 │
│ Working Dir     │                │ Staging Area    │                   │ Repository      │
│ (tvoji fileovi) │                │ (pripremljeno)  │                   │ (spremljeno)    │
│                 │ ◄───────────── │                 │                   │                 │
└─────────────────┘   git restore  └─────────────────┘                   └─────────────────┘
```

**Working Directory** = tvoji fileovi na disku
**Staging Area** = "košarica" s promjenama koje želiš spremiti
**Repository** = trajna povijest svih spremljenih promjena

### 3. Commit

**Commit** = snimka (snapshot) koda u određenom trenutku.

```bash
# Dodaj fileove u staging
git add filename.py       # jedan file
git add .                 # sve promjene

# Spremi (commit) s porukom
git commit -m "Dodao bigquery loader"
```

Svaki commit ima:
- Unique ID (hash): `a1b2c3d4...`
- Poruku: "Dodao bigquery loader"
- Autora i datum
- Pointer na prethodni commit

### 4. Branch (grana)

Branch = paralelna verzija koda. Možeš eksperimentirati bez da pokvariš glavni kod.

```
main:     A ── B ── C ── D ── E
                    │
feature:            └── F ── G ── H
```

```bash
# Kreiraj novu granu
git checkout -b nova-grana

# Prebaci se na postojeću granu
git checkout main

# Vidi sve grane
git branch
```

### 5. Merge

Spajanje dvije grane.

```bash
# Prebaci se na main
git checkout main

# Spoji feature granu u main
git merge feature-branch
```

### 6. Remote (GitHub)

**Remote** = verzija repoa na serveru (GitHub, GitLab, Bitbucket).

```bash
# Poveži lokalni repo s GitHubom
git remote add origin https://github.com/user/repo.git

# Pošalji promjene na GitHub
git push origin main

# Povuci promjene s GitHuba
git pull origin main
```

---

## Najčešće naredbe

### Dnevni workflow:

```bash
# 1. Provjeri status (što je promijenjeno)
git status

# 2. Vidi promjene
git diff

# 3. Dodaj promjene u staging
git add .

# 4. Commitaj
git commit -m "Opis što si napravio"

# 5. Pošalji na GitHub
git push
```

### Korisne naredbe:

```bash
# Vidi povijest commitova
git log --oneline

# Vrati file na zadnju commitanu verziju
git restore filename.py

# Vidi tko je što promijenio
git blame filename.py
```

---

## Vizualni primjer

```
TI RADIŠ:
    1. Editiraš models.py
    2. git add models.py         (staviš u košaricu)
    3. git commit -m "Fix bug"   (spremiš snapshot)
    4. git push                  (pošalješ na GitHub)

KOLEGA RADI:
    1. git pull                  (povuče tvoje promjene)
    2. Vidi tvoj fix
```

---

## .gitignore

Datoteka koja govori Gitu koje fileove da IGNORIRA.

```
# Ne prati ove fileove:
credentials.json     # Tajne!
*.pyc               # Kompilirani Python
__pycache__/        # Cache folder
.env                # Environment varijable
data/               # Generirani podaci
```

---

## Česte greške i rješenja

### "Changes not staged for commit"
```bash
# Zaboravio si git add
git add .
git commit -m "poruka"
```

### "Your branch is behind"
```bash
# Netko je pushao prije tebe
git pull
git push
```

### "Merge conflict"
```bash
# Dva čovjeka editirala istu liniju
# Git ne zna koju verziju uzeti
# Moraš ručno odabrati
```

---

## Git vs GitHub

| Git | GitHub |
|-----|--------|
| Software na tvom računalu | Web servis |
| Prati promjene lokalno | Hosting za Git repoe |
| Radi offline | Treba internet |
| Besplatan | Besplatan za javne repoe |

---

## Pull Request (PR)

**Pull Request** = zahtjev da se tvoj kod spoji u glavni kod (main branch).

### Zašto PR, a ne direktno push u main?

**Bez PR-a:**
```
Ti pushaš direkt u main → Nitko ne provjeri → Bug u produkciji 💥
```

**S PR-om:**
```
Ti pushaš u svoju granu → Otvoriš PR → Kolega pregleda → Odobri → Merge u main ✅
```

### Kako to izgleda:

```
1. Kreiraš branch: feature/add-gcs-upload
2. Napraviš promjene i commitaš
3. Pushaš branch na GitHub
4. Na GitHubu klikneš "New Pull Request"
5. Kolega pregleda tvoj kod (code review)
6. Ako je OK, klikne "Merge"
7. Tvoj kod je sad u main
```

### Vizualno na GitHubu:

```
┌─────────────────────────────────────────────────────────┐
│  Pull Request: "Add GCS upload functionality"           │
├─────────────────────────────────────────────────────────┤
│  feature/gcs-upload  →  main                            │
│                                                         │
│  Files changed: 3                                       │
│  + 150 lines added                                      │
│  - 20 lines removed                                     │
│                                                         │
│  [Conversation] [Commits] [Files changed]               │
│                                                         │
│  💬 Reviewer: "Izgleda dobro, samo dodaj komentar"      │
│                                                         │
│  [Merge pull request]  [Close]                          │
└─────────────────────────────────────────────────────────┘
```

### Zašto je ovo važno za data engineere?

1. **Code Review** - netko provjeri tvoj kod prije produkcije
2. **CI/CD** - automatski testovi se pokrenu na PR-u
3. **Dokumentacija** - PR opisuje što si napravio i zašto
4. **Rollback** - ako nešto pukne, znaš točno koji PR je uzrok

### Praktični workflow:

```bash
# 1. Kreiraj novu granu
git checkout -b feature/gcs-upload

# 2. Napravi promjene, commitaj
git add .
git commit -m "Add GCS upload"

# 3. Pushaj granu na GitHub
git push -u origin feature/gcs-upload

# 4. Idi na GitHub i klikni "Create Pull Request"
```

---

## Napredni koncepti (iz prakse)

### Branch = kopija cijelog repoa

Kad napraviš novi branch, on **nije prazan**. Sadrži sve datoteke iz brancha s kojeg si krenuo:

```bash
git checkout main                          # na main si, 50 fileova
git checkout -b feature/novi-feature       # novi branch, i dalje 50 fileova!
```

Branch je zapravo "pokazivač" (pointer) na isti commit. Tek kad commitaš nešto na novom branchu, on se razlikuje od maina.

```
main:              A ── B ── C
                              │
feature/novi:                 └── (identičan C dok ne commitaš)
```

### git add . vs selektivni add

**`git add .`** dodaje SVE promjene u staging. Opasno ako imaš fileove koje ne želiš commitati (npr. `dbt/.user.yml`, testni folderi).

**Selektivni add** daje ti kontrolu:

```bash
# Dodaj samo specifične fileove
git add airflow/ dbt/ecommerce/models/staging/schema.yml

# Ili dodaj sve pa makni ono što ne želiš
git add .
git restore --staged dbt/.user.yml
```

**Pravilo:** Ako imaš dobar `.gitignore`, `git add .` je siguran. Ako nisi siguran, koristi selektivni add i provjeri s `git status`.

### Zašto git add ako git status već vidi promjene?

Git ima **tri koraka**, ne dva:

```
Disk (Working Dir)  →  git add  →  Staging Area  →  git commit  →  Repository
```

- **`git status`** = POKAZUJE što se promijenilo na disku
- **`git add`** = BIRAŠ koje promjene idu u sljedeći commit
- **`git commit`** = SPREMA odabrane promjene

Zašto? Jer ponekad ne želiš sve promjene u istom commitu. Npr. promijeniš 5 fileova, ali 3 su za jednu stvar, a 2 za drugu - napraviš dva odvojena commita.

### Git ne dodaje nepromijenjene fileove

Ako pokreneš `git add mojfile.py`, ali je `mojfile.py` identičan onom u repou, Git neće ništa stageati jer **nema razlike**. Git prati promjene (diffs), ne fileove.

```bash
git add .                # nema efekta ako je sve isto kao u repou
git status               # "nothing added to commit"
```

### Nakon merge na GitHubu - pull lokalno!

Kad mergaš PR na GitHubu, promjene su **samo na serveru**. Tvoj lokalni `main` je još star:

```
GitHub main:   A ── B ── C ── D (novi merge)
Lokalni main:  A ── B ── C       (zaostaje!)
```

Zato uvijek nakon mergea:

```bash
git checkout main
git pull origin main     # povuče D s GitHuba lokalno
```

Bez toga, sljedeći branch koji kreiraš neće imati najnovije promjene.

### Zašto docker-compose.yml ide u repo?

Infrastruktura kao kod (**Infrastructure as Code**). Ako netko klonira tvoj projekt (ili ti na novom računalu), mora moći pokrenuti sve s jednom naredbom:

```bash
docker-compose up -d     # pokreće cijeli Airflow environment
```

Bez `docker-compose.yml` u repou, nitko ne zna kako pokrenuti Airflow. Projekt mora biti **reproducibilan** - to je ključni princip u data engineeringu.

**Što ide u repo:**
- Kod (Python, SQL, dbt modeli)
- Infrastruktura (docker-compose.yml, Dockerfile)
- CI/CD (.github/workflows/)
- Dokumentacija (README, docs/)

**Što NE ide u repo:**
- Tajne (credentials.json, .env)
- Generirani podaci (data/)
- Lokalne postavke (.user.yml, venv/)

---

## Pronalaženje grešaka u velikim logovima

Kad dobiješ ogroman log (npr. iz Airflow ili dbt), ne čitaj sve - filtriraj:

### 1. Skrolaj na kraj loga
Većina alata (dbt, pytest) na kraju ima **summary**:
```
Completed with 1 error and 0 warnings:
Failure in test not_null_my_first_dbt_model_id
```

### 2. Grep za ključne riječi
```bash
neka_naredba 2>&1 | grep -i "fail\|error"
```

### 3. Tail - samo zadnjih N linija
```bash
neka_naredba 2>&1 | tail -50
```

### 4. Ctrl+F u Airflow UI-u
U web pregledniku: `Cmd+F` i traži "FAIL", "ERROR", "exception".

### 5. U produkciji
Koriste se alati poput **Datadog**, **Grafana Loki**, ili **ELK stack** koji omogućuju pretraživanje logova kroz UI.

---

## Korisni resursi

- [Git dokumentacija](https://git-scm.com/doc)
- [GitHub Git cheatsheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Learn Git Branching (interaktivno)](https://learngitbranching.js.org/)
