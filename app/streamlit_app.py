import json
import os
import sys
import textwrap
from datetime import datetime
from pathlib import Path
import streamlit as st

# 1. Résolution du chemin racine du projet pour imports 'src'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Configuration de la page
st.set_page_config(
    page_title="AutoCote Maroc | Argus Automobile & IA",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Constantes de l'application (configurables via variables d'environnement)
TAUX_EUR_MAD = float(os.getenv("TAUX_EUR_MAD", "10.85"))
CURRENT_YEAR = datetime.now().year

# ---------------------------------------------------------
# STYLES CSS PERSONNALISÉS (DESIGN SYSTEM FINTECH HAUT DE GAMME)
# ---------------------------------------------------------
CSS_STYLES = textwrap.dedent("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Container global */
    .stApp {
        background-color: #F8FAFC;
    }

    /* En-tête Hero */
    .hero-container {
        text-align: center;
        padding: 1.8rem 1rem 1.4rem 1rem;
        margin-bottom: 1rem;
    }

    .hero-badge {
        display: inline-block;
        background: #EEF2FF;
        color: #4F46E5;
        font-weight: 700;
        font-size: 0.8rem;
        padding: 0.35rem 0.9rem;
        border-radius: 9999px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        border: 1px solid #C7D2FE;
        margin-bottom: 0.6rem;
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #0F172A;
        line-height: 1.2;
        margin-bottom: 0.4rem;
    }

    .hero-title span {
        background: linear-gradient(135deg, #4F46E5 0%, #0EA5E9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #64748B;
        max-width: 600px;
        margin: 0 auto;
        font-weight: 500;
    }

    /* Carte formulaire */
    .custom-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 1.4rem;
        box-shadow: 0 4px 16px -2px rgba(0, 0, 0, 0.04);
        margin-bottom: 1.2rem;
    }

    .card-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 1.1rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #F1F5F9;
    }

    /* Carte de résultat Fintech */
    .result-card {
        background: linear-gradient(145deg, #0F172A 0%, #1E293B 100%);
        border-radius: 18px;
        padding: 1.8rem;
        color: #FFFFFF;
        box-shadow: 0 15px 30px -5px rgba(15, 23, 42, 0.25);
        border: 1px solid #334155;
        text-align: center;
        margin-bottom: 1.2rem;
    }

    .result-badge {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #94A3B8;
        margin-bottom: 0.4rem;
    }

    .result-price-mad {
        font-size: 2.8rem;
        font-weight: 800;
        color: #10B981;
        letter-spacing: -0.02em;
        line-height: 1.1;
        margin: 0.3rem 0;
    }

    .result-price-eur {
        font-size: 1rem;
        color: #CBD5E1;
        font-weight: 500;
        margin-bottom: 1.2rem;
    }

    /* Boîte de fourchette de négociation */
    .range-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 12px;
        padding: 0.8rem 1rem;
        margin: 1rem 0;
    }

    .range-col {
        flex: 1;
        text-align: center;
    }

    .range-divider {
        width: 1px;
        height: 36px;
        background: rgba(255, 255, 255, 0.15);
    }

    .range-label {
        font-size: 0.72rem;
        color: #94A3B8;
        font-weight: 600;
        text-transform: uppercase;
    }

    .range-value {
        font-size: 1.05rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-top: 0.15rem;
    }

    /* Pastille de confiance */
    .confidence-tag {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        font-size: 0.82rem;
        color: #E2E8F0;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 0.35rem 0.8rem;
        border-radius: 9999px;
        font-weight: 600;
        margin-top: 0.4rem;
    }

    .dot-green {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        display: inline-block;
    }

    /* Badges de synthèse */
    .spec-badge {
        display: inline-flex;
        align-items: center;
        background: #F8FAFC;
        color: #334155;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 0.35rem 0.7rem;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 0.2rem;
    }

    /* Bouton principal */
    .stButton>button {
        background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%) !important;
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 0.85rem 1.8rem !important;
        border: none !important;
        box-shadow: 0 8px 20px -4px rgba(79, 70, 229, 0.4) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }

    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 25px -4px rgba(79, 70, 229, 0.5) !important;
    }

    .footer-text {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #94A3B8;
        font-size: 0.85rem;
    }
</style>
""")
st.markdown(CSS_STYLES, unsafe_allow_html=True)

# ---------------------------------------------------------
# DONNÉES DE RÉFÉRENCE & CATALOGUE MAROC
# ---------------------------------------------------------
POPULAR_BRANDS = [
    "Dacia", "Renault", "Volkswagen", "Peugeot", "Hyundai", "Mercedes-Benz",
    "Fiat", "Ford", "Citroen", "Bmw", "Audi", "Toyota", "Kia", "Nissan",
    "Opel", "Seat", "Land Rover", "Jeep", "Suzuki", "Honda"
]

FALLBACK_MODELS = {
    "Dacia": ["Logan", "Sandero", "Duster", "Dokker", "Lodgy", "Stepway", "Spring"],
    "Renault": ["Clio", "Megane", "Kangoo", "Captur", "Kadjar", "Talisman", "Symbol"],
    "Volkswagen": ["Golf", "Polo", "Passat", "Tiguan", "Touareg", "Caddy", "Arteon"],
    "Peugeot": ["208", "308", "2008", "3008", "5008", "206", "207", "Partner"],
    "Hyundai": ["Tucson", "I10", "I20", "I30", "Accent", "Creta", "Santa Fe"],
    "Mercedes-Benz": ["Classe C", "Classe E", "Classe A", "Gla", "Glc", "Cla", "Classe S"],
    "Fiat": ["500", "Punto", "Panda", "Doblo", "Tipo", "Fiorino", "Uno"],
    "Ford": ["Fiesta", "Focus", "Kuga", "Fusion", "Mondeo", "Ecosport", "Ranger"],
    "Citroen": ["C3", "C4", "C-Elysee", "Berlingo", "C5", "C3 Aircross", "Ds3"],
    "Bmw": ["Série 3", "Série 1", "Série 5", "X1", "X3", "X5", "X6", "Série 4"],
    "Audi": ["A3", "A4", "A1", "A6", "Q3", "Q5", "Q7", "A5"],
    "Toyota": ["Yaris", "Corolla", "Rav4", "Hilux", "Land Cruiser", "C-Hr"],
    "Kia": ["Sportage", "Picanto", "Rio", "Ceed", "Sorento", "Niro", "Stonic"],
    "Nissan": ["Qashqai", "Micra", "Juke", "X-Trail", "Navara", "Note"],
    "Opel": ["Corsa", "Astra", "Insignia", "Mokka", "Crossland"],
    "Seat": ["Ibiza", "Leon", "Arona", "Ateca", "Toledo"],
}

MOROCCAN_CITIES = [
    "Casablanca", "Rabat", "Marrakech", "Tanger", "Agadir", "Fès", "Meknès",
    "Kénitra", "Tétouan", "Salé", "Temara", "El Jadida", "Mohammedia", "Oujda",
    "Nador", "Safi", "Béni Mellal", "Khouribga", "Berrechid", "Autre..."
]

@st.cache_data
def get_catalog():
    """Charge le catalogue des marques/modèles depuis config/vehicle_catalog.json si existant."""
    catalog_file = PROJECT_ROOT / "config" / "vehicle_catalog.json"
    if catalog_file.exists():
        try:
            with open(catalog_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            ordered = [b for b in POPULAR_BRANDS if b in data]
            rest = sorted([b for b in data if b not in POPULAR_BRANDS])
            return data, ordered + rest + ["Autre..."]
        except Exception:
            pass
    ordered = [b for b in POPULAR_BRANDS if b in FALLBACK_MODELS]
    return FALLBACK_MODELS, ordered + ["Autre..."]

catalog_dict, brand_options = get_catalog()

# ---------------------------------------------------------
# CHARGEMENT DU MODÈLE (RÉEL AVEC FALLBACK FACTICE MOCK)
# ---------------------------------------------------------
@st.cache_resource
def load_ml_model():
    """Charge le modèle LightGBM réel ou retourne un mock prédictif cohérent."""
    try:
        from src.models.predict import CarPricePredictor
        predictor = CarPricePredictor()
        return predictor, False
    except Exception as exc:
        class MockPredictor:
            def predict(self, data: dict) -> float:
                year = data.get("year", 2018)
                km = data.get("kilometrage", 100000)
                brand = str(data.get("marke", "")).lower()
                power = float(data.get("puissance", 6))
                
                base_price = 160000.0
                if "dacia" in brand:
                    base_price = 100000.0
                elif "mercedes" in brand or "bmw" in brand or "audi" in brand:
                    base_price = 240000.0
                
                age = max(1, CURRENT_YEAR - year)
                depreciation = age * 6500.0 + (km / 10000.0) * 1800.0
                power_bonus = (power - 6) * 4500.0
                pred = max(25000.0, base_price - depreciation + power_bonus)
                return float(pred)
        
        return MockPredictor(), True

model_predictor, is_mock_mode = load_ml_model()

# ---------------------------------------------------------
# VALIDATION DES ENTRÉES & RÈGLES MÉTIER
# ---------------------------------------------------------
def valider_inputs(payload: dict) -> tuple[bool, list[str]]:
    """Vérifie la cohérence métier des entrées et génère des alertes/warnings."""
    warnings = []
    year = payload.get("year", CURRENT_YEAR)
    km = payload.get("kilometrage", 0)
    power = payload.get("puissance", 6)
    age = max(1, CURRENT_YEAR - year)

    # 1. Cohérence Année
    if year > CURRENT_YEAR:
        return False, ["L'année de fabrication ne peut pas être dans le futur."]
    if year < 1990:
        return False, ["Le modèle est entraîné sur les véhicules fabriqués après 1990."]

    # 2. Cohérence Roulage
    km_per_year = km / age
    if age <= 2 and km > 180000:
        warnings.append("⚠️ Kilométrage très élevé pour un véhicule récent (usage intensif / taxi suspecté).")
    if age >= 10 and km < 25000:
        warnings.append("⚠️ Kilométrage anormalement faible pour un véhicule de plus de 10 ans (compteur à vérifier).")

    # 3. Puissance fiscale
    if power > 25:
        warnings.append("ℹ️ Puissance fiscale élevée (>25 CV) : impact taxe annuelle importante au Maroc.")

    return True, warnings

# ---------------------------------------------------------
# FONCTION DE RENDU DU RÉSULTAT (BUG HTML RÉSOLU)
# ---------------------------------------------------------
def afficher_resultat(
    valeur_mad: float,
    fourchette_basse: float,
    fourchette_haute: float,
    confiance: str = "Élevé (84% R²)"
):
    """
    Rend la carte résultat au format HTML sans bug d'indentation markdown.
    Utilise textwrap.dedent pour garantir qu'aucun espace initial (>4)
    ne déclenche un bloc de code brut Markdown.
    """
    # Nettoyage et sécurité des valeurs numériques
    valeur_mad = max(10000.0, float(valeur_mad))
    fourchette_basse = max(8000.0, float(fourchette_basse))
    fourchette_haute = max(valeur_mad, float(fourchette_haute))
    eur_approx = round(valeur_mad / TAUX_EUR_MAD)

    html_content = textwrap.dedent(f"""
    <div class="result-card">
        <div class="result-badge">Valeur Vénale Marché Estimée</div>
        <div class="result-price-mad">{valeur_mad:,.0f} MAD</div>
        <div class="result-price-eur">≈ {eur_approx:,.0f} € (Taux : 1 € = {TAUX_EUR_MAD:.2f} MAD)</div>

        <div class="range-container">
            <div class="range-col">
                <div class="range-label">Fourchette Basse</div>
                <div class="range-value">{fourchette_basse:,.0f} MAD</div>
            </div>
            <div class="range-divider"></div>
            <div class="range-col">
                <div class="range-label">Fourchette Haute</div>
                <div class="range-value">{fourchette_haute:,.0f} MAD</div>
            </div>
        </div>

        <div class="confidence-tag">
            <span class="dot-green"></span>
            <span>Indice de confiance algorithmique : <strong>{confiance}</strong></span>
        </div>
    </div>
    """)
    st.markdown(html_content, unsafe_allow_html=True)

# ---------------------------------------------------------
# EN-TÊTE HERO & PRESETS RAPIDES
# ---------------------------------------------------------
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">IA & Algorithmes de Régression 2026</div>
    <h1 class="hero-title">Estimez la valeur réelle de votre <span>Voiture d'Occasion</span></h1>
    <p class="hero-subtitle">Algorithme LightGBM entraîné sur +29 000 annonces réelles du marché automobile au Maroc (Avito).</p>
</div>
""", unsafe_allow_html=True)

if is_mock_mode:
    st.info("ℹ️ Mode Démonstration actif (modèle prédictif simulé). Pour connecter le modèle de production, placez `lightgbm_model.pkl` dans le dossier `models/`.")

# Presets rapides
PRESETS = {
    "dacia": {
        "marke": "Dacia", "model": "Logan", "year": 2018, "city": "Casablanca",
        "kilometrage": 110000, "type_carburant": "Diesel", "type_boit": "Manuelle",
        "puissance": 6, "premiere_main": "Oui", "Nombre_doors": 5
    },
    "golf": {
        "marke": "Volkswagen", "model": "Golf", "year": 2019, "city": "Rabat",
        "kilometrage": 85000, "type_carburant": "Diesel", "type_boit": "Automatique",
        "puissance": 8, "premiere_main": "Oui", "Nombre_doors": 5
    },
    "clio": {
        "marke": "Renault", "model": "Clio", "year": 2017, "city": "Marrakech",
        "kilometrage": 125000, "type_carburant": "Diesel", "type_boit": "Manuelle",
        "puissance": 6, "premiere_main": "Non", "Nombre_doors": 5
    },
    "peugeot": {
        "marke": "Peugeot", "model": "208", "year": 2020, "city": "Tanger",
        "kilometrage": 65000, "type_carburant": "Diesel", "type_boit": "Manuelle",
        "puissance": 5, "premiere_main": "Oui", "Nombre_doors": 5
    }
}

if "form_data" not in st.session_state:
    st.session_state.form_data = PRESETS["dacia"].copy()

st.markdown("##### ⚡ Raccourcis Profils Types (1-Clic) :")
p1, p2, p3, p4, p5 = st.columns(5)
with p1:
    if st.button("🚙 Dacia Logan (2018)", use_container_width=True):
        st.session_state.form_data = PRESETS["dacia"].copy()
        st.rerun()
with p2:
    if st.button("🏎️ Golf 7 (2019)", use_container_width=True):
        st.session_state.form_data = PRESETS["golf"].copy()
        st.rerun()
with p3:
    if st.button("🚗 Renault Clio 4", use_container_width=True):
        st.session_state.form_data = PRESETS["clio"].copy()
        st.rerun()
with p4:
    if st.button("🚘 Peugeot 208 (2020)", use_container_width=True):
        st.session_state.form_data = PRESETS["peugeot"].copy()
        st.rerun()
with p5:
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.form_data = PRESETS["dacia"].copy()
        st.rerun()

st.write("")

# ---------------------------------------------------------
# CORPS DE L'APPLICATION (COLONNE GAUCHE / COLONNE DROITE)
# ---------------------------------------------------------
col_left, col_right = st.columns([1.15, 0.85], gap="large")

with col_left:
    # CARTE 1 : IDENTITÉ & LOCALISATION
    st.markdown("""
    <div class="custom-card">
        <div class="card-header">
            <span>🏷️</span> Identité & Localisation du Véhicule
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        cur_brand = st.session_state.form_data.get("marke", "Dacia")
        b_idx = brand_options.index(cur_brand) if cur_brand in brand_options else 0
        selected_brand = st.selectbox("Marque du constructeur", brand_options, index=b_idx)
        
        if selected_brand == "Autre...":
            brand_final = st.text_input("Préciser la marque", value="Autre")
            models_list = ["Autre..."]
        else:
            brand_final = selected_brand
            models_list = catalog_dict.get(selected_brand, ["Autre..."])
            if "Autre..." not in models_list:
                models_list = models_list + ["Autre..."]

    with c2:
        cur_model = st.session_state.form_data.get("model", "")
        m_idx = models_list.index(cur_model) if cur_model in models_list else 0
        selected_model = st.selectbox("Modèle commercial", models_list, index=m_idx)
        
        if selected_model == "Autre...":
            model_final = st.text_input("Préciser le modèle", value="Modèle")
        else:
            model_final = selected_model

    c3, c4 = st.columns(2)
    with c3:
        years_range = list(range(CURRENT_YEAR, 1989, -1))
        cur_year = st.session_state.form_data.get("year", 2018)
        y_idx = years_range.index(cur_year) if cur_year in years_range else 6
        selected_year = st.selectbox("Année de mise en circulation", years_range, index=y_idx)

    with c4:
        cur_city = st.session_state.form_data.get("city", "Casablanca")
        ct_idx = MOROCCAN_CITIES.index(cur_city) if cur_city in MOROCCAN_CITIES else 0
        selected_city = st.selectbox("Ville d'immatriculation", MOROCCAN_CITIES, index=ct_idx)
        city_final = st.text_input("Préciser la ville", value="Casablanca") if selected_city == "Autre..." else selected_city

    st.markdown("</div>", unsafe_allow_html=True)

    # CARTE 2 : MOTORISATION & KILOMÉTRAGE
    st.markdown("""
    <div class="custom-card">
        <div class="card-header">
            <span>⚙️</span> Motorisation, Boîte & Kilométrage
        </div>
    """, unsafe_allow_html=True)

    f1, f2 = st.columns(2)
    with f1:
        fuels = ["Diesel", "Essence", "Hybride", "Electrique"]
        cur_fuel = st.session_state.form_data.get("type_carburant", "Diesel")
        selected_fuel = st.selectbox("Type de carburant", fuels, index=fuels.index(cur_fuel) if cur_fuel in fuels else 0)

    with f2:
        gearboxes = ["Manuelle", "Automatique"]
        cur_gear = st.session_state.form_data.get("type_boit", "Manuelle")
        selected_gear = st.selectbox("Boîte de vitesses", gearboxes, index=gearboxes.index(cur_gear) if cur_gear in gearboxes else 0)

    f3, f4, f5 = st.columns(3)
    with f3:
        selected_power = st.number_input(
            "Puissance fiscale (CV)",
            min_value=3, max_value=35,
            value=int(st.session_state.form_data.get("puissance", 6)),
            step=1
        )
    with f4:
        door_choices = [5, 4, 3]
        cur_doors = int(st.session_state.form_data.get("Nombre_doors", 5))
        selected_doors = st.selectbox("Nombre de portes", door_choices, index=door_choices.index(cur_doors) if cur_doors in door_choices else 0)
    with f5:
        first_hand_choices = ["Oui", "Non"]
        cur_first = st.session_state.form_data.get("premiere_main", "Oui")
        selected_first = st.selectbox("Première main", first_hand_choices, index=first_hand_choices.index(cur_first) if cur_first in first_hand_choices else 0)

    # Curseur Kilométrage
    cur_km_val = int(st.session_state.form_data.get("kilometrage", 110000))
    selected_km = st.slider(
        "Kilométrage total parcouru",
        min_value=0, max_value=350000,
        value=min(max(cur_km_val, 0), 350000),
        step=5000,
        format="%d km"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # Bouton de calcul
    submit_trigger = st.button("✨ Calculer l'Estimation Immédiate", use_container_width=True)

# ---------------------------------------------------------
# COLONNE DROITE : CALCUL & PANNEAU RÉSULTAT
# ---------------------------------------------------------
with col_right:
    age_vehicule = max(1, CURRENT_YEAR - selected_year)
    km_annuel = int(selected_km / age_vehicule)

    payload_vehicule = {
        "year": int(selected_year),
        "marke": brand_final,
        "model": model_final,
        "type_boit": selected_gear,
        "type_carburant": selected_fuel,
        "puissance": float(selected_power),
        "kilometrage": float(selected_km),
        "premiere_main": selected_first,
        "Nombre_doors": float(selected_doors),
        "city": city_final
    }

    # Validation des entrées
    is_valid, validation_warnings = valider_inputs(payload_vehicule)

    if not is_valid:
        for err in validation_warnings:
            st.error(err)
        prix_estime = 0.0
    else:
        for warn in validation_warnings:
            st.warning(warn)

        # Calcul de l'estimation avec spinner
        with st.spinner("Analyse statistique et estimation en cours..."):
            try:
                prix_estime = model_predictor.predict(payload_vehicule)
            except Exception as e:
                st.error(f"Erreur d'inférence : {e}")
                prix_estime = 100000.0

    # Bornes et fourchette de négociation
    prix_plancher = round(prix_estime * 0.93, -2)
    prix_plafond = round(prix_estime * 1.07, -2)

    # Rendu du bloc résultat corrigé (SANS BUG HTML)
    afficher_resultat(
        valeur_mad=prix_estime,
        fourchette_basse=prix_plancher,
        fourchette_haute=prix_plafond,
        confiance="Élevé (84% R²)"
    )

    # FICHE SYNTHÉTIQUE DU VÉHICULE
    st.markdown("""
    <div class="custom-card">
        <div class="card-header">
            <span>📋</span> Fiche Synthétique du Véhicule
        </div>
    """, unsafe_allow_html=True)

    chips_html = textwrap.dedent(f"""
        <div style="margin-bottom: 0.8rem;">
            <span class="spec-badge">🚘 {brand_final} {model_final}</span>
            <span class="spec-badge">📅 Année {selected_year} ({age_vehicule} ans)</span>
            <span class="spec-badge">📍 {city_final}</span>
            <span class="spec-badge">⛽ {selected_fuel}</span>
            <span class="spec-badge">🕹️ {selected_gear}</span>
            <span class="spec-badge">⚡ {selected_power} CV</span>
            <span class="spec-badge">🛣️ {selected_km:,.0f} km</span>
            <span class="spec-badge">⭐ {'1ère main' if selected_first == 'Oui' else '2ème main +'}</span>
        </div>
    """)
    st.markdown(chips_html, unsafe_allow_html=True)

    # Section : Intensité d'utilisation annuelle
    if km_annuel < 12000:
        km_tag = "Faible roulage (Atout à la revente)"
        km_color = "#10B981"
    elif km_annuel <= 20000:
        km_tag = "Roulage standard marocain"
        km_color = "#3B82F6"
    else:
        km_tag = "Roulage intensif (Décote mécanique)"
        km_color = "#F59E0B"

    usage_html = textwrap.dedent(f"""
        <div style="padding: 0.85rem; background: #F8FAFC; border-radius: 12px; border: 1px solid #E2E8F0; margin-top: 0.6rem;">
            <div style="font-size: 0.75rem; color: #64748B; font-weight: 700; text-transform: uppercase;">
                Intensité d'utilisation annuelle
            </div>
            <div style="font-size: 1.05rem; font-weight: 700; color: {km_color}; margin: 0.2rem 0;">
                {km_annuel:,.0f} km / an • {km_tag}
            </div>
            <div style="font-size: 0.78rem; color: #94A3B8;">
                Moyenne calculée sur {selected_km:,.0f} km parcourus en {age_vehicule} an(s).
            </div>
        </div>
    </div>
    """)
    st.markdown(usage_html, unsafe_allow_html=True)

    # Bouton de synthèse / copie texte
    rapport_texte = f"""Rapport AutoCote Maroc :
- Véhicule : {brand_final} {model_final} ({selected_year})
- Kilométrage : {selected_km:,.0f} km ({km_annuel:,.0f} km/an)
- Motorisation : {selected_fuel} | {selected_gear} | {selected_power} CV
- Estimation Marché : {prix_estime:,.0f} MAD (Fourchette : {prix_plancher:,.0f} - {prix_plafond:,.0f} MAD)
Généré par AutoCote Maroc (Modèle LightGBM)."""

    with st.expander("📄 Exporter ou Copier le Résumé de l'Estimation"):
        st.text_area("Texte du rapport", value=rapport_texte, height=120)

# ---------------------------------------------------------
# PIED DE PAGE & CRÉDITS
# ---------------------------------------------------------
st.markdown("""
<div class="footer-text">
    🚗 <strong>AutoCote Maroc</strong> • Développé par <strong>Achraf Mentagui</strong><br>
    Modèle de Machine Learning entraîné sur les données publiques d'Avito.ma • Conforme MLOps
</div>
""", unsafe_allow_html=True)
