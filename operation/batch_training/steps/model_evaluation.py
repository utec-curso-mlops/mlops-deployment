from batch_training_utils import TRACKING_SERVER_ARN
from sagemaker.workflow.function_step import step

# Global variables
instance_type = "ml.m5.large"

# Step definition
@step(
    name="ModelEvaluation",
    instance_type=instance_type,
    dependencies="./model_training_requirements.txt"
)
def evaluate(
    test_s3_path: str,
    experiment_name: str,
    run_id: str,
    training_run_id: str,
) -> dict:
    import mlflow
    import pandas as pd
    TARGET_COL = "is_fraud"
    mlflow.set_tracking_uri(TRACKING_SERVER_ARN)
    mlflow.set_experiment(experiment_name)
    with mlflow.start_run(run_id=run_id):
        with mlflow.start_run(run_name="ModelEvaluation", nested=True):
            test_df = pd.read_csv(test_s3_path)
            model = mlflow.pyfunc.load_model(f"runs:/{training_run_id}/model")
            results = mlflow.evaluate(
                model=model,
                data=test_df,
                targets=TARGET_COL,
                model_type="classifier",
                evaluators=["default"],
            )
            return {"f1_score": results.metrics["f1_score"]}