import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir)))
from utils import ENV_CODE, TRACKING_SERVER_ARN, USERNAME, ENV_CODE


MODEL_NAME = f"credit-card-fraud-detection-{USERNAME}"
MODEL_VERSION = "latest"
TRACKING_SERVER_ARN = TRACKING_SERVER_ARN
USERNAME = USERNAME
ENV_CODE = ENV_CODE
FUNCTION_NAME = f"mlops-utec-{USERNAME}-online-prediction-faas"
LOG_TABLE = "mlops-utec-table-fraud-faas-log-{USERNAME}"

# Setting environment variables
# os.environ["MODEL_NAME"] = MODEL_NAME
# os.environ["MODEL_VERSION"] = MODEL_VERSION
# os.environ["TRACKING_SERVER_ARN"] = TRACKING_SERVER_ARN
# os.environ["LOG_TABLE"] = LOG_TABLE

with open(os.environ["GITHUB_ENV"], "a") as f:
    f.write(f"MODEL_NAME={MODEL_NAME}\n")
    f.write(f"MODEL_VERSION={MODEL_NAME}\n")
    f.write(f"TRACKING_SERVER_ARN={MODEL_NAME}\n")
    f.write(f"LOG_TABLE={MODEL_NAME}\n")
