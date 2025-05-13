from flask import Flask, request, jsonify
from bot.ia_bot import AIBot
from services.evolutionAPI import EvolutionAPI

app = Flask(__name__)

evolution_api = EvolutionAPI()

print("Iniciando e configurando a sessão do Evolution API...")
evolution_api.start_session()

@app.route('/chatbot/webhook/', methods=['POST'])
def webhook():
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Request must contain JSON'}), 400
    
    data = request.json
    
    try:
        # Evolution API webhook structure: messages are in data.messages
        message_data = data['data']['messages'][0]
        chat_id = message_data['key']['remoteJid']
        received_message = message_data['message'].get('conversation', '')
        if not received_message:
            return jsonify({'status': 'success', 'message': 'Non-text message ignored.'}), 200
    except (KeyError, TypeError) as e:
        return jsonify({'status': 'error', 'message': f'Invalid payload structure: {str(e)}'}), 400

    is_group = '@g.us' in chat_id

    if is_group:
        return jsonify({'status': 'success', 'message': 'Mensagem de grupo ignorada.'}), 200

    ai_bot = AIBot()
    
    evolution_api.start_typing(chat_id=chat_id)
    history_messages = evolution_api.get_history_messages(
        chat_id=chat_id,
        limit=5,
    )
    response_message = ai_bot.invoke(
        history_messages=history_messages,
        question=received_message,
    )
    evolution_api.send_message(
        chat_id=chat_id,
        message=response_message,
    )
    evolution_api.stop_typing(chat_id=chat_id)

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)