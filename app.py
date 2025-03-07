from flask import Flask, request, jsonify
from bot.ia_bot import AIBot
from services.waha import Waha

app = Flask(__name__)

# Instancia o Waha
waha = Waha()

# Inicia e configura a sessão antes de rodar o Flask
print("Iniciando e configurando a sessão do Waha...")
waha.start_session()

@app.route('/chatbot/webhook/', methods=['POST'])
def webhook():
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Request must contain JSON'}), 400
    
    data = request.json
    
    try:
        chat_id = data['payload']['from']
        received_message = data['payload']['body']
    except KeyError as e:
        return jsonify({'status': 'error', 'message': f'Missing key in payload: {str(e)}'}), 400
    except TypeError:
        return jsonify({'status': 'error', 'message': 'Invalid payload structure'}), 400

    is_group = '@g.us' in chat_id

    if is_group:
        return jsonify({'status': 'success', 'message': 'Mensagem de grupo ignorada.'}), 200

    ai_bot = AIBot()
    
    waha.start_typing(chat_id=chat_id)
    history_messages = waha.get_history_messages(
        chat_id=chat_id,
        limit=5,
    )
    response_message = ai_bot.invoke(
        history_messages=history_messages,
        question=received_message,
    )
    waha.send_message(
        chat_id=chat_id,
        message=response_message,
    )
    waha.stop_typing(chat_id=chat_id)

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)