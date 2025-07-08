import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

DATABASE_HOST = os.environ['DATABASE_HOST']
DATABASE_USER = os.environ['DATABASE_USER']
DATABASE_PASSWORD = os.environ['DATABASE_PASSWORD']
DATABASE_NAME = os.environ['DATABASE_NAME']

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM")

TEMPLATE_DIR = os.getenv("TEMPLATE_DIR", "./templates")

COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")

FRONTEND_VIDEO_URL = os.getenv("FRONTEND_VIDEO_URL")

SENTRY_DSN = os.getenv("SENTRY_DSN")
