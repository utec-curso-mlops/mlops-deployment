import sagemaker

from ..utils import DEFAULT_BUCKET, ENV_CODE, TRACKING_SERVER_ARN, USERNAME, ENV_CODE

# Sagemaker configuration
ROLE = sagemaker.get_execution_role()
default_prefix = f"sagemaker/credit-card-fraud-detection/{USERNAME}"
DEFAULT_PATH = DEFAULT_BUCKET + "/" + default_prefix
sagemaker_session = sagemaker.Session(default_bucket=DEFAULT_BUCKET,
                                      default_bucket_prefix=default_prefix)
#Pipeline configuration
PIPELINE_NAME = f"pipeline-train-{ENV_CODE}-{USERNAME}"
MODEL_NAME = f"credit-card-fraud-detection-{USERNAME}"
TRACKING_SERVER_ARN = TRACKING_SERVER_ARN
USERNAME = USERNAME
ENV_CODE = ENV_CODE