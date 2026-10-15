import sys
from pathlib import Path
from datetime import datetime
import streamlit as st

# Assurer que la racine du projet est dans sys.path pour importer 'src'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.predict import CarPricePredictor

st.set_page_config(
    page_title="Estimateur Premium Auto Maroc",
    page_icon="🚗",
    layout="wide"
)

# Background styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.88), rgba(255, 255, 255, 0.88)),
                    url('https://images.unsplash.com/photo-1503376780353-7e6692767b70?ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80');
        background-blend-mode: overlay;
        background-size: cover;
        background-position: 60% center;
        background-attachment: fixed;
    }
</style>
""", unsafe_allow_html=True)

# Custom CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');

    :root {
        --primary: #8A2BE2;
        --secondary: #FF6B6B;
        --accent: #4ECDC4;
    }

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    .stForm {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    .header-section {
        text-align: center;
        margin-bottom: 2rem;
        padding: 1.5rem 0;
    }

    .title {
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        background: linear-gradient(45deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem !important;
    }

    .title1 {
        font-weight: 600 !important;
        color: #555;
        font-size: 1.1rem;
    }

    .stButton button {
        background: linear-gradient(45deg, var(--primary), var(--secondary)) !important;
        border: none !important;
        color: white !important;
        font-size: 1.1rem !important;
        border-radius: 12px !important;
        padding: 0.8rem 1.5rem !important;
        font-weight: 600;
        transition: all 0.3s ease !important;
    }

    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 20px rgba(138, 43, 226, 0.3) !important;
    }

    .success-box {
        background: linear-gradient(45deg, #20bf6b, #26de81) !important;
        color: white !important;
        padding: 2rem !important;
        border-radius: 20px !important;
        text-align: center !important;
        margin-top: 2rem !important;
        box-shadow: 0 8px 25px rgba(32, 191, 107, 0.3);
    }

    .copyright {
        text-align: center;
        color: #666;
        font-size: 0.9rem;
        padding: 2rem 0 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
with st.container():
    st.markdown('<div class="header-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="title">Estimateur Premium Auto</h1>', unsafe_allow_html=True)
    st.markdown('<p class="title1">Votre estimation intelligente de véhicule d\'occasion au Maroc (Avito)</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Load predictor cached
@st.cache_resource
def get_predictor():
    return CarPricePredictor()

try:
    predictor = get_predictor()
except Exception as e:
    st.error(f"⚠️ Impossible de charger le modèle de prédiction : {e}")
    predictor = None

# Input Form
with st.form("car_form"):
    cols = st.columns([5, 1, 5])
    with cols[0]:
        st.subheader("📋 Profil du véhicule")
        year = st.number_input(
            "Année de fabrication",
            min_value=1990,
            max_value=datetime.now().year,
            value=2017
        )
        marke = st.text_input("Marque", value="Dacia")
        model_name = st.text_input("Modèle", value="Logan")
        city = st.text_input("Ville d'immatriculation", value="Casablanca")

    with cols[2]:
        st.subheader("⚙️ Caractéristiques techniques")
        type_boit = st.selectbox(
            "Type de boîte",
            ["Manuelle", "Automatique"],
            index=0
        )
        type_carburant = st.selectbox(
            "Carburant",
            ["Diesel", "Essence", "Hybride", "Electrique"],
            index=0
        )
        puissance = st.text_input("Puissance (CV)", value="6 cv")
        kilometrage = st.text_input(
            "Kilométrage (ex: 100000 ou 100 000 - 120 999)",
            value="100000"
        )
        premiere_main = st.selectbox("Première main", ["Non", "Oui"], index=0)
        nombre_doors = st.text_input("Nombre de portes", value="5")

    submitted = st.form_submit_button("✨ Obtenir l'estimation premium")

if submitted and predictor is not None:
    user_data = {
        "year": int(year),
        "marke": marke,
        "model": model_name,
        "type_boit": type_boit,
        "type_carburant": type_carburant,
        "puissance": puissance,
        "kilometrage": kilometrage,
        "premiere_main": premiere_main,
        "Nombre_doors": nombre_doors,
        "city": city,
    }
    try:
        with st.spinner("Analyse approfondie en cours..."):
            predicted_price = predictor.predict(user_data)

        st.markdown(f"""
        <div class="success-box">
            <h2 style="margin:0;font-weight:700;">ESTIMATION CERTIFIÉE</h2>
            <p style="font-size:2.4rem;margin:1rem 0;font-weight:800;">{predicted_price:,.2f} MAD</p>
            <small>Évaluation statistique basée sur les tendances du marché marocain</small>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"🚨 Une erreur est survenue lors de l'estimation : {str(e)}")

# Copyright
st.markdown("""
<div class="copyright">
    © 2024 Tous droits réservés - Conçu par Achraf Mentagui
</div>
""", unsafe_allow_html=True)

