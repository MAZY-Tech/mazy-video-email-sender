import pytest
import json
from unittest.mock import MagicMock

from src.lambda_function import lambda_handler
from src.config import FRONTEND_VIDEO_URL


FAKE_COGNITO_USER_ID = "fake_cognito_id"
FAKE_USER_INFO = {"email": "test@example.com", "name": "Test User"}
FAKE_VIDEO_ID = "video_01"
FAKE_FILE_NAME = "meu_video_show.mp4"

def create_sqs_event(status, error_message=None):
    body = {
        "video_id": FAKE_VIDEO_ID,
        "file_name": FAKE_FILE_NAME,
        "cognito_user_id": FAKE_COGNITO_USER_ID,
        "status": status,
    }
    if error_message:
        body["message"] = error_message

    return {
        "Records": [
            {
                "messageId": "fake_message_id_001",
                "body": json.dumps(body)
            }
        ]
    }

def test_lambda_handler_success(mocker):
    mock_collection = MagicMock()
    mocker.patch("src.history.get_collection", return_value=mock_collection)
    mock_get_user = mocker.patch("src.lambda_function.get_user_info", return_value=FAKE_USER_INFO)
    mock_send_email = mocker.patch("src.lambda_function.send_notification_email")
    mock_logger_info = mocker.patch("src.lambda_function.logger.info")

    success_event = create_sqs_event("SUCCESS")
    response = lambda_handler(success_event, None)

    assert response["statusCode"] == 200
    mock_collection.insert_one.assert_called_once()
    mock_get_user.assert_called_once_with(FAKE_COGNITO_USER_ID)
    mock_send_email.assert_called_once_with(
        "test@example.com", 
        "Test User",
        FAKE_FILE_NAME,
        "SUCCESS",
        f"{FRONTEND_VIDEO_URL}/{FAKE_VIDEO_ID}", 
        None
    )

    assert mock_logger_info.call_count == 3

