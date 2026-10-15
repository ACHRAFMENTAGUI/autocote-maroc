# Guide de Contribution

Merci de contribuer au projet **Estimateur de Prix de Véhicules d'Occasion (Maroc)** !

## 1. Cloner et préparer l'environnement

```bash
git clone https://github.com/<votre-compte>/morocco-car-price.git
cd morocco-car-price

python -m venv .venv
# Sur Windows :
.\.venv\Scripts\Activate.ps1
# Sur Linux / macOS :
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

## 2. Conventions de Branches et Commits

- Créez une branche dédiée :
  ```bash
  git checkout -b feature/amelioration-modele
  ```
- Respectez les **Conventional Commits** :
  - `feat:` nouvelle fonctionnalité (ex: nouveau modèle, nouvelle feature)
  - `fix:` correction de bug (ex: parsing des valeurs aberrantes)
  - `docs:` documentation (ex: README, docstrings)
  - `test:` ajout ou mise à jour de tests
  - `refactor:` refactorisation sans changement de comportement

## 3. Qualité et Tests

Avant de soumettre une Pull Request :
```bash
# Vérification du style de code
ruff check .

# Exécution des tests unitaires
pytest tests/ -v
```

