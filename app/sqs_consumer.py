# app/sqs_consumer.py
import os
import json
import asyncio
import boto3
from dotenv import load_dotenv

from . import email_sender

load_dotenv()
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")
AWS_REGION = os.getenv("AWS_REGION")

# Cria um cliente SQS
sqs_client = boto3.client("sqs", region_name=AWS_REGION)

def create_history_object(user_id: str, local_zip_path: str):
    return None

async def poll_sqs_queue():
    print("Iniciando o consumidor SQS...")
    while True:
        try:
            print("Verificando mensagens na fila SQS...")
            response = sqs_client.receive_message(
                QueueUrl=SQS_QUEUE_URL,
                MaxNumberOfMessages=5,
                WaitTimeSeconds=20,
                MessageAttributeNames=['All']
            )

            messages = response.get("Messages", [])
            if not messages:
                print("Nenhuma mensagem nova. Aguardando...")
                continue

            for message in messages:
                receipt_handle = message['ReceiptHandle']
                print(f"Mensagem recebida: {message['MessageId']}")
                
                local_zip_path = None
                try:
                    body = json.loads(message['Body'])
                    user_id = body['user_id']
                    s3_bucket = body['s3_bucket']
                    s3_key = body['s3_key']
                    local_zip_path = email_sender.download_zip_from_s3(s3_bucket, s3_key)
                    
                    email_sender.send_email_with_attachment(user_id, local_zip_path)
                    create_history_object(user_id, local_zip_path)
                    print(f"Processamento concluído. Deletando mensagem {message['MessageId']} da fila.")
                    sqs_client.delete_message(
                        QueueUrl=SQS_QUEUE_URL,
                        ReceiptHandle=receipt_handle
                    )
                except Exception as e:
                    print(f"ERRO ao processar mensagem {message['MessageId']}: {e}")
                finally:
                    if local_zip_path and os.path.exists(local_zip_path):
                        os.remove(local_zip_path)
                        print(f"Arquivo temporário {local_zip_path} removido.")

        except Exception as e:
            print(f"ERRO no loop principal do consumidor: {e}")
            await asyncio.sleep(10)