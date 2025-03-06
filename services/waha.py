import requests

class Waha:
    def __init__(self):
        self.__api_url = 'http://waha:3000'
        self.session_name = "default"

    def check_session(self, session_name="default"):
        """ Verifica se a sessão existe e retorna o status """
        url = f'{self.__api_url}/api/sessions/{session_name}'
        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()  # Retorna o status da sessão
            return None  # Sessão não existe
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {str(e)}")
            return None

    def start_session(self):
        """ Cria ou reinicia a sessão (para se necessário e cria uma nova) """
        session_name = "default"
        session_data = self.check_session(session_name)

        if session_data:
            session_status = session_data.get("status", "")
            print(f"📌 Sessão '{session_name}' encontrada. Status: {session_status}")

            if session_status == "CONNECTED":
                print(f"⚠️ Sessão '{session_name}' já está ativa. Parando e criando nova sessão...")
                self.stop_session(session_name)  # Para a sessão existente
                return self.create_session()  # Cria uma nova sessão
            elif session_status == "STOPPED":
                print(f"🔄 Sessão '{session_name}' está parada. Iniciando...")
                return self.start_existing_session(session_name)
            else:
                print(f"⚠️ Sessão '{session_name}' está em estado desconhecido: {session_status}")
                return session_data
        else:
            print(f"🆕 Criando nova sessão '{session_name}'...")
            return self.create_session()

    def stop_session(self, session_name="default"):
        """Para uma sessão existente"""
        url = f'{self.__api_url}/api/sessions/{session_name}/stop'
        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(url, headers=headers)
            if response.status_code == 200:
                print(f"✅ Sessão '{session_name}' parada com sucesso!")
            else:
                print(f"❌ Erro ao parar sessão: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao parar a sessão: {str(e)}")

    def create_session(self):
        """ Cria uma nova sessão """
        headers = {'Content-Type': 'application/json'}
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
        
        url = f'{self.__api_url}/api/sessions'

        try:
            response = requests.post(url, json=sessao, headers=headers)
            if response.status_code in [200, 201]:
                print("✅ Sessão criada com sucesso!")
                return response.json()
            else:
                print(f"❌ Erro ao criar sessão: {response.status_code} - {response.text}")
                return {"error": response.text, "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {str(e)}")
            return {"error": str(e)}

    def start_existing_session(self, session_name="default"):
        """ Inicia uma sessão existente apenas se necessário """
        url = f'{self.__api_url}/api/sessions/{session_name}/start'
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(url, headers=headers)
            if response.status_code in [200, 201]:
                print(f"✅ Sessão '{session_name}' iniciada com sucesso!")
                return response.json()
            elif response.status_code == 422:  # Sessão já iniciada
                print(f"⚠️ Sessão '{session_name}' já está ativa.")
                return {"message": "Session already running"}
            else:
                print(f"❌ Erro ao iniciar sessão: {response.status_code} - {response.text}")
                return {"error": response.text, "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {str(e)}")
            return {"error": str(e)}

    def send_message(self, chat_id, message):
        """Envia mensagem para um chat"""
        url = f"{self.__api_url}/api/sendText"
        headers = {'Content-Type': 'application/json'}
        payload = {'session': self.session_name, 'chatId': chat_id, 'text': message}

        try:
            response = requests.post(url=url, json=payload, headers=headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao enviar mensagem: {str(e)}")
            return {"error": str(e)}

    def get_history_messages(self, chat_id, limit=50):
        """Obtém histórico de mensagens de um chat"""
        url = f"{self.__api_url}/api/{self.session_name}/chats/{chat_id}/messages?limit={limit}&downloadMedia=false"
        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.get(url=url, headers=headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao obter histórico: {str(e)}")
            return {"error": str(e)}

    def start_typing(self, chat_id):
        """Simula que o bot está digitando"""
        url = f"{self.__api_url}/api/startTyping"
        headers = {'Content-Type': 'application/json'}
        payload = {'session': self.session_name, 'chatId': chat_id}

        try:
            requests.post(url=url, json=payload, headers=headers)
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao simular digitação: {str(e)}")

    def stop_typing(self, chat_id):
        """Para a simulação de digitação"""
        url = f"{self.__api_url}/api/stopTyping"
        headers = {'Content-Type': 'application/json'}
        payload = {'session': self.session_name, 'chatId': chat_id}

        try:
            requests.post(url=url, json=payload, headers=headers)
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao parar digitação: {str(e)}")
