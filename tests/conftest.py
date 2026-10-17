from unittest.mock import MagicMock

import numpy as np
import pytest

from src.config import PROJECT_ROOT, config


@pytest.fixture
def sample_car_input() -> dict:
    """Fixture renvoyant un profil valide de véhicule pour les tests."""
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
        "city": "Casablanca",
    }


@pytest.fixture
def mock_pipeline():
    """Mock d'un pipeline scikit-learn / LightGBM prêt pour l'inférence."""
    pipeline = MagicMock()
    # Simule une prédiction réaliste de 85 000 MAD
    pipeline.predict.return_value = np.array([85000.0])
    pipeline.named_steps = {"cleaner": MagicMock(), "regressor": MagicMock()}
    return pipeline


@pytest.fixture
def mock_load_model(monkeypatch, mock_pipeline):
    """Fixture explicite monkeypatchant load_model() pour injecter mock_pipeline."""
    monkeypatch.setattr("src.models.predict.load_model", lambda *args, **kwargs: mock_pipeline)
    return mock_pipeline


@pytest.fixture(autouse=True)
def fallback_mock_model_in_ci(monkeypatch, mock_pipeline):
    """
    Fixture globale autouse : si le modèle .pkl n'est pas présent sur le disque
    (typiquement dans un environnement de CI où les artefacts sont exclus par gitignore),
    load_model est automatiquement détourné vers mock_pipeline pour éviter FileNotFoundError.
    """
    model_path = PROJECT_ROOT / config.model.artifact_path
    if not model_path.exists():
        monkeypatch.setattr("src.models.predict.load_model", lambda *args, **kwargs: mock_pipeline)
