from pathlib import Path
from typing import Any

import joblib
import pandas as pd
import sklearn.compose._column_transformer
from pydantic import BaseModel, Field

# Backward-compatibility patch for pickles serialized with scikit-learn <= 1.6
if not hasattr(sklearn.compose._column_transformer, "_RemainderColsList"):

    class _RemainderColsList(list):
        pass

    sklearn.compose._column_transformer._RemainderColsList = _RemainderColsList

from src.config import PROJECT_ROOT, config
from src.features.preprocessor import CleanInputTransformer
from src.utils.logger import get_logger

logger = get_logger("Predictor")


class CarFeaturesInput(BaseModel):
    year: int = Field(..., ge=1970, le=2030, description="Année de mise en circulation")
    marke: str = Field(..., description="Marque du véhicule")
    model: str = Field(..., description="Modèle du véhicule")
    type_boit: str = Field(..., description="Type de boîte de vitesses")
    type_carburant: str = Field(..., description="Type de carburant")
    puissance: str | float | int = Field(..., description="Puissance fiscale en CV")
    kilometrage: str | float | int = Field(..., description="Kilométrage parcouru")
    premiere_main: str = Field(..., description="Première main (Oui / Non)")
    Nombre_doors: str | float | int = Field(..., description="Nombre de portes")
    city: str = Field(..., description="Ville de localisation")


def load_model(model_path: Path | str | None = None) -> Any:
    """Charge l'artéfact du modèle depuis le disque ou lève FileNotFoundError."""
    path = PROJECT_ROOT / (model_path or config.model.artifact_path)
    if not path.exists():
        raise FileNotFoundError(f"Model file not found at: {path}")
    logger.info(f"Loading model from {path}")
    return joblib.load(path)


class CarPricePredictor:
    """Production predictor wrapper for car price regression."""

    def __init__(self, model_path: Path | str | None = None, model: Any = None):
        self.cleaner = CleanInputTransformer()
        if model is not None:
            self.model = model
            self.path = Path(model_path) if model_path else Path("in-memory-model")
        else:
            self.path = PROJECT_ROOT / (model_path or config.model.artifact_path)
            self.model = load_model(self.path)

    def predict(self, raw_input: dict[str, Any]) -> float:
        """Validate input, clean features, and output predicted price in MAD."""
        validated = CarFeaturesInput(**raw_input)
        df_raw = pd.DataFrame([validated.model_dump()])

        # If the loaded model does not contain our cleaner step, apply cleaner explicitly
        steps = getattr(self.model, "named_steps", {})
        if "cleaner" not in steps:
            df_processed = self.cleaner.transform(df_raw)
        else:
            df_processed = df_raw

        pred = self.model.predict(df_processed)[0]
        # Prices cannot be negative
        return max(0.0, float(pred))


def predict_price(raw_input: dict[str, Any], model: Any = None) -> float:
    """Fonction helper pour prédire le prix d'un véhicule à partir d'un dictionnaire."""
    predictor = CarPricePredictor(model=model) if model is not None else CarPricePredictor()
    return predictor.predict(raw_input)
