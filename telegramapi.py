import requests

class TelegramBotAPI:
    def __init__(self, token,base_url="https://api.telegram.org/bot"):
        self.base_url = f"{base_url}{token}"

    def _request(self, method, params=None, files=None):
        url = f"{self.base_url}/{method}"
        r = requests.post(url, data=params, files=files)
        r.raise_for_status()
        return r.json()

    # --- Generic ---
    def call(self, method, **params):
        return self._request(method, params)

    # --- Updates ---
    def get_updates(self, offset=None, limit=None, timeout=None, allowed_updates=None):
        return self._request("getUpdates", {
            "offset": offset,
            "limit": limit,
            "timeout": timeout,
            "allowed_updates": allowed_updates
        })

    # --- Messages ---
    def send_message(self, chat_id, text, **kwargs):
        params = {"chat_id": chat_id, "text": text}
        params.update(kwargs)
        return self._request("sendMessage", params)

    def forward_message(self, chat_id, from_chat_id, message_id, **kwargs):
        params = {
            "chat_id": chat_id,
            "from_chat_id": from_chat_id,
            "message_id": message_id
        }
        params.update(kwargs)
        return self._request("forwardMessage", params)

    def copy_message(self, chat_id, from_chat_id, message_id, **kwargs):
        params = {
            "chat_id": chat_id,
            "from_chat_id": from_chat_id,
            "message_id": message_id
        }
        params.update(kwargs)
        return self._request("copyMessage", params)

    def delete_message(self, chat_id, message_id):
        return self._request("deleteMessage", {
            "chat_id": chat_id,
            "message_id": message_id
        })

    # --- Media ---
    def send_photo(self, chat_id, photo, caption=None):
        return self._request(
            "sendPhoto",
            {"chat_id": chat_id, "caption": caption},
            {"photo": photo}
        )

    def send_document(self, chat_id, document, caption=None):
        return self._request(
            "sendDocument",
            {"chat_id": chat_id, "caption": caption},
            {"document": document}
        )

    def send_video(self, chat_id, video, caption=None):
        return self._request(
            "sendVideo",
            {"chat_id": chat_id, "caption": caption},
            {"video": video}
        )

    def send_audio(self, chat_id, audio, caption=None):
        return self._request(
            "sendAudio",
            {"chat_id": chat_id, "caption": caption},
            {"audio": audio}
        )

    def send_voice(self, chat_id, voice):
        return self._request(
            "sendVoice",
            {"chat_id": chat_id},
            {"voice": voice}
        )

    # --- Chat management ---
    def get_chat(self, chat_id):
        return self._request("getChat", {"chat_id": chat_id})

    def get_chat_member(self, chat_id, user_id):
        return self._request("getChatMember", {
            "chat_id": chat_id,
            "user_id": user_id
        })

    def get_chat_administrators(self, chat_id):
        return self._request("getChatAdministrators", {"chat_id": chat_id})

    def ban_chat_member(self, chat_id, user_id, until_date=None):
        return self._request("banChatMember", {
            "chat_id": chat_id,
            "user_id": user_id,
            "until_date": until_date
        })

    def unban_chat_member(self, chat_id, user_id):
        return self._request("unbanChatMember", {
            "chat_id": chat_id,
            "user_id": user_id
        })

    # --- Bot info ---
    def get_me(self):
        return self._request("getMe")

    def log_out(self):
        return self._request("logOut")

    # --- File API ---
    def get_file(self, file_id):
        return self._request("getFile", {"file_id": file_id})
