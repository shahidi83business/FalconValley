import aiohttp

class AIHelper:

    def __init__(self, api_key, model="gpt-5.4"):
        self.api_key = api_key
        self.model = model
        self.url = "https://api.gapgpt.app/v1/chat/completions"

    async def ask(self, prompt, system=None):

        messages = []

        if system:
            messages.append({
                "role": "system",
                "content": system
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=payload, headers=headers) as r:
                data = await r.json()

        return data["choices"][0]["message"]["content"]
