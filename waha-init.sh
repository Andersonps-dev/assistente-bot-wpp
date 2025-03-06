#!/bin/sh

# Inicia o Waha normalmente
/usr/bin/dumb-init -- node /app/build/index.js &

# Aguarda alguns segundos para o servidor iniciar
sleep 10

# Inicia a sessão automaticamente
curl -X POST http://localhost:3000/api/sessions/default/start

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
