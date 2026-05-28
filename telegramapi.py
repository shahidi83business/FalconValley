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

    async def send_message(self, chat_id, text, keyboard=None, reply_markup=None):
        """
        ارسال پیام با پشتیبانی از هر دو نام پارامتر keyboard و reply_markup
        """
        # اگر از reply_markup استفاده شده بود، آن را در keyboard قرار بده
        final_keyboard = reply_markup if reply_markup else keyboard
        
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        if final_keyboard:
            payload["reply_markup"] = final_keyboard

        async with self.session.post(f"{self.base_url}/sendMessage", json=payload) as resp:
            return await resp.json()
