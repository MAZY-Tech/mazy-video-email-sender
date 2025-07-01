import boto3

s3_client = boto3.client("s3")
cognito_client = boto3.client("cognito-idp")
