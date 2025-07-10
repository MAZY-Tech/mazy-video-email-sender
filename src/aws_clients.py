import boto3
from config import AWS_REGION

cognito_client = boto3.client("cognito-idp", region_name=AWS_REGION)
