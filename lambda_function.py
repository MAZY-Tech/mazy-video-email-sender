# lambda_function.py
import json
import os
import traceback
from app import email_sender


def lambda_handler(event, context):

    for record in event['Records']:
        message_id = record['messageId']
        receipt_handle = record['receiptHandle'] # O handle para deletar a msg (gerenciado pela AWS)
        
        print(f"Processando mensagem com ID: {message_id} direto do SQS")
        
        local_zip_path = None
        try:
            body = json.loads(record['body'])
            
            #baixa o zip para anexar
            recipient_email = body['recipient_email']#remover por body['id'] para testes quando rota de get_user for implementada
            recipient_name = body['recipient_name']#remover por body['id'] para testes quando rota de get_user for implementada
            s3_bucket = body['s3_bucket']
            s3_key = body['s3_key']
            local_zip_path = email_sender.download_zip_from_s3(s3_bucket, s3_key)

            email_sender.send_email_with_attachment(recipient_email, recipient_name, local_zip_path)
            print(f"Mensagem enviada com sucesso.")

        except Exception as e:
            print(f"ERRO ao processar a mensagem {message_id}.")
            traceback.print_exc() 
            raise e
        
        finally:
            if local_zip_path and os.path.exists(local_zip_path):
                os.remove(local_zip_path)

    return {
        'statusCode': 200,
        'body': json.dumps('Processamento concluído.')
    }