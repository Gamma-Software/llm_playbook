import requests


class TelegramIntegration:
    bot_token: str
    bot_chat_id: str

    def send_message(self, message: str):
        command = "".join(["https://api.telegram.org/bot",
                           self.bot_token,
                           "/sendMessage?chat_id=",
                           self.bot_chat_id,
                           "&parse_mode=Markdown&text="])

        return requests.get(command + message).json()

    def receive_message(self) -> str:
        pass
