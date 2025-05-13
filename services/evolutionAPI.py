import requests

class EvolutionAPI:
    def __init__(self):
        self.__api_url = 'http://evolution-api:3000/api/v1'
        self.session_name = "default"
        self.api_key = 'your-api-key-here'
        
    def check_session(self, session_name="default"):
        url = f'{self.__api_url}/instance/fetchInstances?instanceName={session_name}'
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                instances = response.json().get('instances', [])
                if instances:
                    return instances[0]  # Return the first matching instance
                return None
            return None
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {str(e)}")
            return None

    def start_session(self):
        session_name = "default"
        session_data = self.check_session(session_name)

        if session_data:
            session_status = session_data.get("status", "").upper()
            print(f"📌 Instância '{session_name}' encontrada. Status: {session_status}")

            if session_status == "OPEN":
                print(f"⚠️ Instância '{session_name}' já está ativa. Desconectando e recriando...")
                self.stop_session(session_name)
                self.create_session()
            elif session_status == "CLOSED":
                print(f"🔄 Instância '{session_name}' está fechada. Conectando...")
                self.start_existing_session(session_name)
            else:
                print(f"⚠️ Instância '{session_name}' está em estado desconhecido: {session_status}")
        else:
            print(f"🆕 Criando nova instância '{session_name}'...")
            self.create_session()

        self.configure_session()

    def stop_session(self, session_name="default"):
        """Desconecta uma instância existente"""
        url = f'{self.__api_url}/instance/logout/{session_name}'
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }

        try:
            response = requests.delete(url, headers=headers)
            if response.status_code == 200:
                print(f"✅ Instância '{session_name}' desconectada com sucesso!")
            else:
                print(f"❌ Erro ao desconectar instância: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao desconectar a instância: {str(e)}")

    def create_session(self):
        """Cria uma nova instância"""
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }
        instance_data = {
            "instanceName": "default",
            "webhook": {
                "url": "http://api:5000/chatbot/webhook/",
                "enabled": True,
                "webhookByEvents": True,
                "events": ["messages.upsert"]
            }
        }

        url = f'{self.__api_url}/instance/create'

        try:
            response = requests.post(url, json=instance_data, headers=headers)
            if response.status_code in [200, 201]:
                print("✅ Instância criada com sucesso!")
                return response.json()
            else:
                print(f"❌ Erro ao criar instância: {response.status_code} - {response.text}")
                return {"error": response.text, "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {str(e)}")
            return {"error": str(e)}

    def start_existing_session(self, session_name="default"):
        """Conecta uma instância existente"""
        url = f'{self.__api_url}/instance/connect/{session_name}'
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code in [200, 201]:
                print(f"✅ Instância '{session_name}' conectada com sucesso!")
                return response.json()
            elif response.status_code == 422:
                print(f"⚠️ Instância '{session_name}' já está conectada.")
                return {"message": "Instance already connected"}
            else:
                print(f"❌ Erro ao conectar instância: {response.status_code} - {response.text}")
                return {"error": response.text, "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {str(e)}")
            return {"error": str(e)}

    def configure_session(self, session_name="default"):
        """Configura o webhook da instância"""
        url = f'{self.__api_url}/settings/set/{session_name}'
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }
        config = {
            "webhook": {
                "url": "http://api:5000/chatbot/webhook/",
                "enabled": True,
                "webhookByEvents": True,
                "events": ["messages.upsert"]
            }
        }

        try:
            response = requests.post(url, json=config, headers=headers)
            if response.status_code in [200, 201]:
                print(f"✅ Instância '{session_name}' configurada com sucesso!")
                return response.json()
            else:
                print(f"❌ Erro ao configurar instância: {response.status_code} - {response.text}")
                return {"error": response.text, "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            print(f"Erro na configuração da instância: {str(e)}")
            return {"error": str(e)}

    def send_message(self, chat_id, message):
        url = f"{self.__api_url}/message/sendText/{self.session_name}"
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }
        payload = {
            "number": chat_id,
            "text": message
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar mensagem: {str(e)}")
            return {"error": str(e)}

    def get_history_messages(self, chat_id, limit=50):
        url = f"{self.__api_url}/chat/fetchMessages/{self.session_name}?number={chat_id}&limit={limit}"
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }
        try:
            response = requests.get(url, headers=headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter histórico: {str(e)}")
            return {"error": str(e)}

    def start_typing(self, chat_id):
        url = f"{self.__api_url}/message/sendPresence/{self.session_name}"
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }
        payload = {
            "number": chat_id,
            "presence": "composing"
        }
        try:
            requests.post(url, json=payload, headers=headers)
        except requests.exceptions.RequestException as e:
            print(f"Erro ao iniciar digitação: {str(e)}")

    def stop_typing(self, chat_id):
        url = f"{self.__api_url}/message/sendPresence/{self.session_name}"
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }
        payload = {
            "number": chat_id,
            "presence": "paused"
        }
        try:
            requests.post(url, json=payload, headers=headers)
        except requests.exceptions.RequestException as e:
            print(f"Erro ao parar digitação: {str(e)}")