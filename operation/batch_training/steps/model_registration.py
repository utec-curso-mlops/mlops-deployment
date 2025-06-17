from batch_training_utils import TRACKING_SERVER_ARN
from sagemaker.workflow.function_step import step

# Global variables
instance_type = "ml.m5.large"

# Step definition
@step(
    name="ModelRegistration",
    instance_type=instance_type,
    image_uri="arn:aws:sagemaker:us-east-1:885854791233:image/sagemaker-base-python-v4",
    dependencies="./model_training_requirements.txt"
)
def register(
    model_name: str,
    experiment_name: str,
    run_id: str,
    training_run_id: str,
):
    import mlflow

    mlflow.set_tracking_uri(TRACKING_SERVER_ARN)
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_id=run_id):
        with mlflow.start_run(run_name="ModelRegistration", nested=True):
            mlflow.register_model(f"runs:/{training_run_id}/model", model_name)
