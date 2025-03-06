#!/bin/sh

# Inicia o Waha normalmente em background
/usr/bin/dumb-init -- node /app/build/index.js &

echo "Aguardando Waha iniciar..."
while ! curl -s http://waha:3000/api/sessions/default/status > /dev/null; do
  sleep 2
done

echo "Waha iniciado! Iniciando sessão..."
curl -X POST http://waha:3000/api/sessions/default/start

echo "Aguardando a sessão iniciar..."
sleep 5

echo "Registrando webhook..."
curl -X POST http://waha:3000/api/sessions/default/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "url": "http://api:5000/chatbot/webhook/",
    "events": ["message"]
  }'

echo "Webhook registrado com sucesso!"

# Mantém o processo rodando
wait
