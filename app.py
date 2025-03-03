from flask import Flask, request, jsonify
from bot.ia_bot import AIBot
from services.waha import Waha

app = Flask(__name__)

@app.route('/chatbot/webhook/', methods=['POST'])
def webhook():
    data = request.json

    if 'payload' not in data:
        return jsonify({'status': 'error', 'message': 'Missing payload in request'}), 400

    payload = data['payload']

    if 'from' not in payload or 'body' not in payload:
        return jsonify({'status': 'error', 'message': 'Missing required fields in payload'}), 400

    chat_id = payload['from']
    received_message = payload['body']
    is_group = '@g.us' in chat_id
    is_status = 'status@broadcast' in chat_id

    if is_group or is_status:
        return jsonify({'status': 'success', 'message': 'Mensagem de grupo/status ignorada.'}), 200

    waha = Waha()
    ai_bot = AIBot()

    waha.start_typing(chat_id=chat_id)
    response = ai_bot.invoke(question=received_message)
    waha.send_message(
        chat_id=chat_id,
        message=response,
    )
    waha.stop_typing(chat_id=chat_id)

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)