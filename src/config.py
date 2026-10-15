from pathlib import Path
from typing import Any, Dict, List
import yaml
from pydantic import BaseModel

PROJECT_ROOT = Path(__file__).resolve().parent.parent

class DataConfig(BaseModel):
    raw_path: str
    processed_path: str
    target_column: str
    test_size: float
    val_size: float
    random_state: int

class FeaturesConfig(BaseModel):
    numeric: List[str]
    categorical: List[str]

class ModelConfig(BaseModel):
    name: str
    params: Dict[str, Any]
    artifact_path: str

class MLflowConfig(BaseModel):
    experiment_name: str
    tracking_uri: str

class AppConfig(BaseModel):
    data: DataConfig
    features: FeaturesConfig
    model: ModelConfig
    mlflow: MLflowConfig

def load_config(config_path: str = "config/config.yaml") -> AppConfig:
    full_path = PROJECT_ROOT / config_path
    if not full_path.exists():
        raise FileNotFoundError(f"Configuration file not found at: {full_path}")
    with open(full_path, "r", encoding="utf-8") as f:
        config_dict = yaml.safe_load(f)
    return AppConfig(**config_dict)

config = load_config()
