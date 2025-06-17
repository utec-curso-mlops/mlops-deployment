import boto3
import json
#from ..faas_utils import FUNCTION_NAME
FUNCTION_NAME = "mlops-utec-rickpuma-online-prediction-faas"

def test_lambda_invocation():
    client = boto3.client('lambda')
    payload = {"body": {"data": [0,237.10,487.97,504.7,7878.1]}}
    response = client.invoke(FunctionName=FUNCTION_NAME,Payload=json.dumps(payload),LogType='Tail')
    response_payload = json.loads(response['Payload'].read().decode('utf-8'))
    assert abs(eval(response_payload["body"])["prediction"] - 0.0007983) < 0.000001

