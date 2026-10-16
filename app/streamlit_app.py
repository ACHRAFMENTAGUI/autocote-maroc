import json
import os
import sys
import textwrap
from datetime import datetime
from pathlib import Path
import streamlit as st

# 1. Résolution dynamique du projet root pour imports 'src'
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

TAUX_EUR_MAD = float(os.getenv("TAUX_EUR_MAD", "10.85"))
CURRENT_YEAR = datetime.now().year

# ---------------------------------------------------------
# ✅ FIX #1 : Helper pour rendre le HTML proprement
# ---------------------------------------------------------
def render_html(html: str):
    """Nettoie (dedent + strip) et affiche du HTML dans Streamlit."""
    st.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)

# ---------------------------------------------------------
# 1. CSS CUSTOM COMPLET (FINTECH : BLEU NUIT, ÉMERAUDE, ARDOISE)
# ---------------------------------------------------------
FINTECH_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        --color-dark: #0F172A;
        --color-dark-surface: #1E293B;
        --color-emerald: #10B981;
        --color-emerald-light: #34D399;
        --color-slate: #94A3B8;
        --color-slate-light: #F1F5F9;
        --color-border: #E2E8F0;
        --color-bg: #F8FAFC;
    }

    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background-color: var(--color-bg);
    }

    /* En-tête Hero */
    .hero-container {
        text-align: center;
        padding: 1.8rem 1rem 1.2rem 1rem;
        margin-bottom: 0.8rem;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: #0F172A;
        color: #34D399;
        font-weight: 700;
        font-size: 0.78rem;
        padding: 0.35rem 0.9rem;
        border-radius: 9999px;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        border: 1px solid rgba(52, 211, 153, 0.3);
        margin-bottom: 0.6rem;
    }

    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.2;
        margin-bottom: 0.3rem;
    }

    .hero-title span {
        background: linear-gradient(135deg, #0F172A 0%, #10B981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 0.98rem;
        color: #64748B;
        max-width: 620px;
        margin: 0 auto;
        font-weight: 500;
    }

    /* Cartes formulaire et sections */
    .custom-card {
        background: #FFFFFF;
        border: 1px solid var(--color-border);
        border-radius: 16px;
        padding: 1.3rem;
        box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.04);
        margin-bottom: 1.2rem;
    }

    .card-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--color-dark);
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--color-slate-light);
    }

    /* Modernisation des champs Selectbox et Slider */
    div[data-baseweb="select"] > div {
        border-radius: 10px !important;
        border: 1px solid #CBD5E1 !important;
        transition: all 0.2s ease !important;
    }

    div[data-baseweb="select"] > div:hover {
        border-color: #34D399 !important;
    }

    div[data-baseweb="select"] > div:focus-within {
        border-color: #10B981 !important;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15) !important;
    }

    /* Slider styling */
    div[data-testid="stSlider"] > div > div > div > div {
        background-color: #10B981 !important;
    }

    /* Modernisation des Boutons */
    .stButton>button {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%) !important;
        color: #FFFFFF !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 0.8rem 1.6rem !important;
        border: 1px solid #334155 !important;
        box-shadow: 0 8px 20px -4px rgba(15, 23, 42, 0.3) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease !important;
    }

    .stButton>button:hover {
        transform: translateY(-2px) !important;
        border-color: #34D399 !important;
        box-shadow: 0 12px 25px -4px rgba(16, 185, 129, 0.25) !important;
    }

    /* Boutons de raccourcis */
    div[data-testid="column"] .stButton>button {
        font-size: 0.88rem !important;
        padding: 0.5rem 0.8rem !important;
        border-radius: 10px !important;
    }

    /* Carte de Résultat Fintech */
    .result-card {
        background: linear-gradient(145deg, #0F172A 0%, #1E293B 100%);
        border-radius: 18px;
        padding: 1.8rem;
        color: #FFFFFF;
        box-shadow: 0 20px 35px -8px rgba(15, 23, 42, 0.35);
        border: 1px solid rgba(52, 211, 153, 0.2);
        text-align: center;
        margin-bottom: 1.2rem;
        position: relative;
    }

    .result-badge {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #94A3B8;
        margin-bottom: 0.4rem;
    }

    .result-price-mad {
        font-size: 3rem;
        font-weight: 800;
        color: #34D399;
        letter-spacing: -0.02em;
        line-height: 1.1;
        margin: 0.3rem 0;
        text-shadow: 0 2px 14px rgba(52, 211, 153, 0.3);
    }

    .result-price-eur {
        font-size: 0.98rem;
        color: #CBD5E1;
        font-weight: 500;
        margin-bottom: 1.2rem;
    }

    /* Boîte de fourchette de négociation */
    .range-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 0.8rem 1rem;
        margin: 1rem 0;
    }

    .range-col { flex: 1; text-align: center; }
    .range-divider { width: 1px; height: 36px; background: rgba(255, 255, 255, 0.15); }
    .range-label { font-size: 0.7rem; color: #94A3B8; font-weight: 600; text-transform: uppercase; }
    .range-value { font-size: 1.05rem; font-weight: 700; color: #FFFFFF; margin-top: 0.15rem; }

    /* Badges Fiche Synthétique avec micro-interactions */
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
        transition: transform 0.15s ease, background-color 0.15s ease, border-color 0.15s ease;
    }

    .spec-badge:hover {
        transform: translateY(-2px);
        background-color: #EEF2F6;
        border-color: #34D399;
    }

    /* Animation Skeleton Loader */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.45; }
    }

    .skeleton-box {
        animation: pulse 1.4s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        background: #E2E8F0;
        border-radius: 8px;
    }

    /* Comparateur Cards */
    .compare-card {
        background: #FFFFFF;
        border: 2px solid #E2E8F0;
        border-radius: 16px;
        padding: 1.2rem;
        transition: border-color 0.2s ease;
    }
    .compare-card.winner {
        border-color: #10B981;
        box-shadow: 0 6px 20px -4px rgba(16, 185, 129, 0.2);
    }
</style>
"""
st.markdown(FINTECH_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# DONNÉES DE RÉFÉRENCE & CATALOGUE
# ---------------------------------------------------------
POPULAR_BRANDS = [
    "Dacia", "Renault", "Volkswagen", "Peugeot", "Hyundai", "Mercedes-Benz",
    "Fiat", "Ford", "Citroen", "Bmw", "Audi", "Toyota", "Kia", "Nissan",
    "Opel", "Seat", "Land Rover", "Jeep", "Suzuki", "Honda"
]

FALLBACK_MODELS = {
    "Dacia": ["Logan", "Sandero", "Duster", "Dokker", "Lodgy", "Stepway"],
    "Renault": ["Clio", "Megane", "Kangoo", "Captur", "Kadjar", "Symbol"],
    "Volkswagen": ["Golf", "Polo", "Passat", "Tiguan", "Touareg", "Caddy"],
    "Peugeot": ["208", "308", "2008", "3008", "5008", "Partner"],
    "Hyundai": ["Tucson", "I10", "I20", "I30", "Accent", "Creta"]
}

MOROCCAN_CITIES = [
    "Casablanca", "Rabat", "Marrakech", "Tanger", "Agadir", "Fès", "Meknès",
    "Kénitra", "Tétouan", "Salé", "Temara", "El Jadida", "Mohammedia", "Oujda",
    "Nador", "Safi", "Béni Mellal", "Khouribga", "Berrechid", "Autre..."
]

@st.cache_data
def get_catalog():
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
    return FALLBACK_MODELS, [b for b in POPULAR_BRANDS if b in FALLBACK_MODELS] + ["Autre..."]

catalog_dict, brand_options = get_catalog()

# ---------------------------------------------------------
# CHARGEMENT DU MODÈLE (RÉEL + FALLBACK MOCK)
# ---------------------------------------------------------
@st.cache_resource
def load_ml_model():
    try:
        from src.models.predict import CarPricePredictor
        return CarPricePredictor(), False
    except Exception:
        class MockPredictor:
            def predict(self, data: dict) -> float:
                year = data.get("year", 2018)
                km = data.get("kilometrage", 100000)
                brand = str(data.get("marke", "")).lower()
                base = 112000.0 if "dacia" in brand else 158000.0
                age = max(1, CURRENT_YEAR - year)
                return max(25000.0, base - (age * 5500.0) - (km / 10000.0) * 1600.0)
        return MockPredictor(), True

model_predictor, is_mock_mode = load_ml_model()

# ---------------------------------------------------------
# VALIDATION DES ENTRÉES & RÈGLES MÉTIER
# ---------------------------------------------------------
def valider_inputs(payload: dict) -> tuple[bool, list[str]]:
    warnings = []
    year = payload.get("year", CURRENT_YEAR)
    km = payload.get("kilometrage", 0)
    power = payload.get("puissance", 6)
    age = max(1, CURRENT_YEAR - year)

    if year > CURRENT_YEAR:
        return False, ["L'année de fabrication ne peut pas être dans le futur."]
    if year < 1990:
        return False, ["Le modèle prend en charge les véhicules construits après 1990."]

    if age <= 2 and km > 160000:
        warnings.append("⚠️ Kilométrage exceptionnellement élevé pour un véhicule récent (usage intensif / taxi).")
    if age >= 10 and km < 25000:
        warnings.append("⚠️ Kilométrage anormalement faible pour un véhicule de plus de 10 ans (compteur à vérifier).")
    if power > 25:
        warnings.append("ℹ️ Puissance fiscale importante (>25 CV) : taxe annuelle élevée au Maroc.")

    return True, warnings

# ---------------------------------------------------------
# ✅ FIX #2 : RENDU DU RÉSULTAT (dedent + strip)
# ---------------------------------------------------------
def afficher_resultat(valeur_mad, fourchette_basse, fourchette_haute, confiance="Élevé (84% R²)"):
    valeur_mad = max(10000.0, float(valeur_mad))
    fourchette_basse = max(8000.0, float(fourchette_basse))
    fourchette_haute = max(valeur_mad, float(fourchette_haute))
    eur_approx = round(valeur_mad / TAUX_EUR_MAD)

    # ✅ Construction du HTML sur une seule chaîne sans indentation parasite
    html_content = (
        '<div class="result-card">'
        '<div class="result-badge">Valeur Vénale Marché Estimée</div>'
        f'<div class="result-price-mad">{valeur_mad:,.0f} MAD</div>'
        f'<div class="result-price-eur">≈ {eur_approx:,.0f} € (Taux : 1 € = {TAUX_EUR_MAD:.2f} MAD)</div>'
        '<div class="range-container">'
        '<div class="range-col">'
        '<div class="range-label">Fourchette Basse</div>'
        f'<div class="range-value">{fourchette_basse:,.0f} MAD</div>'
        '</div>'
        '<div class="range-divider"></div>'
        '<div class="range-col">'
        '<div class="range-label">Fourchette Haute</div>'
        f'<div class="range-value">{fourchette_haute:,.0f} MAD</div>'
        '</div>'
        '</div>'
        '</div>'
    )
    st.markdown(html_content, unsafe_allow_html=True)

# ---------------------------------------------------------
# HERO BANNER
# ---------------------------------------------------------
render_html("""
<div class="hero-container">
    <div class="hero-badge">⚡ Argus Automobile & IA Maroc 2026</div>
    <h1 class="hero-title">Estimez la valeur réelle de votre <span>Voiture d'Occasion</span></h1>
    <p class="hero-subtitle">Algorithme LightGBM entraîné sur +29 000 transactions réelles au Maroc (Marché Auto Maroc).</p>
</div>
""")

if is_mock_mode:
    st.info("ℹ️ Mode Démonstration actif. Le modèle de production se charge depuis `models/lightgbm_model.pkl`.")

# ---------------------------------------------------------
# NAVIGATION PAR ONGLETS (ESTIMATION SIMPLE VS COMPARATEUR)
# ---------------------------------------------------------
tab_estimation, tab_comparateur = st.tabs(["📊 Estimation Simple", "⚖️ Mode Comparateur (2 Véhicules)"])

PRESETS = {
    "dacia": {"marke": "Dacia", "model": "Logan", "year": 2018, "city": "Casablanca", "kilometrage": 110000, "type_carburant": "Diesel", "type_boit": "Manuelle", "puissance": 6, "premiere_main": "Oui", "Nombre_doors": 5},
    "golf": {"marke": "Volkswagen", "model": "Golf", "year": 2019, "city": "Rabat", "kilometrage": 85000, "type_carburant": "Diesel", "type_boit": "Automatique", "puissance": 8, "premiere_main": "Oui", "Nombre_doors": 5},
    "clio": {"marke": "Renault", "model": "Clio", "year": 2017, "city": "Marrakech", "kilometrage": 125000, "type_carburant": "Diesel", "type_boit": "Manuelle", "puissance": 6, "premiere_main": "Non", "Nombre_doors": 5},
    "peugeot": {"marke": "Peugeot", "model": "208", "year": 2020, "city": "Tanger", "kilometrage": 65000, "type_carburant": "Diesel", "type_boit": "Manuelle", "puissance": 5, "premiere_main": "Oui", "Nombre_doors": 5}
}

# =========================================================
# TAB 1 : ESTIMATION SIMPLE
# =========================================================
with tab_estimation:
    if "form_data" not in st.session_state:
        st.session_state.form_data = PRESETS["dacia"].copy()

    st.markdown("##### ⚡ Raccourcis Profils Types :")
    p1, p2, p3, p4, p5 = st.columns(5)
    with p1:
        if st.button("🚙 Dacia Logan", key="p_dacia", use_container_width=True):
            st.session_state.form_data = PRESETS["dacia"].copy(); st.rerun()
    with p2:
        if st.button("🏎️ Golf 7", key="p_golf", use_container_width=True):
            st.session_state.form_data = PRESETS["golf"].copy(); st.rerun()
    with p3:
        if st.button("🚗 Renault Clio", key="p_clio", use_container_width=True):
            st.session_state.form_data = PRESETS["clio"].copy(); st.rerun()
    with p4:
        if st.button("🚘 Peugeot 208", key="p_208", use_container_width=True):
            st.session_state.form_data = PRESETS["peugeot"].copy(); st.rerun()
    with p5:
        if st.button("🔄 Reset", key="p_reset", use_container_width=True):
            st.session_state.form_data = PRESETS["dacia"].copy(); st.rerun()

    st.write("")

    # Layout Responsive 2 Colonnes Desktop -> 1 Colonne Mobile
    col_form, col_panel = st.columns([1.15, 0.85], gap="large")

    with col_form:
        # ✅ FIX #3 : Utilisation du helper render_html
        render_html('<div class="custom-card"><div class="card-header">🏷️ Identité & Localisation</div></div>')

        c1, c2 = st.columns(2)
        with c1:
            cur_brand = st.session_state.form_data.get("marke", "Dacia")
            b_idx = brand_options.index(cur_brand) if cur_brand in brand_options else 0
            selected_brand = st.selectbox("Marque", brand_options, index=b_idx, key="s_brand")
            brand_final = st.text_input("Préciser marque", "Autre", key="t_brand") if selected_brand == "Autre..." else selected_brand
            models_list = catalog_dict.get(selected_brand, ["Autre..."]) + (["Autre..."] if "Autre..." not in catalog_dict.get(selected_brand, []) else [])
        with c2:
            cur_model = st.session_state.form_data.get("model", "")
            m_idx = models_list.index(cur_model) if cur_model in models_list else 0
            selected_model = st.selectbox("Modèle commercial", models_list, index=m_idx, key="s_model")
            model_final = st.text_input("Préciser modèle", "Logan", key="t_model") if selected_model == "Autre..." else selected_model

        c3, c4 = st.columns(2)
        with c3:
            years_range = list(range(CURRENT_YEAR, 1989, -1))
            cur_year = st.session_state.form_data.get("year", 2018)
            selected_year = st.selectbox("Année mise en circulation", years_range, index=years_range.index(cur_year) if cur_year in years_range else 6, key="s_year")
        with c4:
            cur_city = st.session_state.form_data.get("city", "Casablanca")
            selected_city = st.selectbox("Ville", MOROCCAN_CITIES, index=MOROCCAN_CITIES.index(cur_city) if cur_city in MOROCCAN_CITIES else 0, key="s_city")
            city_final = st.text_input("Préciser ville", "Casablanca", key="t_city") if selected_city == "Autre..." else selected_city

        render_html('<div class="custom-card"><div class="card-header">⚙️ Motorisation & Kilométrage</div></div>')

        f1, f2 = st.columns(2)
        with f1:
            fuels = ["Diesel", "Essence", "Hybride", "Electrique"]
            cur_fuel = st.session_state.form_data.get("type_carburant", "Diesel")
            selected_fuel = st.selectbox("Carburant", fuels, index=fuels.index(cur_fuel) if cur_fuel in fuels else 0, key="s_fuel")
        with f2:
            gearboxes = ["Manuelle", "Automatique"]
            cur_gear = st.session_state.form_data.get("type_boit", "Manuelle")
            selected_gear = st.selectbox("Boîte", gearboxes, index=gearboxes.index(cur_gear) if cur_gear in gearboxes else 0, key="s_gear")

        f3, f4, f5 = st.columns(3)
        with f3:
            selected_power = st.number_input("Puissance (CV)", 3, 35, int(st.session_state.form_data.get("puissance", 6)), key="n_power")
        with f4:
            door_choices = [5, 4, 3]
            selected_doors = st.selectbox("Portes", door_choices, index=door_choices.index(int(st.session_state.form_data.get("Nombre_doors", 5))), key="s_doors")
        with f5:
            first_hand_choices = ["Oui", "Non"]
            selected_first = st.selectbox("Première main", first_hand_choices, index=first_hand_choices.index(st.session_state.form_data.get("premiere_main", "Oui")), key="s_first")

        cur_km_val = int(st.session_state.form_data.get("kilometrage", 110000))
        selected_km = st.slider("Kilométrage total (km)", 0, 350000, min(max(cur_km_val, 0), 350000), 5000, format="%d km", key="sl_km")

        submit_trigger = st.button("✨ Calculer l'Estimation Immédiate", key="btn_calc", use_container_width=True)

    with col_panel:
        age_vehicule = max(1, CURRENT_YEAR - selected_year)
        km_annuel = int(selected_km / age_vehicule)

        payload = {
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

        is_valid, validation_warnings = valider_inputs(payload)
        if not is_valid:
            for err in validation_warnings: st.error(err)
            prix_estime = 0.0
        else:
            for warn in validation_warnings: st.warning(warn)

            with st.spinner("Analyse du marché et prédiction LightGBM..."):
                try:
                    prix_estime = model_predictor.predict(payload)
                except Exception as e:
                    st.error(f"Erreur d'inférence : {e}")
                    prix_estime = 100000.0

        prix_plancher = round(prix_estime * 0.93, -2)
        prix_plafond = round(prix_estime * 1.07, -2)

        # Carte résultat
        afficher_resultat(prix_estime, prix_plancher, prix_plafond, "Élevé (84% R²)")

        # Tooltip explicatif Indice R² & Confiance
        with st.popover("ℹ️ Comprendre l'Indice de Confiance et le R² (84%)"):
            st.markdown("""
            **Pourquoi un R² de 84% ?**
            - **R² (Coefficient de détermination)** : Indique que **84% des variations de prix** observées sur le marché marocain sont fidèlement expliquées par les caractéristiques du véhicule (marque, modèle, âge, carburant, kilométrage).
            - **Fiabilité Élevée** : Le modèle s'appuie sur une base de **29 342 annonces réelles** d'marche-auto-maroc, assurant une robustesse face aux variations régionales.
            """)

        # Fiche synthétique
        render_html('<div class="custom-card"><div class="card-header">📋 Fiche Synthétique du Véhicule</div></div>')

        # ✅ FIX #4 : HTML en une seule chaîne (pas de décalage d'indentation)
        chips_html = (
            '<div style="margin-bottom: 0.8rem;">'
            f'<span class="spec-badge">🚘 {brand_final} {model_final}</span>'
            f'<span class="spec-badge">📅 Année {selected_year} ({age_vehicule} ans)</span>'
            f'<span class="spec-badge">📍 {city_final}</span>'
            f'<span class="spec-badge">⛽ {selected_fuel}</span>'
            f'<span class="spec-badge">🕹️ {selected_gear}</span>'
            f'<span class="spec-badge">⚡ {selected_power} CV</span>'
            f'<span class="spec-badge">🛣️ {selected_km:,.0f} km</span>'
            f"<span class=\"spec-badge\">⭐ {'1ère main' if selected_first == 'Oui' else '2ème main +'}</span>"
            '</div>'
        )
        st.markdown(chips_html, unsafe_allow_html=True)

        km_tag = "Faible roulage (Atout revente)" if km_annuel < 12000 else ("Standard marocain" if km_annuel <= 20000 else "Roulage intensif")
        km_color = "#10B981" if km_annuel < 12000 else ("#3B82F6" if km_annuel <= 20000 else "#F59E0B")

        # ✅ FIX #5 : Balises correctement fermées (suppression du </div> orphelin)
        usage_html = (
            '<div style="padding: 0.85rem; background: #F8FAFC; border-radius: 12px; border: 1px solid #E2E8F0; margin-top: 0.6rem;">'
            '<div style="font-size: 0.72rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Intensité d\'utilisation annuelle</div>'
            f'<div style="font-size: 1.05rem; font-weight: 700; color: {km_color}; margin: 0.2rem 0;">{km_annuel:,.0f} km / an • {km_tag}</div>'
            f'<div style="font-size: 0.78rem; color: #94A3B8;">Moyenne calculée sur {selected_km:,.0f} km en {age_vehicule} an(s).</div>'
            '</div>'
        )
        st.markdown(usage_html, unsafe_allow_html=True)

        # 5. Bouton "Copier le résultat"
        st.markdown("##### 📋 Exporter ou Copier le Résultat :")
        rapport_export = f"""[AutoCote Maroc 2026]
Véhicule : {brand_final} {model_final} ({selected_year})
Kilométrage : {selected_km:,.0f} km ({km_annuel:,.0f} km/an)
Carburant / Boîte : {selected_fuel} | {selected_gear} | {selected_power} CV
Ville : {city_final}
----------------------------------------
VALEUR ESTIMÉE : {prix_estime:,.0f} MAD (≈ {round(prix_estime/TAUX_EUR_MAD):,.0f} €)
Fourchette marché : {prix_plancher:,.0f} - {prix_plafond:,.0f} MAD
Indice de confiance : 84% (Modèle LightGBM)"""

        st.code(rapport_export, language="markdown")

# =========================================================
# TAB 2 : MODE COMPARATEUR (2 VÉHICULES CÔTE À CÔTE)
# =========================================================
with tab_comparateur:
    st.markdown("#### ⚖️ Comparaison Immédiate de 2 Véhicules d'Occasion")
    st.caption("Analysez l'écart de cote, de kilométrage et de décote entre deux options d'achat ou de vente.")

    col_v1, col_v2 = st.columns(2, gap="large")

    # Véhicule A
    with col_v1:
        render_html('<div class="compare-card"><h4>🚗 Véhicule A</h4></div>')
        v1_brand = st.selectbox("Marque A", brand_options, index=brand_options.index("Dacia") if "Dacia" in brand_options else 0, key="v1_b")
        v1_models = catalog_dict.get(v1_brand, ["Autre..."])
        v1_model = st.selectbox("Modèle A", v1_models, index=0, key="v1_m")
        v1_year = st.selectbox("Année A", list(range(CURRENT_YEAR, 1994, -1)), index=6, key="v1_y")
        v1_km = st.slider("Kilométrage A (km)", 0, 300000, 110000, 5000, key="v1_km")
        v1_fuel = st.selectbox("Carburant A", ["Diesel", "Essence", "Hybride"], index=0, key="v1_f")
        v1_gear = st.selectbox("Boîte A", ["Manuelle", "Automatique"], index=0, key="v1_g")
        v1_power = st.number_input("CV A", 3, 25, 6, key="v1_p")
        v1_city = st.selectbox("Ville A", MOROCCAN_CITIES, index=0, key="v1_c")

    # Véhicule B
    with col_v2:
        render_html('<div class="compare-card"><h4>🚙 Véhicule B</h4></div>')
        v2_brand = st.selectbox("Marque B", brand_options, index=brand_options.index("Renault") if "Renault" in brand_options else 1, key="v2_b")
        v2_models = catalog_dict.get(v2_brand, ["Autre..."])
        v2_model = st.selectbox("Modèle B", v2_models, index=0, key="v2_m")
        v2_year = st.selectbox("Année B", list(range(CURRENT_YEAR, 1994, -1)), index=7, key="v2_y")
        v2_km = st.slider("Kilométrage B (km)", 0, 300000, 125000, 5000, key="v2_km")
        v2_fuel = st.selectbox("Carburant B", ["Diesel", "Essence", "Hybride"], index=0, key="v2_f")
        v2_gear = st.selectbox("Boîte B", ["Manuelle", "Automatique"], index=0, key="v2_g")
        v2_power = st.number_input("CV B", 3, 25, 6, key="v2_p")
        v2_city = st.selectbox("Ville B", MOROCCAN_CITIES, index=1, key="v2_c")

    # Calculs de comparaison
    p1_data = {"year": int(v1_year), "marke": v1_brand, "model": v1_model, "type_boit": v1_gear, "type_carburant": v1_fuel, "puissance": float(v1_power), "kilometrage": float(v1_km), "premiere_main": "Oui", "Nombre_doors": 5.0, "city": v1_city}
    p2_data = {"year": int(v2_year), "marke": v2_brand, "model": v2_model, "type_boit": v2_gear, "type_carburant": v2_fuel, "puissance": float(v2_power), "kilometrage": float(v2_km), "premiere_main": "Oui", "Nombre_doors": 5.0, "city": v2_city}

    pred_a = model_predictor.predict(p1_data)
    pred_b = model_predictor.predict(p2_data)
    delta_price = pred_b - pred_a
    pct_diff = (delta_price / pred_a) * 100 if pred_a > 0 else 0

    st.write("")
    st.markdown("### 📊 Résultats du Match Comparatif")

    r_col1, r_col2, r_col3 = st.columns(3)
    r_col1.metric(f"Prix {v1_brand} {v1_model}", f"{pred_a:,.0f} MAD", delta=f"{v1_year}")
    r_col2.metric(f"Prix {v2_brand} {v2_model}", f"{pred_b:,.0f} MAD", delta=f"{delta_price:+,.0f} MAD ({pct_diff:+.1f}%)", delta_color="inverse")

    economique = f"{v1_brand} {v1_model}" if pred_a < pred_b else f"{v2_brand} {v2_model}"
    r_col3.metric("Option la plus accessible", economique, delta=f"Économie : {abs(delta_price):,.0f} MAD")

    st.dataframe([
        {"Critère": "Cote Estimée (MAD)", "Véhicule A": f"{pred_a:,.0f} MAD", "Véhicule B": f"{pred_b:,.0f} MAD", "Écart": f"{abs(delta_price):,.0f} MAD"},
        {"Critère": "Âge", "Véhicule A": f"{CURRENT_YEAR - v1_year} ans", "Véhicule B": f"{CURRENT_YEAR - v2_year} ans", "Écart": f"{abs(v1_year - v2_year)} an(s)"},
        {"Critère": "Kilométrage Annuel", "Véhicule A": f"{int(v1_km/max(1, CURRENT_YEAR - v1_year)):,.0f} km/an", "Véhicule B": f"{int(v2_km/max(1, CURRENT_YEAR - v2_year)):,.0f} km/an", "Écart": f"{abs(int(v1_km/max(1, CURRENT_YEAR - v1_year)) - int(v2_km/max(1, CURRENT_YEAR - v2_year))):,.0f} km"},
        {"Critère": "Carburant & Boîte", "Véhicule A": f"{v1_fuel} ({v1_gear})", "Véhicule B": f"{v2_fuel} ({v2_gear})", "Écart": "Identique" if v1_fuel == v2_fuel and v1_gear == v2_gear else "Différent"}
    ], use_container_width=True)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
render_html("""
<div style="text-align: center; padding: 2rem 0 1rem 0; color: #94A3B8; font-size: 0.85rem;">
    🚗 <strong>AutoCote Maroc</strong> • Développé par <strong>Achraf Mentagui</strong><br>
    Modèle de Machine Learning entraîné sur les données d'marche-auto-maroc • Conforme MLOps
</div>
""")