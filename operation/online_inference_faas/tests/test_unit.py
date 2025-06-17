import pytest
import mlflow
import mlflow.xgboost
from faas_utils import TRACKING_SERVER_ARN

mlflow.set_tracking_uri(TRACKING_SERVER_ARN)

model_name = "credit-card-fraud-detection"
model_version = "latest"
model_uri = f"models:/{model_name}/{model_version}"

def model_exists(model_uri):
    """Checks if the model exists in the MLflow Model Registry."""
    try:
        mlflow.xgboost.load_model(model_uri)
        return True
    except mlflow.exceptions.MlflowException:
        return False

@pytest.mark.parametrize("model_uri", [
    "models:/credit-card-fraud-detection/latest",  # Registered model with version 1
    "models:/churn-detection/1" # A model that doesn't exist
])
def test_model_registry(model_uri):
    """Test if model exists in MLflow registry."""
    assert model_exists(model_uri), f"Model '{model_uri}' does not exist!"

