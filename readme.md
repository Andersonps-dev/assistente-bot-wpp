# Guia de Instalação e Configuração do Projeto

## Pré-requisitos
Antes de iniciar, certifique-se de ter os seguintes requisitos instalados na sua máquina:

- **Docker**: Para instalar, siga as instruções oficiais: [Docker Install](https://docs.docker.com/get-docker/)
- **Docker Compose**: Para instalar, siga as instruções oficiais: [Docker Compose Install](https://docs.docker.com/compose/install/)
- **Python**: Para instalar, siga as instruções oficiais: [Python Install](https://www.python.org/downloads/)
- **WhastApp Business**
- **Groq**: Para criar API do LLaMA: [Create API Groq](https://console.groq.com/playground)

## Passo a passo para configuração

1. **Criar o arquivo `.env`**
   
   Crie um arquivo chamado `.env` na raiz do projeto e adicione a seguinte variável:
   
   ```env
   GROQ_API_KEY= 'Sua chave api'
   ```

2. **Ativar o WAHA**
   
   Execute o seguinte comando no terminal para rodar o WAHA no Docker:
   
   ```sh
   docker run -it -p 3000:3000/tcp devlikeapro/waha
   ```

3. **Construir os containers com Docker Compose**
   
   Execute os comandos abaixo para construir e iniciar os serviços do projeto:
   
   ```sh
   docker-compose up --build api
   docker-compose up --build waha
   ```

4. **Acessar o dashboard**
   
   Abra o navegador e acesse:
   
   ```
   http://localhost:3000/dashboard/
   ```
   Vai até a parte Sessions
   Linha do default -> Configuração -> Url: http://api:5000/chatbot/webhook/ -> Events: somente menssage -> update


5. **Conectar o WhatsApp Business**
   
   No terminal, um QR Code será exibido. Use o WhatsApp Business para escanear e conectar ao serviço.

---
6. **Iniciar banco de dados no container**
   docker exec -it wpp_bot_api /bin/bash

   # Dentro do container
   python /app/rag/rag.py