
import asyncio
from fastapi import FastAPI
from .sqs_consumer import poll_sqs_queue

app = FastAPI(
    title="Serviço Consumidor de E-mails SQS",
    description="Este serviço ouve uma fila SQS e envia e-mails com os zips de imagens extraidas armazenados em nosso S3.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    print("Aplicação iniciada.")
    asyncio.create_task(poll_sqs_queue())

@app.get("/health", tags=["Monitoring"])
async def health_check():
    return {"status": "ok"}