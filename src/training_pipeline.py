import mlflow
from prefect import flow, get_run_logger, task
from hyperopt import fmin, tpe, STATUS_OK, Trials, space_eval
from prefect.task_runners import SequentialTaskRunner
import pandas as pd
from typing import Dict
import xgboost
from churnlib import create_xgboost_churn_model, xgb_space, CHURN_MLFLOW_EXPERIMENT_NAME
from sklearn.metrics import (
    roc_auc_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)


TRAINING_DATA_PATH = "../data/Bank Customer Churn Prediction.csv"
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment(CHURN_MLFLOW_EXPERIMENT_NAME)


@task
def ingest_data():
    """Ingest data from a source"""
    logger = get_run_logger()
    logger.info("Ingesting data...")
    churn_db = pd.read_csv(TRAINING_DATA_PATH)
    return churn_db


@task
def optimize_hyperparameters(data: pd.DataFrame, search_space: Dict):
    """Optimize hyperparameters for a model"""
    logger = get_run_logger()
    logger.info("Optimizing hyperparameters...")

    def xgboost_objective_function(params: Dict) -> float:

        xgb_model = create_xgboost_churn_model(
            data=data,
            params={},
            target_col="churn",
            exclude_cols=["customer_id", "country", "gender"],
        )
        train = xgboost.DMatrix(
            xgb_model.split_data["x_train"], xgb_model.split_data["y_train"]
        )
        res = xgboost.cv(
            params,
            train,
            num_boost_round=100,
            nfold=5,
            metrics={"auc"},
            seed=0,
            callbacks=[
                xgboost.callback.EvaluationMonitor(show_stdv=True),
                xgboost.callback.EarlyStopping(15),
            ],
        )
        best_loss = res["test-auc-mean"].iloc[-1]
        return {"loss": best_loss, "status": STATUS_OK}

    trials = Trials()
    best = fmin(
        fn=xgboost_objective_function,
        space=search_space,
        algo=tpe.suggest,
        max_evals=3,
        trials=trials,
    )
    return space_eval(search_space, best)

@flow(task_runner=SequentialTaskRunner())
def churn_model_training():
    """Train a model with the given parameters"""
    logger = get_run_logger()
    logger.info("Training model...")
    churn_db = ingest_data()
    best_hyperparameters = optimize_hyperparameters(data=churn_db, search_space=xgb_space)

    mlflow.xgboost.autolog()
    with mlflow.start_run():

        churn_model = create_xgboost_churn_model(
            data=churn_db,
            params={},
            target_col="churn",
            exclude_cols=["customer_id", "country", "gender"],
        )
        x_train, y_train = (
            churn_model.split_data["x_train"],
            churn_model.split_data["y_train"],
        )
        x_test, y_test = (
            churn_model.split_data["x_test"],
            churn_model.split_data["y_test"],
        )
        best_xgb = xgboost.XGBClassifier(**best_hyperparameters)
        best_xgb.fit(x_train, y_train)

        predictions = best_xgb.predict(x_test)

        accuracy_metric = accuracy_score(y_test, predictions)
        precision_metric = precision_score(y_test, predictions)
        recall_metric = recall_score(y_test, predictions)
        f1_score_metric = f1_score(y_test, predictions)

        mlflow.log_metric(
            "AUC score", roc_auc_score(y_test, best_xgb.predict_proba(x_test)[:, 1])
        )

        mlflow.end_run()

    return None


if __name__ == "__main__":
    churn_model_training()
