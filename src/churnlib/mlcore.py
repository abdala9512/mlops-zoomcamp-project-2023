"""This module contains the classes to train the model.
Example:
    $ python training/mlcore.py

Todo:
    * Add more models.
    * Add more metrics.

"""

from typing import Any, Dict, List
import xgboost
import pandas as pd
from sklearn.model_selection import train_test_split
from abc import ABC, abstractmethod
from hyperopt import hp
import numpy as np


XGB_MAX_DEPTH = 25
xgb_space = {
    "objective": hp.choice("objective", ["binary:logistic"]),
    "max_depth": hp.choice("max_depth", np.arange(1, XGB_MAX_DEPTH, dtype=int)),
    "min_child_weight": hp.uniform("min_child_weight", 0, 5),
    "learning_rate": hp.loguniform("learning_rate", np.log(0.005), np.log(0.2)),
    "gamma": hp.uniform("gamma", 0, 5),
    "colsample_bytree": hp.quniform("colsample_bytree", 0.1, 1, 0.01),
    "colsample_bynode": hp.quniform("colsample_bynode", 0.1, 1, 0.01),
    "colsample_bylevel": hp.quniform("colsample_bylevel", 0.1, 1, 0.01),
    "subsample": hp.quniform("subsample", 0.5, 1, 0.05),
    "reg_alpha": hp.uniform("reg_alpha", 0, 5),
    "reg_lambda": hp.uniform("reg_lambda", 0, 5),
}


class BaseChurnModel(ABC):
    """BaseChurnModel.

    This class is the base class for the churn model.

    Attributes:
        model (Any): A estimator or pipeline to fit.
        seed (int): The seed to use.
        split_data (Dict[str, pd.DataFrame]): A dictionary with the split data.
        target_col (str): The target column to predict.


    """

    def __init__(
        self,
        data: pd.DataFrame,
        target_col: str,
        seed: int = 100,
        exclude_cols: List[str] | str = [],
        prediction_dataset: bool = False
    ) -> None:
        """__init__ method.

        Args:
            estimator (str): A estimator to fit.
            target_col (str): The target column to predict.
            seed (int): The seed to use.

        """
        self.seed = seed
        self.data = data
        self.target_col = target_col
        if prediction_dataset:
            self.modeling_data = self.data.drop(exclude_cols, axis=1)
        if exclude_cols:
            self.excluded_data = self.data[exclude_cols]
        self.split_data = self._split_data_randomly()
        

    def _split_data_randomly(
        self,
    ) -> None:
        """_split_data method.

        This method splits the data into train and test sets.

        Args:
            data (pd.DataFrame): A dataframe with the data to fit.

        """
        x_values = self.data.drop(
            list(self.excluded_data.columns) + [self.target_col], axis=1
        )
        y_values = self.data[self.target_col]
        x_train, x_test, y_train, y_test = train_test_split(
            x_values, y_values, test_size=0.2, random_state=self.seed
        )
        return {
            "x_train": x_train,
            "x_test": x_test,
            "y_train": y_train,
            "y_test": y_test,
        }

    def split_time_based(self, date_column: str, split_dates: Dict) -> Dict:
        pass

    @abstractmethod
    def generate_estimator(self) -> Any:
        ...

    @abstractmethod
    def train(self, data: pd.DataFrame) -> Any:
        """train method.

        This method trains the model.

        Args:
            data (pd.DataFrame): A dataframe with the data to fit.

        Returns:
            Any: A fitted model.

        """
        ...


class ChurnModel(BaseChurnModel):
    """ChurnModel.



    Attributes:
        model (Any): A estimator or pipeline to fit.
        seed (int): The seed to use.
        split_data (Dict[str, pd.DataFrame]): A dictionary with the split data.
        target_col (str): The target column to predict.


    """

    def __init__(
        self,
        data: pd.DataFrame,
        target_col: str,
        params: Dict,
        seed=100,
        exclude_cols: List[str] = [],
    ) -> None:
        """__init__ method.

        Args:
            estimator (str): A estimator to fit.
            target_col (str): The target column to predict.
            seed (int): The seed to use.

        """
        super().__init__(
            data=data, target_col=target_col, seed=seed, exclude_cols=exclude_cols
        )
        self.model = self.generate_estimator(params=params)

    def generate_estimator(self, params: Dict) -> xgboost.XGBModel:
        """generate_estimator method.

        This method generates a XGBoost estimator.

        Args:
            params (Dict): A dictionary with the parameters.

        Returns:
            xgboost.XGBModel: A XGBoost estimator.

        """

        return xgboost.XGBClassifier(**params)

    def train(self) -> xgboost.XGBModel:
        """train method.

        This method trains the model.

        Args:
            data (pd.DataFrame): A dataframe with the data to fit.

        Returns:
            xgboost.XGBModel: A fitted model.

        """
        return self.model.fit(self.split_data["x_train"], self.split_data["y_train"])


def create_xgboost_churn_model(
    data: pd.DataFrame,
    params: Dict,
    target_col: str,
    exclude_cols: List[str] | str = [],
) -> BaseChurnModel:
    """create_xgboost_churn_model method.

    This method creates a XGBoost model.

    Args:
        data (pd.DataFrame): A dataframe with the data to fit.
        params (Dict): A dictionary with the parameters.
        target_col (str): The target column to predict.
        exclude_cols (List[str]): A list of columns to exclude.

    Returns:
        BaseChurnModel: A XGBoost model.

    """
    model = ChurnModel(
        data=data,
        target_col=target_col,
        seed=100,
        params=params,
        exclude_cols=exclude_cols,
    )

    return model
