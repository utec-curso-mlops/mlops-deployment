import mlflow
import json
import os
import pandas as pd

# Load model
model_name = os.getenv("MODEL_NAME")
model_version = os.getenv("MODEL_VERSION")
model_uri = f"models:/{model_name}/{model_version}"

# Set tracking server
tracking_server_arn = os.getenv("TRACKING_SERVER_ARN")
print(tracking_server_arn)

# Set tracking server
mlflow.set_tracking_uri(tracking_server_arn)
model = mlflow.xgboost.load_model(model_uri)
FEATURES = ['card_present', 'trx_vel_last_1mths', 'trx_vel_last_2mths',
                'amt_vel_last_1mths', 'amt_vel_last_2mths']

def lambda_handler(event, context):
    if not isinstance(event, dict):
        event = eval(event)
    df = pd.DataFrame([event['body']['data']])
    pred = model.predict_proba(df[FEATURES])[:, 1][0]
    
    return {
        'statusCode': 200,
        'body': json.dumps({'prediction': float(pred)})
    }


