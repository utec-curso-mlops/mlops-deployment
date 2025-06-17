from batch_training_utils import TRACKING_SERVER_ARN, SAGEMAKER_ROLE
from sagemaker.workflow.function_step import step

# Global variables
instance_type = "ml.m5.large"

# Step definition
@step(
    name="ModelRegistration",
    instance_type=instance_type,
    image_uri = "public.ecr.aws/sagemaker/sagemaker-distribution:3.1.0-cpu",
    #dependencies="model_training_requirements.txt",
    role=SAGEMAKER_ROLE
)
def register(
    model_name: str,
    experiment_name: str,
    run_id: str,
    training_run_id: str,
):
    import subprocess
    subprocess.run(['pip', 'install', 'mlflow==2.13.2', 'sagemaker-mlflow==0.1.0']) 
    mlflow.set_tracking_uri(TRACKING_SERVER_ARN)
    mlflow.set_experiment(experiment_name)
    import mlflow
    with mlflow.start_run(run_id=run_id):
        with mlflow.start_run(run_name="ModelRegistration", nested=True):
            mlflow.register_model(f"runs:/{training_run_id}/model", model_name)
