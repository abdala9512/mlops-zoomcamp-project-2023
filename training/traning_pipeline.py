import mlflow
from prefect import flow, get_run_logger, task
from xgboost import XGBClassifier
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials

from prefect.task_runners import SequentialTaskRunner


@task
def ingest_data():
    """Ingest data from a source"""
    logger = get_run_logger()
    logger.info("Ingesting data...")
    return None

@task
def optimize_hyperparameters():
    """Optimize hyperparameters for a model"""
    logger = get_run_logger()
    logger.info("Optimizing hyperparameters...")
    return None

@flow(task_runner=SequentialTaskRunner())
def churn_model_training():
    """Train a model with the given parameters"""
    logger = get_run_logger()
    logger.info("Training model...")
    churn_db = ingest_data()
    best_hyperparameters = optimize_hyperparameters()
    return None

if __name__ == "__main__":
    churn_model_training()