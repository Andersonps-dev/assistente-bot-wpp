#!/bin/sh
if ! command -v dumb-init &> /dev/null
then
    echo "dumb-init não encontrado, instalando..."
    apt-get update && apt-get install -y dumb-init
fi

/usr/bin/dumb-init -- node /app/build/index.js &

sleep 10

curl -X POST http://waha:3000/api/sessions/default/start

sleep 5

curl -X POST http://localhost:3000/api/sessions/default/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "url": "http://api:5000/chatbot/webhook/",
    "events": ["message"]
  }'

wait
