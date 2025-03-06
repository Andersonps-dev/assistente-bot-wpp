#!/bin/sh

# Instala o dumb-init se não estiver presente
if ! command -v dumb-init &> /dev/null
then
    echo "dumb-init não encontrado, instalando..."
    apt-get update && apt-get install -y dumb-init
fi

# Inicia o Waha normalmente
/usr/bin/dumb-init -- node /app/build/index.js &

# Aguarda alguns segundos para o servidor iniciar
sleep 10

# Inicia a sessão automaticamente
curl -X POST http://waha:3000/api/sessions/default/start

# Aguarda mais alguns segundos para garantir que a sessão foi criada
sleep 5

# Registra o webhook automaticamente
curl -X POST http://localhost:3000/api/sessions/default/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "url": "http://api:5000/chatbot/webhook/",
    "events": ["message"]
  }'

# Mantém o processo rodando
wait
