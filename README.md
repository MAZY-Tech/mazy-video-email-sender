# Mazy-video-tools-notification

Microsserviço de worker serverless para envio de e-mails com anexos do S3, acionado por eventos do SQS.

## Sumário

1. [Sobre o Projeto](#sobre-o-projeto)
2. [Arquitetura da Solução](#arquitetura-da-solução)
3. [Tecnologias Utilizadas](#tecnologias-utilizadas)
4. [Pré-requisitos](#pré-requisitos)
5. [Como Executar e Testar Localmente](#como-executar-e-testar-localmente)
6. [Empacotamento e Deploy](#empacotamento-e-deploy)
7. [Configuração da Lambda](#configuração-da-lambda)

## Sobre o Projeto

O **Mazy-video-tools-notification** é um microsserviço serverless desenvolvido em **Python**, seguindo um padrão de arquitetura **orientada a eventos**. A função é projetada para operar de forma assíncrona, consumindo mensagens de uma fila AWS SQS.

Este projeto tem como objetivo oferecer uma solução robusta e escalável para o envio de e-mails de notificações, que contenham os zips com os videos extraidos pelo **mazy-video-tools-extractor**

## Arquitetura da Solução

A solução foi desenhada para ser altamente escalável e resiliente, aproveitando os serviços gerenciados da AWS.

1. **Gatilho (Trigger):** Um serviço publica uma mensagem em uma fila **AWS SQS**. A mensagem contém metadados em formato JSON, como o id da transação (video_id) e a localização (`bucket` e `key`) do arquivo no S3.
2. **Invocação:** O serviço SQS invoca automaticamente a função **AWS Lambda**, passando a mensagem da fila como um evento de entrada.
3. **Processamento:** A função Lambda executa a seguinte lógica:
   * Analisa a mensagem do SQS para extrair os dados.
   * Usa o SDK da AWS (`boto3`) para se conectar ao **Amazon S3** e baixar o arquivo ZIP extraido do video especificado para o diretório temp do ambiente de execução.
   * Cria e envia um e-mail via **SMTP**, anexando o arquivo ZIP e pegando o seu formato de um template previamente montado.
4. **Pós-processamento:**
   * Se a execução for bem-sucedida, o SQS remove a mensagem da fila.
   * Em caso de falha, a mensagem permanece na fila para uma nova tentativa 

## Tecnologias Utilizadas

* **Python**: Linguagem de programação principal da função.
* **Boto3**: SDK da AWS para Python, utilizado para interagir com S3 e SQS.
* **Jinja2**: Biblioteca para criação de templates HTML dinâmicos.
* **AWS Lambda**: Serviço de computação serverless que executa o código.
* **AWS SQS**: Serviço de fila de mensagens que desacopla os componentes e aciona a Lambda.
* **AWS S3**: Serviço de armazenamento de objetos para hospedar os arquivos a serem anexados.

## Pré-requisitos

Antes de começar, certifique-se de ter as seguintes ferramentas instaladas e configuradas em seu ambiente:

* **Python 3.9+**: E o gerenciador de pacotes **Pip**.
* **Git**: Para clonar o repositório.
* **AWS CLI**: Configurado com credenciais de acesso à sua conta AWS.

## Como Executar e Testar Localmente

Siga os passos abaixo para configurar e testar o projeto em seu ambiente local antes do deploy:

1. **Clonar o repositório**
   ```
   git clone git@github.com:MAZY-Tech/mazy-video-tools-notification.git
   cd mazy-video-tools-notification/
   ```

2. **Configurar o ambiente virtual e instalar dependências**
   ```
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configurar variáveis de ambiente para teste**
   * Copie o arquivo `.env.local.example` para `.env.local`.
   * Preencha o arquivo `.env.local` com suas credenciais de SMTP e dados de um bucket S3 de teste.

4. **Executar o script de teste local**
   * Certifique-se de que o arquivo ZIP de teste exista no S3.
   * Ajuste os dados no `mock_sqs_event` dentro do arquivo `local_testing.py`.
   * Execute o teste:
     ```
     python local_testing.py
     ```
   * O script simulará a invocação da Lambda e exibirá os logs no terminal.

## Empacotamento e Deploy

Para fazer o deploy na AWS, o código e suas dependências precisam ser compactados em um arquivo `.zip`.

1. **Criar o diretório do pacote e instalar dependências**
   ```
   mkdir package
   pip install -r requirements.txt --target ./package
   ```

2. **Copiar o código da aplicação**
   ```
   cp -r app/ ./package/
   cp lambda_function.py ./package/
   ```

3. **Gerar o arquivo .zip**
   A compactação deve ser feita a partir do conteúdo do diretório `package`.
   ```
   cd package
   zip -r ../deployment-package.zip .
   cd ..
   ```
   O arquivo `deployment-package.zip` está pronto para ser enviado à AWS Lambda.

## Configuração da Lambda

| Item de Configuração | Valor | 
| ----- | ----- | 
| **Runtime** | Python 3.9 (ou superior) | 
| **Handler** | `lambda_function.lambda_handler` | 
| **Timeout** | 30 segundos (recomendado) | 
| **Gatilho (Trigger)** | SQS (apontando para a fila de origem) | 
| **IAM Role** | Deve conter permissões para `s3:GetObject`, `sqs:*` e `logs:*` | 

### Variáveis de Ambiente

As seguintes variáveis devem ser configuradas diretamente no ambiente da Lambda:

| Variável | Descrição | Exemplo | 
| ----- | ----- | ----- | 
| `AWS_REGION` | Região da AWS onde os serviços estão localizados. | `us-east-1` | 
| `SMTP_SERVER` | Endereço do servidor SMTP para envio de e-mail. | `smtp.gmail.com` | 
| `SMTP_PORT` | Porta do servidor SMTP (geralmente 587 para TLS). | `587` | 
| `SMTP_USER` | Nome de usuário para autenticação no servidor SMTP. | `seu_email@example.com` | 
| `SMTP_PASSWORD` | Senha para autenticação. **Use AWS Secrets Manager em produção.** | `sua_senha_de_app` | 
| `EMAIL_FROM` | Endereço de e-mail que aparecerá como remetente. | `Seu Serviço <no-reply@example.com>` |
        