# Documentation Pipeline CI/CD

## 1. Fichiers de Configuration

### `pyproject.toml`
Fichier de configuration principal pour les outils Python modernes.
```toml
[tool.black]
line-length = 88                # Longueur maximum des lignes
target-version = ['py311']      # Version Python ciblée
include = '\.pyi?$'            # Fichiers à inclure (regex)
extend-exclude = '''           # Fichiers à exclure
^/env/
'''
```
**Rôle**: Configure Black, le formateur de code Python, définissant les règles de formatage.

### `.flake8`
Configuration du linter Flake8.
```ini
[flake8]
max-line-length = 88           # Longueur maximum des lignes (cohérent avec Black)
extend-ignore = E203          # Erreurs à ignorer
exclude = .git,__pycache__,build,dist,venv/ # Dossiers à exclure
```
**Rôle**: Définit les règles de style et qualité du code Python.

### `.github/workflows/CI.yml`
Configuration du pipeline CI GitHub Actions.
```yaml
name: CI

on:                           # Déclencheurs
  push:
    branches: [ "**" ]        # Tous les pushs sur toutes les branches
  pull_request:
    branches: [ "main" ]      # PRs vers main

jobs:
  lint:                       # Job de linting
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3            # Récupère le code
      - name: Set up Python                  # Configure Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies           # Installe les outils
        run: |
          python -m pip install --upgrade pip
          pip install black flake8
      - name: Run Black                      # Lance Black
        run: black . --check
      - name: Run Flake8                     # Lance Flake8
        run: flake8 .
```
**Rôle**: Automatise la vérification du code à chaque push/PR.

## 2. Protection de la Branche Main

### Configuration sur GitHub
1. Aller dans `Settings > Branches`
2. Ajouter une règle de protection pour `main`
3. Activer :
   - "Require pull request reviews before merging"
   - "Require status checks to pass before merging"
   - Sélectionner le check "lint" comme requis
   - "Include administrators"

## 3. Processus de Pull Request

### Workflow
1. Créer une nouvelle branche
```bash
git checkout -b feature/nouvelle-fonctionnalite
```

2. Développer et commit
```bash
git add .
git commit -m "feat: description"
git push -u origin feature/nouvelle-fonctionnalite
```

3. Créer la PR sur GitHub
   - Base: main ← Compare: feature/nouvelle-fonctionnalite
   - Ajouter description détaillée
   - Attendre les checks automatiques

4. Process de Review
   - Les checks doivent passer (Black + Flake8)
   - Review requise approuvée
   - Corrections si nécessaire

5. Merge
   - Possible uniquement si tous les critères sont remplis
   - Utiliser "Squash and merge" pour un historique propre

### En cas d'échec des checks
```bash
# Formatter localement
black .
# Vérifier
flake8
# Push les corrections
git push
```
