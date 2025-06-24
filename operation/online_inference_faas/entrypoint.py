import mlflow
import json
import os
import pandas as pd
from decimal import Decimal
import boto3

# Load model
model_name = os.getenv("MODEL_NAME")
model_version = os.getenv("MODEL_VERSION")
model_uri = f"models:/{model_name}/{model_version}"

# Set tracking server
tracking_server_arn = os.getenv("TRACKING_SERVER_ARN")
print(tracking_server_arn)
logging_table = os.getenv("LOG_TABLE")

# Set tracking server
mlflow.set_tracking_uri(tracking_server_arn)
model = mlflow.xgboost.load_model(model_uri)
FEATURES = ['card_present', 'trx_vel_last_1mths', 'trx_vel_last_2mths',
                'amt_vel_last_1mths', 'amt_vel_last_2mths']

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def lambda_handler(event, context):
    if not isinstance(event, dict):
        event = eval(event)
    df = pd.DataFrame([event['body']['data']])
    pred = model.predict_proba(df[FEATURES])[:, 1][0]
    # Logging prediction
    table = dynamodb.Table(logging_table)

    response = table.put_item(
        Item= {
            "transaction_id" : event['body']['data']["transacion_id"],
            "cod_month": event['body']['data']["cod_month"],
            "card_present": event['body']['data']["card_present"],
            "trx_vel_last_1mths": event['body']['data']["trx_vel_last_1mths"],
            "trx_vel_last_2mths": event['body']['data']["trx_vel_last_2mths"],
            "amt_vel_last_1mths": Decimal(str(event['body']['data']["amt_vel_last_1mths"])),
            "amt_vel_last_2mths": Decimal(str(event['body']['data']["amt_vel_last_2mths"]))
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'prediction': float(pred)})
    }


