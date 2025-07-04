import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import jinja2

from config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, EMAIL_FROM, TEMPLATE_DIR, logger

def send_notification_email(recipient_email: str, recipient_name: str, status: str, download_url: str = None, error_message: str = None):
    template_loader = jinja2.FileSystemLoader(searchpath=TEMPLATE_DIR)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("base.html")
    html_body = template.render(
        name=recipient_name,
        status=status,
        download_url=download_url,
        error_message=error_message
    )

    subject = f"Your video processing {status.lower()}"
    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            logger.info(f"Email sent to {recipient_email}")
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise
