# from sagemaker.workflow.function_step import step
# from sagemaker.workflow.pipeline import Pipeline
# import sagemaker
# from sagemaker.workflow.parameters import ParameterInteger
# import utils


# user = utils.get_username()
# pipeline_name = f"pipeline-basico-{user}"
# role = sagemaker.get_execution_role()
# instance_type = "ml.m5.large"
# periodo = ParameterInteger(name="PeriodoCarga", default_value=202503)


# @step(
#     name="DataPull",
#     instance_type=instance_type,
# )
# def data_pull(data_source: str, periodo: int) -> tuple[str, str]:
#     print(f"Data pull from {data_source}")
#     print(f"Periodo:{periodo}")
#     return "s3://train_path", "s3://test_path"

# @step(
#     name="ModelTraining",
#     instance_type=instance_type,
# )
# def model_training(train_path: str, test_path: str, periodo: int) -> str:
#     print(f"Train set: {train_path} and test set:{test_path}")
#     print(f"Periodo:{periodo}")
#     return "model_path"

# data_pull_step = data_pull("s3:mybucket/data", periodo)
# model_training_step = model_training(data_pull_step[0],
#                                      data_pull_step[1], periodo)



# pipeline = Pipeline(name=pipeline_name, steps=[data_pull_step, model_training_step],parameters=[periodo])
# pipeline.upsert(role_arn=role)


# import sagemaker
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir)))
# from utils import DEFAULT_BUCKET, ENV_CODE, TRACKING_SERVER_ARN, USERNAME, ENV_CODE

# # Sagemaker configuration
# SAGEMAKER_ROLE = "arn:aws:iam::654654589924:role/service-role/SageMaker-MLOpsEngineer"
# default_prefix = f"sagemaker/credit-card-fraud-detection/{USERNAME}"
# DEFAULT_PATH = DEFAULT_BUCKET + "/" + default_prefix
# sagemaker_session = sagemaker.Session(default_bucket=DEFAULT_BUCKET,
#                                       default_bucket_prefix=default_prefix)
# #Pipeline configuration
# PIPELINE_NAME = f"pipeline-train-{ENV_CODE}-{USERNAME}"
# MODEL_NAME = f"credit-card-fraud-detection-{USERNAME}"
# TRACKING_SERVER_ARN = TRACKING_SERVER_ARN
# USERNAME = USERNAME
# ENV_CODE = ENV_CODE