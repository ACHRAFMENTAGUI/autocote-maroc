# 🚗 Moroccan Used Car Price Estimator (Avito.ma)

[![CI/CD Pipeline](https://github.com/username/morocco-car-price/actions/workflows/ci.yml/badge.svg)](https://github.com/username/morocco-car-price/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

Un pipeline complet de Machine Learning et MLOps pour estimer la valeur vénale d'un véhicule d'occasion au Maroc, entraîné sur plus de 29 000 annonces scrapées sur **Avito.ma**.

---

## 📌 Présentation du Projet

- **Problème ML** : Régression supervisée
- **Variable cible** : `price` (prix en Dirhams Marocains - MAD)
- **Modèle de référence** : `LightGBM Regressor` dans un `Pipeline` Scikit-Learn
- **Features prises en compte** :
  - *Numériques* : Année de fabrication, kilométrage, puissance fiscale, nombre de portes.
  - *Catégorielles* : Marque, modèle, boîte de vitesses, type de carburant, ville, première main.
- **Interface Utilisateur** : Application interactive développée avec **Streamlit**.

### Performances des modèles (sur le jeu de test)

| Modèle | $R^2$ Score | MAE (MAD) | RMSE (MAD) |
|---|---|---|---|
| **LightGBM** | **0.84** | **~14 200 MAD** | **~22 500 MAD** |
| CatBoost | 0.83 | ~14 900 MAD | ~23 200 MAD |
| XGBoost | 0.82 | ~15 800 MAD | ~24 100 MAD |

---

## 🏗️ Structure du Projet

```text
PFM/
├── .github/workflows/ci.yml      # Intégration continue GitHub Actions
├── config/config.yaml            # Hyperparamètres et configurations centralisées
├── data/
│   ├── raw/                      # Données brutes scrapées (AvitoData.csv)
│   └── processed/                # Données nettoyées (clean_data.csv)
├── models/                       # Modèles sérialisés (.pkl)
├── notebooks/                    # Notebooks ordonnés (01_scraping à 05_lightgbm)
├── src/                          # Code source modulaire
│   ├── config.py                 # Chargeur de configuration Pydantic
│   ├── data/loader.py            # Ingestion et split
│   ├── features/preprocessor.py  # Pipeline de nettoyage et scaling
│   ├── models/train.py           # Entraînement avec MLflow
│   └── models/predict.py         # Moteur d'inférence sécurisé
├── app/streamlit_app.py          # Dashboard Streamlit
├── tests/                        # Tests unitaires et d'intégration (pytest)
├── Dockerfile                    # Image de production conteneurisée
├── pyproject.toml                # Standard de packaging moderne
└── requirements.txt              # Dépendances applicatives
```

---

## 🚀 Démarrage Rapide

### 1. Cloner le dépôt et créer l'environnement

```bash
git clone https://github.com/username/morocco-car-price.git
cd morocco-car-price

# Créer un environnement virtuel
python -m venv .venv

# Activer l'environnement
# Sur Windows :
.\.venv\Scripts\Activate.ps1
# Sur Linux / macOS :
source .venv/bin/activate

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

### 2. Lancer l'application Web (Streamlit)

```bash
streamlit run app/streamlit_app.py
```
L'interface s'ouvre alors sur `http://localhost:8501`.

---

## 📊 Entraînement et Tracking (MLflow)

Pour ré-entraîner le modèle et enregistrer les métriques dans l'interface MLflow :

```bash
python -m src.models.train
mlflow ui
```
Puis ouvrez `http://localhost:5000` pour visualiser les métriques ($R^2$, MAE, RMSE) et les artefacts.

---

## 🧪 Exécution des Tests

```bash
# Lancer les tests unitaires avec rapport de couverture
pytest --cov=src tests/
```

---

## 🐳 Déploiement avec Docker

```bash
# Construire l'image Docker
docker build -t car-price-app .

# Lancer le conteneur
docker run -p 8501:8501 car-price-app
```

---

## 👥 Auteurs & Crédits
- **Achraf Mentagui** & **Rihab El Marikh**
- Licence : [MIT](LICENSE)
