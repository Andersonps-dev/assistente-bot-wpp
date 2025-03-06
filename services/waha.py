import requests

class Waha:
    def __init__(self):
        self.__api_url = 'http://waha:3000'

    def start_session(self):
        headers = {
            'Content-Type': 'application/json',
        }
        sessao = {
            "name": "default",
            "config": {
                "webhooks": [
                    {
                        "url": "http://api:5000/chatbot/webhook/",
                        "events": ["message"]
                    }
                ]
            }
        }
        
        # Usar a rota correta para criar a sessão
        url = f'{self.__api_url}/api/sessions'

        try:
            response = requests.post(
                url=url,
                json=sessao,
                headers=headers,
            )
            # Verificar o status da resposta
            if response.status_code in [200, 201]:
                print("Sessão criada e iniciada com sucesso!")
                return response.json()
            else:
                print(f"Erro ao criar sessão: {response.status_code} - {response.text}")
                return {"error": response.text, "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {str(e)}")
            return {"error": str(e)}

    def start_existing_session(self, session_name="default"):
        # Método separado para iniciar uma sessão existente, se necessário
        url = f'{self.__api_url}/api/sessions/{session_name}/start'
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(url=url, headers=headers)
            if response.status_code in [200, 201]:
                print(f"Sessão '{session_name}' iniciada com sucesso!")
                return response.json()
            else:
                print(f"Erro ao iniciar sessão: {response.status_code} - {response.text}")
                return {"error": response.text, "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {str(e)}")
            return {"error": str(e)}

    # Outros métodos (send_message, get_history_messages, etc.) permanecem iguais

    def send_message(self, chat_id, message):
        url = f'{self.__api_url}/api/sendText'
        headers = {'Content-Type': 'application/json'}
        payload = {
            'session': 'default',
            'chatId': chat_id,
            'text': message,
        }
        requests.post(url=url, json=payload, headers=headers)

    def get_history_messages(self, chat_id, limit):
        url = f'{self.__api_url}/api/default/chats/{chat_id}/messages?limit={limit}&downloadMedia=false'
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url=url, headers=headers)
        return response.json()

    def start_typing(self, chat_id):
        url = f'{self.__api_url}/api/startTyping'
        headers = {'Content-Type': 'application/json'}
        payload = {'session': 'default', 'chatId': chat_id}
        requests.post(url=url, json=payload, headers=headers)

    def stop_typing(self, chat_id):
        url = f'{self.__api_url}/api/stopTyping'
        headers = {'Content-Type': 'application/json'}
        payload = {'session': 'default', 'chatId': chat_id}
        requests.post(url=url, json=payload, headers=headers)