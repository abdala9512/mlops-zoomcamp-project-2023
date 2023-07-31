import mlflow
from prefect import flow, get_run_logger
from prefect.task_runners import SequentialTaskRunner
from evidently.report import Report
from evidently import ColumnMapping
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric
import psycopg

create_table_statement = """
drop table if exists dummy_metrics;
create table dummy_metrics(
	timestamp timestamp,
	prediction_drift float,
	num_drifted_columns integer,
	share_missing_values float
)
"""

@task
def prep_db():
	with psycopg.connect("host=localhost port=5432 user=postgres password=example", autocommit=True) as conn:
		res = conn.execute("SELECT 1 FROM pg_database WHERE datname='test'")
		if len(res.fetchall()) == 0:
			conn.execute("create database test;")
		with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example") as conn:
			conn.execute(create_table_statement)


def ingest_data():
    """Ingest data from a source"""
    logger = get_run_logger()
    logger.info("Ingesting data...")
    return None

def get_production_model():
    """Get the production model"""
    logger = get_run_logger()
    logger.info("Getting production model...")
    return None

def score_model():
    """Score the model"""
    logger = get_run_logger()
    logger.info("Scoring model...")
    return None

def write_predictions():
    """Write the scored model to a database"""
    logger = get_run_logger()
    logger.info("Writing to database...")
    return None


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
    return None


if __name__ == "__main__":
    score_churn()