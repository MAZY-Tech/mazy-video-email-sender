import json
from dotenv import load_dotenv

from src.lambda_function import lambda_handler

print("--- Iniciando teste local da função Lambda ---")
load_dotenv(dotenv_path='.env.local')
print("Variáveis de ambiente carregadas.")

# evento mock
mock_sqs_event = {
    "Records": [
        {
            "messageId": "19dd0b57-b21e-4ac1-bd88-01bbb068cb78",
            "receiptHandle": "MessageReceiptHandle",
            "body": json.dumps({
                "video_id": "298ce197-3627-4845-83d7-cd6c98a9df8c",
                "cognito_user_id": "a4681438-70b1-70cb-308f-cc40ea50066a",
                "status": "COMPLETED",
                "message": "",
                "timestamp": "2025-06-19T19:46:37+00:00"
            }),
            "attributes": {
                "ApproximateReceiveCount": "1",
                "SentTimestamp": "1523232000000",
                "SenderId": "123456789012",
                "ApproximateFirstReceiveTimestamp": "1523232000001"
            },
            "messageAttributes": {},
            "md5OfBody": "7b270e59b47ff90a553787216d55d91d",
            "eventSource": "aws:sqs",
            "eventSourceARN": "arn:aws:sqs:us-east-1:123456789012:MyQueue",
            "awsRegion": "us-east-1"
        }
    ]
}

print("\nEvento SQS simulado:")
print(json.dumps(mock_sqs_event, indent=2))

try:
    print("\n--- Executando lambda_handler ---")
    result = lambda_handler(mock_sqs_event, None)
    print("\n--- Execução concluída com sucesso ---")
    print("Resultado retornado:", result)
except Exception as e:
    print(f"\n--- A execução da Lambda falhou com uma exceção: {e} ---")