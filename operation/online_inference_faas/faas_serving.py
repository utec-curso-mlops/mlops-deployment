from faas_utils import TRACKING_SERVER_ARN, MODEL_NAME, MODEL_VERSION, USERNAME

!aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 654654589924.dkr.ecr.us-east-1.amazonaws.com

repository_name = f"utec-mlops/{USERNAME}/online-prediction"

!aws ecr create-repository --repository-name $repository_name

!docker build -t $repository_name .

ecr_url = "654654589924.dkr.ecr.us-east-1.amazonaws.com"
tag_name = f"{repository_name}:latest"
full_tag_name = f"{ecr_url}/{tag_name}"

!docker tag $tag_name $full_tag_name

!docker push $full_tag_name

function_name = f"mlops-utec-{USERNAME}-online-prediction"
print(function_name)
lambda_role = "arn:aws:iam::654654589924:role/utec-lambda-mlops-role"

!aws lambda create-function \
        --function-name $function_name \
        --package-type Image \
        --code ImageUri=$full_tag_name \
        --role $lambda_role \
        --architectures x86_64 \
        --region us-east-1 \
        --timeout 120

# aws lambda update-function-configuration \
#   --function-name my-function \
#   --environment "Variables={BUCKET=amzn-s3-demo-bucket,KEY=file.txt}"


{
  "body": {
    "data": [0,237.10,487.97,504.7,7878.1]
  }
}

