from batch_training_utils import TRACKING_SERVER_ARN, DEFAULT_PATH
from sagemaker.workflow.function_step import step



# Global variables
instance_type = "ml.m5.large"

# Step definition
@step(
    name="DataPull",
    instance_type=instance_type,
    dependencies="./data_pull_requirements.txt"
)
def data_pull(experiment_name: str, run_name: str,
              cod_month_start: int, cod_month_end: int) -> tuple[str, str, str]:
    import awswrangler as wr
    import mlflow

    mlflow.set_tracking_uri(TRACKING_SERVER_ARN)
    mlflow.set_experiment(experiment_name)
    TARGET_COL = "is_fraud"
    query = """
        SELECT  transaction_id
                ,amount
                ,merchant_category
                ,merchant_country
                ,card_present
                ,is_fraud
                ,cod_month
                ,trx_vel_last_1mths
                ,trx_vel_last_2mths
                ,amt_vel_last_1mths
                ,amt_vel_last_2mths
        FROM    RISK_MANAGEMENT.CREDIT_CARD_TRANSACTIONS
        WHERE   cod_month between {} and {}
    """.format(cod_month_start, cod_month_end)
    train_s3_path = f"s3://{DEFAULT_PATH}/train_data/train.csv"
    with mlflow.start_run(run_name=run_name) as run:
        run_id = run.info.run_id
        with mlflow.start_run(run_name="DataPull", nested=True):
            df = wr.athena.read_sql_query(sql=query, database="risk_management")
            df.to_csv(train_s3_path, index=False)
            mlflow.log_input(
                mlflow.data.from_pandas(df, train_s3_path,
                                        targets=TARGET_COL),
                context="DataPull"
            )
    return train_s3_path, experiment_name, run_id


