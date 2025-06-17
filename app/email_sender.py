# app/email_sender.py
import os
import smtplib
import boto3
import tempfile
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import jinja2

load_dotenv()
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM")

template_loader = jinja2.FileSystemLoader(searchpath="./app/templates")
template_env = jinja2.Environment(loader=template_loader)

s3_client = boto3.client('s3', region_name=os.getenv("AWS_REGION"))

def get_user_by_id(user_id: str):
    # get email from backend via http here
    return 'blablabla@gmail.com'

def download_zip_from_s3(bucket: str, key: str) -> str:
    temp_dir = tempfile.gettempdir()
    local_path = os.path.join(temp_dir, Path(key).name)
    print(f"Baixando s3://{bucket}/{key} para {local_path}...")
    s3_client.download_file(bucket, key, local_path)
    print("Download concluído.")
    return local_path

def send_email_with_attachment(user_id: str, local_zip_path: str):
    print(f"Preparando e-mail...")

    template = template_env.get_template("base.html")
    html_body = template.render()
    recipient_email = get_user_by_id(user_id)

    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = recipient_email
    msg['Subject'] = "Seu arquivo ZIP está pronto!"
    msg.attach(MIMEText(html_body, 'html'))
    with open(local_zip_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {Path(local_zip_path).name}",
    )
    msg.attach(part)
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            print(f"E-mail para {recipient_email} enviado com sucesso!")
    except Exception as e:
        print(f"Falha ao enviar e-mail: {e}")
        raise 