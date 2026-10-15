from pathlib import Path
from typing import Tuple
import pandas as pd
from sklearn.model_selection import train_test_split
from src.config import PROJECT_ROOT, config
from src.utils.logger import get_logger

logger = get_logger("DataLoader")

def load_clean_data(file_path: Path | str = None) -> pd.DataFrame:
    """Load cleaned dataset from CSV file."""
    path = PROJECT_ROOT / (file_path or config.data.processed_path)
    if not path.exists():
        raise FileNotFoundError(f"Cleaned dataset not found at: {path}")
    logger.info(f"Loading data from {path}")
    df = pd.read_csv(path)
    logger.info(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns.")
    return df

def split_data(
    df: pd.DataFrame,
    target_column: str = None,
    test_size: float = None,
    random_state: int = None
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split dataset into train and test sets."""
    target = target_column or config.data.target_column
    t_size = test_size if test_size is not None else config.data.test_size
    seed = random_state if random_state is not None else config.data.random_state

    X = df.drop(columns=[target], errors="ignore")
    y = df[target]

    logger.info(f"Splitting data with test_size={t_size}, random_state={seed}")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=t_size, random_state=seed
    )
    return X_train, X_test, y_train, y_test

