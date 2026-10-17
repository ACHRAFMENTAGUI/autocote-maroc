import joblib
import mlflow
import numpy as np
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline

from src.config import PROJECT_ROOT, config
from src.data.loader import load_clean_data, split_data
from src.features.preprocessor import CleanInputTransformer, build_feature_pipeline
from src.utils.logger import get_logger

logger = get_logger("ModelTraining")


def run_training():
    logger.info("Initializing MLflow experiment...")
    mlflow.set_tracking_uri(config.mlflow.tracking_uri)
    mlflow.set_experiment(config.mlflow.experiment_name)

    df = load_clean_data()
    X_train, X_test, y_train, y_test = split_data(df)

    with mlflow.start_run(run_name="lightgbm_baseline"):
        logger.info(f"Logging parameters: {config.model.params}")
        mlflow.log_params(config.model.params)

        pipeline = Pipeline(
            [
                ("cleaner", CleanInputTransformer()),
                ("preprocessor", build_feature_pipeline()),
                ("regressor", LGBMRegressor(**config.model.params)),
            ]
        )

        logger.info("Training LightGBM pipeline...")
        pipeline.fit(X_train, y_train)

        logger.info("Evaluating on test set...")
        y_pred = pipeline.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)

        metrics = {"mae": float(mae), "rmse": float(rmse), "r2_score": float(r2)}
        mlflow.log_metrics(metrics)
        logger.info(f"Results: R2={r2:.4f} | MAE={mae:,.2f} MAD | RMSE={rmse:,.2f} MAD")

        # Save model artifact
        output_path = PROJECT_ROOT / config.model.artifact_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(pipeline, output_path)
        logger.info(f"Saved trained model to {output_path}")

        mlflow.log_artifact(str(output_path))
        logger.info("Model artifact successfully logged to MLflow.")


if __name__ == "__main__":
    run_training()
