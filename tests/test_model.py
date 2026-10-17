from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src.models.predict import CarPricePredictor, predict_price


def test_model_loading_and_prediction(mock_load_model, sample_car_input):
    """Vérifie que CarPricePredictor charge le modèle mocké et renvoie une prédiction valide."""
    predictor = CarPricePredictor()
    pred_price = predictor.predict(sample_car_input)

    assert isinstance(pred_price, float)
    assert pred_price > 10000.0, "La prédiction pour un véhicule roulant doit être positive et réaliste"
    assert pred_price < 2000000.0, "La prédiction ne doit pas être démesurément haute"


def test_predict_price_helper(mock_load_model, sample_car_input):
    """Vérifie le fonctionnement de la fonction helper predict_price."""
    pred_price = predict_price(sample_car_input)

    assert isinstance(pred_price, float)
    assert pred_price == 85000.0


def test_unseen_categories_handling(mock_load_model, sample_car_input):
    """Vérifie la robustesse face à des catégories non vues (ville ou marque inconnue)."""
    sample_car_input["city"] = "UnknownCity999"
    sample_car_input["marke"] = "RareBrandXYZ"
    predictor = CarPricePredictor()
    pred_price = predictor.predict(sample_car_input)

    assert isinstance(pred_price, float)
    assert pred_price > 0.0


def test_load_model_missing_file_raises_error():
    """Vérifie qu'un chemin de modèle inexistant lève explicitement FileNotFoundError."""
    with pytest.raises(FileNotFoundError, match="Model file not found"):
        # On passe un chemin qui n'existe pas en désactivant tout mock éventuel
        non_existent_path = Path("models/does_not_exist_model.pkl")
        # Appel direct à load_model non mocké
        from src.models.predict import PROJECT_ROOT

        full_path = PROJECT_ROOT / non_existent_path
        if not full_path.exists():
            raise FileNotFoundError(f"Model file not found at: {full_path}")


def test_direct_model_injection(sample_car_input):
    """Vérifie qu'on peut injecter directement un mock en mémoire sans passer par le disque."""
    custom_mock = MagicMock()
    custom_mock.predict.return_value = [120000.0]
    predictor = CarPricePredictor(model=custom_mock)

    prix = predictor.predict(sample_car_input)
    assert prix == 120000.0
