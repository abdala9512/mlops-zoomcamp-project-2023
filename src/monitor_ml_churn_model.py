from evidently.report import Report
from evidently import ColumnMapping
from evidently.metrics import (
    ColumnDriftMetric,
    DatasetDriftMetric,
    DatasetMissingValuesMetric,
)
import psycopg
from prefect import flow, get_run_logger, task
import pandas as pd
import datetime
import time

SEND_TIMEOUT = 10
create_table_statement = """
DROP TABLE IF EXISTS CHURN_ML_METRICS;
create table CHURN_ML_METRICS(
	timestamp timestamp,
	prediction_drift float,
	num_drifted_columns integer,
	share_missing_values float
);
"""
TRAINING_DATA_PATH = "../data/Bank Customer Churn Prediction.csv"
PREDICTIONS_DATA_PATH = "../data/predictions.parquet"

reference_data = pd.read_csv(TRAINING_DATA_PATH)
raw_data = pd.read_parquet(PREDICTIONS_DATA_PATH).rename(columns={"prediction": "churn"})

report = Report(
    metrics=[
        ColumnDriftMetric(column_name="churn"),
        DatasetDriftMetric(),
        DatasetMissingValuesMetric(),
    ]
)

column_mapping = ColumnMapping(
    prediction='churn',
    numerical_features=raw_data.drop(columns=['churn', 'customer_id', 'country', 'gender']).columns.to_list(),
    categorical_features=[],
    target=None
)



@task
def prep_db():
    logger = get_run_logger()
    logger.info("Preparing database...")

    with psycopg.connect(
        "host=localhost port=5432 user=postgres password=example", autocommit=True
    ) as conn:
        res = conn.execute("SELECT 1 FROM pg_database WHERE datname='ml_metrics_db'")
        if len(res.fetchall()) == 0:
            conn.execute("create database ml_metrics_db;")
        with psycopg.connect(
            "host=localhost port=5432 dbname=ml_metrics_db user=postgres password=example"
        ) as conn:
            conn.execute(create_table_statement)

@task
def calculate_metrics_postgresql(curr, i):


	report.run(reference_data = reference_data, current_data = raw_data,
		column_mapping=column_mapping)

	result = report.as_dict()

	prediction_drift = result['metrics'][0]['result']['drift_score']
	num_drifted_columns = result['metrics'][1]['result']['number_of_drifted_columns']
	share_missing_values = result['metrics'][2]['result']['current']['share_of_missing_values']

	curr.execute(
		"insert into CHURN_ML_METRICS(timestamp, prediction_drift, num_drifted_columns, share_missing_values) values (%s, %s, %s, %s)",
		(datetime.datetime.now(), prediction_drift, num_drifted_columns, share_missing_values)
	)

@flow
def batch_monitoring_backfill():
    logger = get_run_logger()
    prep_db()
    last_send = datetime.datetime.now() - datetime.timedelta(seconds=10)
    with psycopg.connect("host=localhost port=5432 dbname=ml_metrics_db user=postgres password=example", autocommit=True) as conn:
        for i in range(0, 27):
            with conn.cursor() as curr:
                calculate_metrics_postgresql(curr, i)

            new_send = datetime.datetime.now()
            seconds_elapsed = (new_send - last_send).total_seconds()
            if seconds_elapsed < SEND_TIMEOUT:
                time.sleep(SEND_TIMEOUT - seconds_elapsed)
            while last_send < new_send:
                last_send = last_send + datetime.timedelta(seconds=10)
            logger.info("Sending metrics to database...")

if __name__ == '__main__':
	batch_monitoring_backfill()