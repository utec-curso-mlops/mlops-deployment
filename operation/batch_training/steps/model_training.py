from batch_training_utils import TRACKING_SERVER_ARN, DEFAULT_PATH
from sagemaker.workflow.function_step import step

# Global variables
instance_type = "ml.m5.large"

# Step definition
@step(
    name="ModelTraining",
    instance_type=instance_type,
    image_uri="arn:aws:sagemaker:us-east-1:885854791233:image/sagemaker-base-python-v4",
    dependencies="./model_training_requirements.txt"
)
def train(train_s3_path: str, experiment_name: str,
                   run_id: str) -> tuple[str, str, str, str]:
    import pandas as pd
    import mlflow
    from sklearn.model_selection import train_test_split
    from xgboost import XGBClassifier
    TARGET_COL = "is_fraud"
    SEED = 42
    TRAIN_SPLIT = 0.7
    FEATURES = ['card_present', 'trx_vel_last_1mths', 'trx_vel_last_2mths',
                'amt_vel_last_1mths', 'amt_vel_last_2mths']
    mlflow.set_tracking_uri(TRACKING_SERVER_ARN)
    mlflow.set_experiment(experiment_name)
    df = pd.read_csv(train_s3_path)
    X = df[FEATURES]
    y = df[TARGET_COL]
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        train_size=TRAIN_SPLIT,
                                                        random_state=SEED)
    use_gpu = False
    param = dict(
        objective="binary:logistic",
        max_depth=5,
        eta=0.2,
        gamma=4,
        min_child_weight=6,
        subsample=0.7,
        tree_method="gpu_hist" if use_gpu else "hist",
        n_estimators=50
    )
    with mlflow.start_run(run_id=run_id):
        with mlflow.start_run(run_name="ModelTraining",
                              nested=True) as training_run:
            training_run_id = training_run.info.run_id
            test_s3_path = f"s3://{DEFAULT_PATH}/test_data/test.csv"
            df_test = pd.concat([X_test, y_test], axis=1)
            df_test.to_csv(test_s3_path, index=False)
            mlflow.log_input(
                mlflow.data.from_pandas(df_test, test_s3_path,
                                        targets=TARGET_COL),
                context="ModelTraining"
            )
            mlflow.xgboost.autolog(
                log_input_examples=True,
                log_model_signatures=True,
                log_models=True,
                log_datasets=True,
                model_format="xgb",
            )
            xgb = XGBClassifier(**param)
            xgb.fit(X_train, y_train)
    return test_s3_path, experiment_name, run_id, training_run_id