from unittest.mock import patch

from cognito_utils import get_user_info

FAKE_USER_POOL_ID = "us-east-1_fake12345"
COGNITO_USER_ID = "c7a7a405-e3d3-4a2f-a1d2-7a1b3e4f5a6b"

@patch('cognito_utils.COGNITO_USER_POOL_ID', FAKE_USER_POOL_ID)
@patch('cognito_utils.cognito_client')
def test_get_user_info_with_full_details(mock_cognito_client):
    mock_cognito_client.admin_get_user.return_value = {
        "UserAttributes": [
            {"Name": "email", "Value": "jane.doe@example.com"},
            {"Name": "name", "Value": "Jane Doe"},
            {"Name": "given_name", "Value": "Jane"},
        ]
    }

    user_info = get_user_info(COGNITO_USER_ID)

    mock_cognito_client.admin_get_user.assert_called_once_with(
        UserPoolId=FAKE_USER_POOL_ID,
        Username=COGNITO_USER_ID
    )
    assert user_info == {
        "email": "jane.doe@example.com",
        "name": "Jane Doe"
    }

@patch('cognito_utils.COGNITO_USER_POOL_ID', FAKE_USER_POOL_ID)
@patch('cognito_utils.cognito_client')
def test_get_user_info_fallback_to_given_name(mock_cognito_client):
    mock_cognito_client.admin_get_user.return_value = {
        "UserAttributes": [
            {"Name": "email", "Value": "john.doe@example.com"},
            {"Name": "given_name", "Value": "John"},
        ]
    }

    user_info = get_user_info(COGNITO_USER_ID)

    assert user_info == {
        "email": "john.doe@example.com",
        "name": "John"
    }

@patch('cognito_utils.COGNITO_USER_POOL_ID', FAKE_USER_POOL_ID)
@patch('cognito_utils.cognito_client')
def test_get_user_info_fallback_to_email(mock_cognito_client):
    mock_cognito_client.admin_get_user.return_value = {
        "UserAttributes": [
            {"Name": "email", "Value": "user@example.com"},
            {"Name": "email_verified", "Value": "true"},
        ]
    }

    user_info = get_user_info(COGNITO_USER_ID)

    assert user_info == {
        "email": "user@example.com",
        "name": "user@example.com"
    }

@patch('cognito_utils.COGNITO_USER_POOL_ID', FAKE_USER_POOL_ID)
@patch('cognito_utils.cognito_client')
def test_get_user_info_with_missing_attributes(mock_cognito_client):
    mock_cognito_client.admin_get_user.return_value = {
        "UserAttributes": [
            {"Name": "sub", "Value": "some-uuid"},
        ]
    }

    user_info = get_user_info(COGNITO_USER_ID)

    assert user_info == {
        "email": None,
        "name": None
    }