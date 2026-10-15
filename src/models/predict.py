from pathlib import Path
from typing import Any, Dict
import joblib
import pandas as pd
from pydantic import BaseModel, Field
import sklearn.compose._column_transformer

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

class CarPricePredictor:
    """Production predictor wrapper for car price regression."""

    def __init__(self, model_path: Path | str = None):
        self.path = PROJECT_ROOT / (model_path or config.model.artifact_path)
        if not self.path.exists():
            raise FileNotFoundError(f"Model file not found at: {self.path}")
        logger.info(f"Loading model from {self.path}")
        self.model = joblib.load(self.path)
        self.cleaner = CleanInputTransformer()

    def predict(self, raw_input: Dict[str, Any]) -> float:
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
