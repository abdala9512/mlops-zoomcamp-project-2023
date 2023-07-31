import mlflow
from prefect import flow, get_run_logger, task
from prefect.task_runners import SequentialTaskRunner
from churnlib import CHURN_MLFLOW_MODEL_NAME, ChurnModel
import pandas as pd
import datetime



@task
def ingest_data():
    """Ingest data from a source"""
    logger = get_run_logger()
    logger.info("Ingesting data...")
    prod_data = pd.read_csv(PRODUCTION_DATA_PATH)
    inference_data = prod_data.drop(["customer_id", "country", "gender"], axis=1)
    
    return inference_data, prod_data

@task
def get_production_model():
    """Get the production model"""
    logger = get_run_logger()
    logger.info("Getting production model...")

    prod_model = mlflow.xgboost.load_model(model_uri=f"models:/{CHURN_MLFLOW_MODEL_NAME}/Production",)
    return prod_model

@task
def score_model(model: mlflow.xgboost, data: pd.DataFrame):
    """Score the model"""
    logger = get_run_logger()
    logger.info("Scoring model...")
    predictions = model.predict_proba(data)[:, 1]
    return predictions

@task
def write_predictions(predictions: pd.DataFrame):
    """Write the scored model to a database"""
    logger = get_run_logger()
    logger.info("Writing to database...")
    predictions.to_parquet(PREDICTIONS_DATA_PATH)
    return None

@task
def calculate_monitoring_metrics():
    """Calculate monitoring metrics"""
    logger = get_run_logger()
    logger.info("Calculating monitoring metrics...")
    return None


@flow(task_runner=SequentialTaskRunner())
def score_churn():
    """Score the model"""
    logger = get_run_logger()
    logger.info("Scoring model...")
    inference_data, prod_data = ingest_data()
    model = get_production_model()
    predictions = score_model(model, inference_data)
    prod_data["prediction"] = predictions
    write_predictions(prod_data)
    calculate_monitoring_metrics()

    return None


if __name__ == "__main__":
    score_churn()