import re
from datetime import datetime
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.config import config

class CleanInputTransformer(BaseEstimator, TransformerMixin):
    """Transformer for cleaning and standardizing user/scraped input data."""

    def fit(self, X, y=None):
        return self

    @staticmethod
    def _clean_numeric(value):
        if pd.isna(value):
            return 0.0
        if isinstance(value, (int, float)):
            return float(value)
        cleaned = re.sub(r"[^\d.]", "", str(value))
        return float(cleaned) if cleaned else 0.0

    @staticmethod
    def _parse_kilometrage(value):
        if pd.isna(value):
            return 0.0
        val_str = str(value).replace(" ", "")
        if "-" in val_str:
            parts = [float(p) for p in val_str.split("-") if p.isdigit()]
            return sum(parts) / len(parts) if parts else 0.0
        return CleanInputTransformer._clean_numeric(val_str)

    def transform(self, X):
        df = X.copy()
        current_year = datetime.now().year

        if "kilometrage" in df.columns:
            df["kilometrage"] = df["kilometrage"].apply(self._parse_kilometrage)
        if "puissance" in df.columns:
            df["puissance"] = df["puissance"].apply(self._clean_numeric)
        if "Nombre_doors" in df.columns:
            df["Nombre_doors"] = df["Nombre_doors"].apply(self._clean_numeric)
        if "year" in df.columns:
            df["year"] = df["year"].apply(self._clean_numeric)

        for cat_col in config.features.categorical:
            if cat_col in df.columns:
                df[cat_col] = df[cat_col].fillna("Unknown").astype(str).str.strip().str.title()

        return df

def build_feature_pipeline() -> ColumnTransformer:
    """Build Scikit-learn ColumnTransformer for scaling numeric and encoding categorical features."""
    num_pipeline = Pipeline([
        ("scaler", StandardScaler())
    ])

    cat_pipeline = Pipeline([
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_pipeline, config.features.numeric),
            ("cat", cat_pipeline, config.features.categorical),
        ],
        remainder="drop"
    )
    return preprocessor
