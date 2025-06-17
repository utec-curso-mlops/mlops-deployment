import mlflow
import json
from faas_utils import TRACKING_SERVER_ARN, MODEL_NAME, MODEL_VERSION

# Load model
model_uri = f"models:/{MODEL_NAME}/{MODEL_VERSION}"

# Set tracking server
mlflow.set_tracking_uri(TRACKING_SERVER_ARN)
model = mlflow.xgboost.load_model(model_uri)


def lambda_handler(event, context):
    if not isinstance(event, dict):
        event = eval(event)
    data = [event['body']['data']]
    pred = model.predict_proba(data)[:, 1][0]

    return {
        'statusCode': 200,
        'body': json.dumps({'prediction': float(pred)})
    }