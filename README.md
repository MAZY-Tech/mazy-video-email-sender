# MAZY Video Tools Notification

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=MAZY-Tech_mazy-video-tools-notification&metric=coverage)](https://sonarcloud.io/summary/new_code?id=MAZY-Tech_mazy-video-tools-notification)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=MAZY-Tech_mazy-video-tools-notification&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=MAZY-Tech_mazy-video-tools-notification)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=MAZY-Tech_mazy-video-tools-notification&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=MAZY-Tech_mazy-video-tools-notification)

Função **AWS Lambda** para envio de notificações por e-mail com link de resultado da extração das imagens, acionada por eventos do SQS.

## Sumário

1. [Sobre o Projeto](#sobre-o-projeto)  
2. [Arquitetura da Solução](#arquitetura-da-solução)  
3. [Tecnologias Utilizadas](#tecnologias-utilizadas)  
4. [Pré-requisitos](#pré-requisitos)  
5. [Como Executar e Testar Localmente](#como-executar-e-testar-localmente)  
6. [Empacotamento e Deploy (SAM)](#empacotamento-e-deploy-sam)  
7. [Configuração da Lambda](#configuração-da-lambda)  

## Sobre o Projeto

O **mazy-video-tools-notification** é um microsserviço serverless em **Python 3.12** que consome mensagens de uma fila **AWS SQS** (`mazy-video-tools-notification`), consulta o usuário no **Amazon Cognito**, gera um **Presigned URL** para download do vídeo processado (quando `status == "COMPLETED"`) ou envia uma mensagem de erro (quando `status == "FAILED"`), e notifica o usuário por e-mail usando **SMTP**.

## Arquitetura da Solução

1. **Trigger**: Mensagens em JSON chegam na fila SQS `mazy-video-tools-notification`.  
2. **Lambda Invocation**: SQS invoca automaticamente a função Lambda.  
3. **Get User Info**: A função usa o `cognito_user_id` para chamar **AdminGetUser** no Cognito e obter `email` e `name`.  
4. **Presigned URL**: Se `status == "COMPLETED"`, gera um link assinado com o S3 para o objeto no bucket.  
5. **E-mail Notification**: Envia e-mail via SMTP com o template Jinja2 (`base.html`), passando as variáveis:
   - `name`  
   - `status`  
   - `video_url` (se COMPLETED)  
   - `error_message` (se FAILED)  
6. **Retentativa & Logging**: Em caso de falha, a mensagem permanece na fila para nova tentativa. Logs via CloudWatch.

## Tecnologias Utilizadas

- **Python 3.12**  
- **Boto3** (S3, SQS, Cognito)  
- **Jinja2** (HTML templating)  
- **AWS Lambda**  
- **AWS SQS**  
- **AWS S3**  
- **AWS Cognito**  
- **AWS SAM**
- **Sentry**
- **Sonar**

## Pré-requisitos

- **Python 3.12** e **pip**  
- **AWS CLI** configurado  
- **SAM CLI** (opcional, para deploy)  
- Permissões AWS para criar/atualizar Lambda, SQS, IAM roles e políticas.

## Como Executar e Testar Localmente

1. Clone o repositório e entre na pasta:  
   ```bash
   git clone git@github.com:MAZY-Tech/mazy-video-tools-notification.git
   cd mazy-video-tools-notification
   ```

2. Crie e ative um virtualenv, instale dependências:  
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Configure variáveis de ambiente (crie `.env` a partir de `.env.example`):  
   ```
   cp .env.example .env
   ```

4. Simule um evento com SAM CLI:
   ```bash
   sam local invoke  NotificationFunction --event example.json
   ```

## Teste Unitários

1. Com os pacotes já instalados localmente, execute:
   ```
   pytest -v
   ```
## Empacotamento e Deploy (SAM)

1. **Build**:  
   ```bash
   sam build
   ```
2. **Deploy**:  
   ```bash
   sam deploy --guided
   ```

O template SAM está em `template.yaml` e inclui:

- **SQS Queue**: `mazy-video-tools-notification`  
- **Lambda Function**: Python 3.12, handler `lambda_function.lambda_handler`, role `arn:aws:iam::${AWS::AccountId}:role/LabRole`  
- **IAM Policies**:  
  - `AWSLambdaBasicExecutionRole`  
  - Permissões SQS (Receive, Delete)  
  - Permissão `s3:GetObject` para o bucket de vídeos  
  - Permissão `cognito-idp:AdminGetUser` para o user pool  

## Configuração da Lambda

No console AWS ou via SAM, defina as variáveis de ambiente:

| Variável                | Descrição                                                                 |
|------------------------|---------------------------------------------------------------------------|
| `DATABASE_HOST`        | Endpoint do banco de dados.                                               |
| `DATABASE_USER`        | Nome de usuário para o banco de dados.                                   |
| `DATABASE_PASSWORD`    | Senha para o banco de dados.                                              |
| `DATABASE_NAME`        | Nome do banco de dados (database/schema).                                 |
| `SMTP_SERVER`          | Endpoint do servidor SMTP para envio de e-mails.                          |
| `SMTP_PORT`            | Porta do servidor SMTP (ex: 587 para TLS).                                |
| `SMTP_USER`            | Nome de usuário para autenticação no servidor SMTP.                       |
| `SMTP_PASSWORD`        | Senha para o servidor SMTP (em produção, use um Secrets Manager).         |
| `EMAIL_FROM`           | Endereço de e-mail que aparecerá como remetente ("From").                 |
| `COGNITO_USER_POOL_ID` | O ID do User Pool do AWS Cognito.                                         |
| `FRONTEND_VIDEO_URL`   | URL base do frontend para montar o link do vídeo no e-mail.               |
| `SENTRY_DSN`           | DSN (Data Source Name) do projeto no Sentry para monitoramento de erros.  |
| `TEMPLATE_DIR`         | (Opcional) Caminho para o diretório de templates Jinja2.                  |

---

## Participantes

- **Alison Israel - RM358367**  
  *Discord*: @taykarus | E-mail: taykarus@gmail.com

- **José Matheus de Oliveira - RM358854**  
  *Discord*: @jsmatheus | E-mail: matheusoliveira.info@gmail.com

- **Victor Zaniquelli - RM358533**  
  *Discord*: @zaniquelli | E-mail: zaniquelli@outlook.com.br

- **Yan Gianini - RM358368**  
  *Discord*: @.gianini | E-mail: yangianini@gmail.com
