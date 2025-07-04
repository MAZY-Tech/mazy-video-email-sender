import json
from config import logger
from s3_utils import generate_presigned_url
from cognito_utils import get_user_info
from email_sender import send_notification_email

def lambda_handler(event, context):
    for record in event.get("Records", []):
        message_id = record.get("messageId")
        logger.info(f"Processing message ID: {message_id}")
        try:
            body = json.loads(record["body"])
            cognito_user_id = body["cognito_user_id"]
            user_info = get_user_info(cognito_user_id)
            recipient_email = user_info["email"]
            recipient_name = user_info["name"]
            status = body["status"].upper()
            download_url = None
            error_message = None

            if status == "COMPLETED":
                bucket_name = body["bucket"]
                key = body["key"]
                download_url = generate_presigned_url(bucket_name, key)
            elif status == "FAILED":
                error_message = body.get("message")

            send_notification_email(recipient_email, recipient_name, status, download_url, error_message)
            logger.info("Notification sent successfully")
        except Exception as e:
            logger.error(f"Error processing message {message_id}: {e}")
            raise
    return {"statusCode": 200, "body": json.dumps("Processing complete.")}
