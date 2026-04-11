import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import save_object, load_object
from networksecurity.utils.main_utils.utils import load_numpy_array_data, evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)

import mlflow
import dagshub
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ✅ Initialize DagsHub from environment variables
dagshub.init(
    repo_owner=os.getenv("DAGSHUB_REPO_OWNER", "theshivammishra10"),
    repo_name=os.getenv("DAGSHUB_REPO_NAME", "Network-Security-System"),
    mlflow=True
)

# ✅ Use env variable for MLflow tracking
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
if MLFLOW_TRACKING_URI:
    os.environ["MLFLOW_TRACKING_URI"] = MLFLOW_TRACKING_URI


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig,
                 data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def track_mlflow(self, model, train_metric, test_metric, model_name):
        try:
            with mlflow.start_run():

                # ✅ log metrics
                mlflow.log_metric("train_f1", train_metric.f1_score)
                mlflow.log_metric("test_f1", test_metric.f1_score)

                mlflow.log_metric("train_precision", train_metric.precision_score)
                mlflow.log_metric("test_precision", test_metric.precision_score)

                mlflow.log_metric("train_recall", train_metric.recall_score)
                mlflow.log_metric("test_recall", test_metric.recall_score)

                # ✅ log model
                mlflow.sklearn.log_model(
                    model,
                    "model",
                    registered_model_name=model_name
                )

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def train_model(self, X_train, y_train, X_test, y_test):

        models = {
            "Random Forest": RandomForestClassifier(),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(),
            "Logistic Regression": LogisticRegression(max_iter=1000),
            "AdaBoost": AdaBoostClassifier(),
        }

        params = {
            "Decision Tree": {
                'criterion': ['gini', 'entropy', 'log_loss'],
            },
            "Random Forest": {
                'n_estimators': [16, 32, 64, 128],
            },
            "Gradient Boosting": {
                'learning_rate': [0.1, 0.01],
                'n_estimators': [32, 64, 128],
            },
            "Logistic Regression": {},
            "AdaBoost": {
                'learning_rate': [0.1, 0.01],
                'n_estimators': [32, 64, 128],
            }
        }

        # ✅ Evaluate models
        model_report = evaluate_models(
            X_train=X_train,
            y_train=y_train,
            X_test=X_test,
            y_test=y_test,
            models=models,
            param=params
        )

        # ✅ Get best model
        best_model_name = max(model_report, key=model_report.get)
        best_model = models[best_model_name]

        # ✅ IMPORTANT: train model (fixes your biggest bug)
        best_model.fit(X_train, y_train)

        # ✅ Predictions
        y_train_pred = best_model.predict(X_train)
        y_test_pred = best_model.predict(X_test)

        # ✅ Metrics
        train_metric = get_classification_score(y_train, y_train_pred)
        test_metric = get_classification_score(y_test, y_test_pred)

        # ✅ MLflow logging (single run, correct)
        self.track_mlflow(best_model, train_metric, test_metric, best_model_name)

        # ✅ Load preprocessor
        preprocessor = load_object(
            file_path=self.data_transformation_artifact.transformed_object_file_path
        )

        # ✅ Save model
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path, exist_ok=True)

        network_model = NetworkModel(
            preprocessor=preprocessor,
            model=best_model
        )

        save_object(
            self.model_trainer_config.trained_model_file_path,
            obj=network_model
        )

        # Optional: separate save
        save_object("final_model/model.pkl", best_model)

        # ✅ Artifact
        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_metric_artifact=train_metric,
            test_metric_artifact=test_metric
        )

        logging.info(f"Model trainer artifact: {model_trainer_artifact}")

        return model_trainer_artifact

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            X_train, y_train = train_arr[:, :-1], train_arr[:, -1]
            X_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            return self.train_model(X_train, y_train, X_test, y_test)

        except Exception as e:
            raise NetworkSecurityException(e, sys)