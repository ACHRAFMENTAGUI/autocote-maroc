import pytest
from src.models.predict import CarPricePredictor

@pytest.fixture
def sample_car_input():
    return {
        "year": 2017,
        "marke": "Dacia",
        "model": "Logan",
        "type_boit": "Manuelle",
        "type_carburant": "Diesel",
        "puissance": "6 cv",
        "kilometrage": "100000",
        "premiere_main": "Non",
        "Nombre_doors": "5",
        "city": "Casablanca"
    }

def test_model_loading_and_prediction(sample_car_input):
    predictor = CarPricePredictor()
    pred_price = predictor.predict(sample_car_input)

    assert isinstance(pred_price, float)
    assert pred_price > 10000.0, "La prédiction pour un véhicule roulant doit être positive et réaliste"
    assert pred_price < 2000000.0, "La prédiction ne doit pas être démesurément haute"

def test_unseen_categories_handling(sample_car_input):
    """Test resilience against unseen categories (OHE handle_unknown='ignore')."""
    sample_car_input["city"] = "UnknownCity999"
    sample_car_input["marke"] = "RareBrandXYZ"
    predictor = CarPricePredictor()
    pred_price = predictor.predict(sample_car_input)

    assert isinstance(pred_price, float)
    assert pred_price > 0.0
