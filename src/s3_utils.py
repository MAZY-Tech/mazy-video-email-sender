from config import SIGNED_URL_EXPIRATION
from aws_clients import s3_client

def generate_presigned_url(bucket_name: str, key: str, expiration: int = None) -> str:
    expiration = expiration or SIGNED_URL_EXPIRATION
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": key},
        ExpiresIn=expiration,
    )
