import sys
import os
import boto3
from botocore.exceptions import ClientError
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir)))
from utils import ENV_CODE, TRACKING_SERVER_ARN, USERNAME, ENV_CODE


MODEL_NAME = f"credit-card-fraud-detection-{USERNAME}"
MODEL_VERSION = "latest"
TRACKING_SERVER_ARN = TRACKING_SERVER_ARN
USERNAME = USERNAME
ENV_CODE = ENV_CODE
FUNCTION_NAME = f"mlops-utec-{USERNAME}-online-prediction-faas"
LOG_TABLE = f"mlops-utec-table-fraud-faas-log-{USERNAME}"

# Setting environment variables
with open(os.environ["GITHUB_ENV"], "a") as f:
    f.write(f"MODEL_NAME={MODEL_NAME}\n")
    f.write(f"MODEL_VERSION={MODEL_VERSION}\n")
    f.write(f"TRACKING_SERVER_ARN={TRACKING_SERVER_ARN}\n")
    f.write(f"LOG_TABLE={LOG_TABLE}\n")

# Creating Logging table
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

try:
    table = dynamodb.create_table(
        TableName=LOG_TABLE,
        KeySchema=[
            {
                'AttributeName': 'cod_month',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'transaction_id',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'cod_month',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'transaction_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    table.meta.client.get_waiter('table_exists').wait(TableName=LOG_TABLE)

except ClientError as e:
    if e.response['Error']['Code'] == 'ResourceInUseException':
        print(f"ResourceInUseException caught: {e.response['Error']['Message']}")
    else:
        print(f"An unexpected ClientError occurred: {e}")