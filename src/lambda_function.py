import json
from config import logger, FRONTEND_VIDEO_URL
from cognito_utils import get_user_info
from email_sender import send_notification_email
from history import add_notification_history

def lambda_handler(event, context):
    for record in event.get("Records", []):
        message_id = record.get("messageId")
        logger.info(f"Processing message ID: {message_id}")
        try:
            body = json.loads(record["body"])
            video_id = body["video_id"]
            file_name = body["file_name"]

            cognito_user_id = body["cognito_user_id"]            
            user_info = get_user_info(cognito_user_id)
            recipient_email = user_info["email"]
            recipient_name = user_info["name"]

            status = body["status"].upper()
            video_url = f'{FRONTEND_VIDEO_URL}/{video_id}'
            error_message = None

            if status == "FAILED":
                error_message = body.get("message")

            send_notification_email(recipient_email, recipient_name, file_name, status, video_url, error_message)
            
            add_notification_history(
                cognito_user_id=cognito_user_id,
                recipient_email=recipient_email,
                video_id=video_id
            )
            logger.info("Notification sent successfully")
        except Exception as e:
            logger.error(f"Error processing message {message_id}: {e}")
            raise
    return {"statusCode": 200, "body": json.dumps("Processing complete.")}
