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

## Korisni resursi

- [Git dokumentacija](https://git-scm.com/doc)
- [GitHub Git cheatsheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Learn Git Branching (interaktivno)](https://learngitbranching.js.org/)
