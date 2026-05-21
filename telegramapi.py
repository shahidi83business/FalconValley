# telegramapi.py

import aiohttp


class TelegramBotAPI:

    def __init__(self, base_url: str):
        self.base_url = f"{base_url}"
        self.session: aiohttp.ClientSession | None = None

    async def start(self):
        """ایجاد session"""
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def close(self):
        """بستن session"""
        if self.session:
            await self.session.close()
            self.session = None

    async def get_updates(self, offset=None):

        if self.session is None:
            raise RuntimeError("Session is not started. Call await bot.start() first.")

        url = f"{self.base_url}/getUpdates"

        params = {"timeout": 30}

        if offset is not None:
            params["offset"] = offset

        async with self.session.get(url, params=params) as r:
            return await r.json()

    async def send_message(self, chat_id, text,keyboard=None):

        if self.session is None:
            raise RuntimeError("Session is not started. Call await bot.start() first.")

        url = f"{self.base_url}/sendMessage"

        payload = {
            "chat_id": chat_id,
          "text": text
        }
        if keyboard is not None:
            payload["reply_markup"] = keyboard
            
        async with self.session.post(url, json=payload) as r:
            return await r.json()
