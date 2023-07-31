
from typing import List
import mlflow

def search_best_model(
        experiment_names: List[str] = [MLFLOW_FAKE_NEWS_EXPERIMENT_NAME],
        metric_name: str = "val_auc_15"
    ) -> str:
    """Search Best Run ID of given experiments
    """
    runs_  = mlflow.search_runs(experiment_names=experiment_names)
    run_id = runs_.loc[runs_[f'metrics.{metric_name}'].idxmax()]['run_id']
    artifact_path = json.loads(
        runs_[runs_["run_id"] == run_id]["tags.mlflow.log-model.history"].values[0]
    )[0]["artifact_path"]
    
    return run_id, artifact_path