# 🚗 AutoCote Maroc — Argus Automobile & Intelligence Artificielle

[![CI/CD Pipeline](https://github.com/username/autocote-maroc/actions/workflows/ci.yml/badge.svg)](https://github.com/username/autocote-maroc/actions)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Framework Streamlit](https://img.shields.io/badge/frontend-Streamlit%201.40+-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Model: LightGBM](https://img.shields.io/badge/ML%20Engine-LightGBM%204.0+-02569B.svg)](https://lightgbm.readthedocs.io/)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Docker Ready](https://img.shields.io/badge/docker-ready-2496ED.svg?logo=docker&logoColor=white)](Dockerfile)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **AutoCote Maroc** est une plateforme open-source d'estimation prédictive de la valeur vénale des véhicules d'occasion au Maroc. Alimentée par un modèle de gradient boosting (**LightGBM**) calibré sur un corpus représentatif de **plus de 29 000 transactions réelles**, la solution offre une cotation instantanée, une fourchette de négociation argumentée et un comparateur multi-véhicules dans une interface responsive orientée Fintech.

---

## 📑 Table des Matières

1. [À Propos du Projet](#-a-propos-du-projet)
2. [Fonctionnalités Clés](#-fonctionnalites-cles)
3. [Architecture du Repository](#-architecture-du-repository)
4. [Stack Technique](#-stack-technique)
5. [Installation & Démarrage](#-installation--demarrage)
   - [Environnement Virtuel Local](#1-environnement-virtuel-local)
   - [Déploiement Conteneurisé avec Docker](#2-deploiement-conteneurise-avec-docker)
6. [Guide d'Utilisation](#-guide-dutilisation)
   - [Application Web Interactive](#1-interface-utilisateur-web-streamlit)
   - [Utilisation en API Python (Inférence Programmatique)](#2-utilisation-en-api-python)
   - [Pipeline d'Entraînement & Tracking MLflow](#3-pipeline-dentrainement-mlflow)
7. [Performances du Modèle & Benchmarks](#-performances-du-modele--benchmarks)
8. [Validation & Tests Automatisés](#-validation--tests-automatises)
9. [Déploiement en Production](#-deploiement-en-production)
10. [Feuille de Route (Roadmap)](#-feuille-de-route-roadmap)
11. [Guide de Contribution](#-guide-de-contribution)
12. [Licence & Mentions Légales](#-licence--mentions-legales)
13. [Auteurs & Contact](#-auteurs--contact)

---

## 💡 À Propos du Projet

Sur le marché automobile marocain de la seconde main, l'absence de cote officielle standardisée complique la fixation d'un prix équitable entre particuliers et concessionnaires. Les prix affichés souffrent souvent d'asymétries d'information et de fortes variations selon les régions géographiques.

**AutoCote Maroc** répond à cette problématique par une approche rigoureuse d'ingénierie des données et de Machine Learning :
- **Approche statistique empirique** : Apprentissage supervisé sur les transactions du parc automobile national.
- **Rétro-ingénierie des facteurs de dépréciation** : Prise en compte conjointe de la marque, du modèle, de l'âge calendaire, de l'intensité kilométrique annuelle et de la puissance fiscale.
- **Transparence algorithmique** : Rendu clair des métriques de confiance ($R^2$, intervalles de fluctuation) pour éclairer les décisions d'achat et de vente.

---

## ✨ Fonctionnalités Clés

### 1. Menus Déroulants en Cascade & Catalogue Dynamique
- Sélection de la marque parmi un catalogue des constructeurs les plus diffusés au Maroc (*Dacia, Renault, Volkswagen, Peugeot, Hyundai, Mercedes-Benz...*).
- **Mise à jour dynamique des modèles** : Le choix d'une marque restreint automatiquement la liste aux seuls modèles existants, éliminant les erreurs de saisie utilisateur.
- Prise en charge des marques et modèles spécifiques via une option d'échappement adaptable.

### 2. Raccourcis Profils Types (1-Clic)
- Accès instantané à 4 profils de véhicules emblématiques du marché marocain pour un audit rapide :
  - 🚙 *Dacia Logan (2018)*
  - 🏎️ *Volkswagen Golf 7 (2019)*
  - 🚗 *Renault Clio 4 (2017)*
  - 🚘 *Peugeot 208 (2020)*

### 3. Fiche Synthétique & Indicateur d'Intensité Kilométrique
- Badges visuels récapitulatifs mis à jour en direct lors de la configuration.
- Calcul automatique de l'âge effectif et du **kilométrage annuel moyen** ($\text{km/an}$), assorti d'un diagnostic d'usure :
  - 🟢 *Faible roulage* ($< 12\,000\text{ km/an}$) : Atout valorisant à la revente.
  - 🔵 *Roulage standard marocain* ($12\,000\text{ -- }20\,000\text{ km/an}$).
  - 🟠 *Roulage intensif* ($> 20\,000\text{ km/an}$) : Décote mécanique accélérée.

### 4. Carte de Cotation Marché & Fourchette de Négociation
- Estimation de la valeur vénale médiane en **MAD** (Dirhams Marocains) et conversion indicative en **Euros (€)**.
- Délimitation d'un corridor de négociation réaliste à $\pm 7\%$ (**fourchette basse pour achat rapide** vs **fourchette haute pour valorisation optimale**).
- Popover explicatif vulgarisant la portée statistique de l'indice de confiance et du coefficient $R^2$.

### 5. Export Rapide du Rapport
- Génération d'un résumé textuel normé prêt à être copié en un clic pour partage sur messagerie ou insertion dans une annonce.

### 6. Mode Comparateur (2 Véhicules Côte à Côte)
- Deuxième onglet dédié à la comparaison simultanée de 2 configurations de véhicules.
- Calcul du différentiel de prix (en valeur absolue et en pourcentage), identification de l'option la plus économique et tableau comparatif des caractéristiques.

---

## 🏛️ Architecture du Repository

Le projet adopte les standards d'organisation **Cookiecutter Data Science** pour garantir la reproductibilité et la modularité :

```text
PFM/
├── .github/
│   └── workflows/
│       └── ci.yml               # Pipeline d'intégration continue (Lint + Tests)
├── .streamlit/
│   └── config.toml              # Thème graphique Fintech (sans flash blanc)
├── app/
│   ├── streamlit_app.py         # Application web interactive (Frontend)
│   └── assets/                  # Ressources statiques et visuelles
├── config/
│   ├── config.yaml              # Hyperparamètres et configuration du pipeline ML
│   └── vehicle_catalog.json     # Dictionnaire structuré des marques et modèles
├── data/
│   ├── raw/                     # Données brutes anonymisées (market_data_raw.csv)
│   └── processed/               # Dataset nettoyé (clean_data.csv - 29 342 lignes)
├── models/
│   └── lightgbm_model.pkl       # Artefact du modèle de production sérialisé
├── notebooks/                   # Workflow expérimental documenté
│   ├── 01_scraping.ipynb        # Collecte et ingestion
│   ├── 02_cleaning.ipynb        # Nettoyage, imputations et analyse exploratoire
│   ├── 03_catboost.ipynb        # Expérimentation CatBoost
│   ├── 04_xgboost.ipynb         # Expérimentation XGBoost
│   └── 05_lightgbm.ipynb        # Modèle de référence retenu
├── scripts/
│   └── sanitize_trademarks.py   # Script de conformité légale et anonymisation
├── src/                         # Package Python modulaire
│   ├── __init__.py
│   ├── config.py                # Validation de schéma via Pydantic
│   ├── data/
│   │   ├── __init__.py
│   │   └── loader.py            # Ingestion et partitionnement train/val/test
│   ├── features/
│   │   ├── __init__.py
│   │   └── preprocessor.py      # ColumnTransformer (StandardScaler, OneHotEncoder)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── predict.py           # Moteur d'inférence sécurisé
│   │   └── train.py             # Script de ré-entraînement avec tracking MLflow
│   └── utils/
│       ├── __init__.py
│       └── logger.py            # Gestionnaire de logs structurés
├── tests/                       # Suite de tests automatisés (pytest)
│   ├── __init__.py
│   ├── test_app.py              # Tests fonctionnels UI (Streamlit AppTest)
│   ├── test_model.py            # Tests de non-régression et robustesse du modèle
│   └── test_preprocessor.py     # Tests unitaires de transformation de features
├── .env.example                 # Modèle de configuration des variables d'environnement
├── .gitignore                   # Exclusion des caches, données lourdes et modèles
├── CONTRIBUTING.md              # Protocole de contribution et conventions de commits
├── Dockerfile                   # Image de conteneur optimisée pour la production
├── LICENSE                      # Licence open-source MIT
├── Makefile                     # Commandes d'automatisation (install, test, run)
├── pyproject.toml               # Configuration moderne du packaging Python (PEP 621)
└── requirements.txt             # Dépendances applicatives épinglées
```

---

## 🛠️ Stack Technique

- **Langage** : Python 3.10+ / 3.11
- **Machine Learning & Data Processing** : LightGBM, Scikit-learn, Pandas, NumPy, Joblib
- **Validation & Schémas** : Pydantic v2, PyYAML
- **Interface Utilisateur** : Streamlit (Mode multi-onglets, design responsive)
- **MLOps & Expérimentation** : MLflow, Git, Git LFS
- **Tests & Assurance Qualité** : Pytest, Streamlit AppTest, Ruff (Linter & Formatter)
- **Conteneurisation** : Docker, Docker Compose

---

## 💻 Installation & Démarrage

### 1. Environnement Virtuel Local

```bash
# 1. Cloner le dépôt
git clone https://github.com/username/autocote-maroc.git
cd autocote-maroc

# 2. Créer l'environnement virtuel isolé
python -m venv .venv

# 3. Activer l'environnement
# Sur Windows (PowerShell) :
.\.venv\Scripts\Activate.ps1
# Sur Linux / macOS :
source .venv/bin/activate

# 4. Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

### 2. Déploiement Conteneurisé avec Docker

L'application est entièrement conteneurisée pour garantir l'indépendance vis-à-vis de l'environnement hôte :

```bash
# Construire l'image Docker
docker build -t autocote-maroc:latest .

# Démarrer le conteneur sur le port 8501
docker run -d -p 8501:8501 --name autocote-app autocote-maroc:latest

# Accéder à l'application
open http://localhost:8501
```

---

## 📖 Guide d'Utilisation

### 1. Interface Utilisateur Web (Streamlit)

Pour lancer le dashboard interactif :

```bash
streamlit run app/streamlit_app.py
```
Accédez ensuite à `http://localhost:8501` dans votre navigateur.

### 2. Utilisation en API Python

Le moteur de prédiction [`CarPricePredictor`](file:///e:/GitHub/PFM/src/models/predict.py) peut être directement importé dans n'importe quel script tiers ou service backend (FastAPI, Flask, Celery) :

```python
from src.models.predict import CarPricePredictor

# Initialisation du moteur d'inférence (charge le pipeline LightGBM)
predictor = CarPricePredictor()

# Payload du véhicule à expertiser
donnees_vehicule = {
    "year": 2018,
    "marke": "Dacia",
    "model": "Logan",
    "type_boit": "Manuelle",
    "type_carburant": "Diesel",
    "puissance": 6,
    "kilometrage": 110000,
    "premiere_main": "Oui",
    "Nombre_doors": 5,
    "city": "Casablanca"
}

# Calcul de l'estimation vénale
prix_estime_mad = predictor.predict(donnees_vehicule)
print(f"Cote estimée : {prix_estime_mad:,.0f} MAD")
# Output: Cote estimée : 121,220 MAD
```

### 3. Pipeline d'Entraînement & Tracking MLflow

Pour ré-entraîner le modèle sur de nouvelles données et journaliser les métriques dans **MLflow** :

```bash
# Lancer l'entraînement
python -m src.models.train

# Visualiser les courbes et les runs dans l'interface MLflow
mlflow ui --port 5000
```
Accédez au tableau de bord des expériences sur `http://localhost:5000`.

---

## 📊 Performances du Modèle & Benchmarks

Les modèles ont été évalués selon un protocole strict de validation croisée et test hold-out ($80\%$ train, $20\%$ test) :

| Modèle | $R^2$ Score (Test) | MAE (Erreur Moyenne) | RMSE | Statut |
| :--- | :---: | :---: | :---: | :---: |
| **LightGBM Regressor** | **0.84** | **~14 200 MAD** | **~22 500 MAD** | **Production (Déployé)** |
| CatBoost Regressor | 0.83 | ~14 900 MAD | ~23 200 MAD | Benchmark |
| XGBoost Regressor | 0.82 | ~15 800 MAD | ~24 100 MAD | Benchmark |

### Variables Explicatives Majeures (Feature Importance)
1. **Année de fabrication** (Poids prédominant sur la décote globale)
2. **Kilométrage total** (Usure mécanique effective)
3. **Marque & Modèle** (Liquidité et prestige constructeur sur le marché local)
4. **Puissance fiscale (CV)** (Impact direct sur la vignette et la motorisation)
5. **Type de boîte de vitesses** (Surcote constatée pour les boîtes automatiques récentes)

---

## 🧪 Validation & Tests Automatisés

Le dépôt inclut une suite de tests unitaires et fonctionnels couvrant l'intégrité des transformations de données, le moteur d'inférence et le bon rendu de l'interface Streamlit :

```bash
# Exécution de l'intégralité de la suite de tests
pytest tests/ -v
```

### Détail de la couverture des tests :
- `tests/test_preprocessor.py` : Validation du parsing des formats de kilométrage, des puissances fiscales et du standard de casse.
- `tests/test_model.py` : Validation du chargement du modèle, bornage des prix ($> 10\,000\text{ MAD}$) et résistance aux catégories inconnues (`handle_unknown='ignore'`).
- `tests/test_app.py` : Tests fonctionnels d'interface via `streamlit.testing.v1.AppTest` (vérification du démarrage sans exception, interaction avec les boutons presets et déclenchement du calcul).

---

## 🚀 Déploiement en Production

| Plateforme | Méthode recommandée | Configuration requise |
| :--- | :--- | :--- |
| **Streamlit Community Cloud** | Connexion directe au dépôt GitHub | Spécifier `app/streamlit_app.py` comme point d'entrée. |
| **Hugging Face Spaces** | Space de type **Streamlit** ou **Docker** | Fichiers `Dockerfile` et `requirements.txt` inclus. |
| **Serveur Cloud Privé (VPS/AWS/GCP)** | Conteneur Docker managé | `docker-compose up -d` ou orchestration Kubernetes. |

---

## 🗺️ Feuille de Route (Roadmap)

- [x] Structuration modulaire et packaging `src/`.
- [x] Pipeline de feature engineering reproductible Scikit-learn.
- [x] Interface Streamlit avec menus déroulants dynamiques et mode comparateur.
- [x] Suite de tests automatisés (Backend & AppTest Streamlit).
- [ ] **API REST FastAPI** : Exposition d'un microservice de prédiction avec documentation OpenAPI/Swagger.
- [ ] **Explicabilité Locale (SHAP Values)** : Visualisation interactive des facteurs ayant influencé le prix d'un véhicule donné (forme de cascade d'impact).
- [ ] **Surveillance de Dérive de Données (Evidently AI)** : Alertes de data drift sur les variations de prix du marché.
- [ ] **Export PDF officiel** : Génération d'une fiche d'expertise téléchargeable aux formats PDF.

---

## 🤝 Guide de Contribution

Les contributions sont les bienvenues ! Pour proposer une amélioration :

1. Forkez le dépôt.
2. Créez votre branche thématique :
   ```bash
   git checkout -b feature/amelioration-preprocesseur
   ```
3. Respectez les conventions **Conventional Commits** (`feat:`, `fix:`, `docs:`, `test:`).
4. Assurez-vous que le linter et les tests passent au vert :
   ```bash
   ruff check .
   pytest tests/
   ```
5. Ouvrez une Pull Request détaillée. Consultez [`CONTRIBUTING.md`](CONTRIBUTING.md) pour les détails.

---

## ⚖️ Licence & Mentions Légales

### Licence
Ce projet est distribué sous licence open-source **MIT**. Vous êtes libre de l'utiliser, l'étudier, le modifier et le redistribuer. Consultez le fichier [`LICENSE`](LICENSE) pour plus d'informations.

### Clause de Non-Affiliation & Données Publiques
> **AutoCote Maroc** est une initiative logicielle et académique indépendante développée à des fins d'analyse statistique et de démonstration technique. Ce projet n'est **affilié, sponsorisé, associé, ni approuvé par aucune plateforme commerciale tierce d'annonces classées**. Les estimations fournies sont générées par des modèles d'apprentissage statistique et ne constituent pas une expertise légale d'assurance.

---

## 👥 Auteurs & Contact

- **Achraf Mentagui** — *Data Science & Machine Learning Engineering*
- **Rihab El Marikh** — *Data Engineering & Modélisation Statistique*

Pour toute question, collaboration de recherche ou retour d'expérience :
- Ouvrez une [Issue GitHub](https://github.com/username/autocote-maroc/issues).
- Rejoignez les discussions sur le repository.
