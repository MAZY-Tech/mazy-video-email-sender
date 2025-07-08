from .aws_clients import cognito_client
from .config import COGNITO_USER_POOL_ID

def get_user_info(cognito_user_id: str) -> dict:
    response = cognito_client.admin_get_user(
        UserPoolId=COGNITO_USER_POOL_ID,
        Username=cognito_user_id
    )
    attrs = {attr["Name"]: attr["Value"] for attr in response.get("UserAttributes", [])}
    return {
        "email": attrs.get("email"),
        "name": attrs.get("name") or attrs.get("given_name") or attrs.get("email")
    }
