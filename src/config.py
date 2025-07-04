import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM")

TEMPLATE_DIR = os.getenv("TEMPLATE_DIR", "./templates")
SIGNED_URL_EXPIRATION = int(os.getenv("SIGNED_URL_EXPIRATION", 3600))

COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
