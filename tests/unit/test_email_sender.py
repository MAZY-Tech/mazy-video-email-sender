import pytest
from unittest.mock import patch, MagicMock
from email_sender import send_notification_email

@pytest.fixture
def email_data():
    return {
        "recipient_email": "user@example.com",
        "recipient_name": "User",
        "file_name": "video.mp4",
        "status": "COMPLETED",
        "video_url": "http://example.com/video",
        "error_message": None,
    }

@patch("email_sender.smtplib.SMTP")
@patch("email_sender.jinja2.Environment")
def test_send_email_success(mock_jinja_env, mock_smtp, email_data):
    mock_template = MagicMock()
    mock_template.render.return_value = "<html>Email Body</html>"
    mock_env = MagicMock()
    mock_env.get_template.return_value = mock_template
    mock_jinja_env.return_value = mock_env

    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    send_notification_email(**email_data)

    mock_env.get_template.assert_called_once_with("base.html")
    mock_template.render.assert_called_once_with(
        name=email_data["recipient_name"],
        file_name=email_data["file_name"],
        status=email_data["status"],
        video_url=email_data["video_url"],
        error_message=email_data["error_message"]
    )

    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once()
    mock_server.send_message.assert_called_once()

@patch("email_sender.smtplib.SMTP", side_effect=Exception("SMTP error"))
@patch("email_sender.jinja2.Environment")
def test_send_email_failure(mock_jinja_env, mock_smtp, email_data):
    mock_template = MagicMock()
    mock_template.render.return_value = "<html>Email Body</html>"
    mock_env = MagicMock()
    mock_env.get_template.return_value = mock_template
    mock_jinja_env.return_value = mock_env

    with pytest.raises(Exception, match="SMTP error"):
        send_notification_email(**email_data)
