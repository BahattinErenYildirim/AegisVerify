import os
import asyncio
import requests

class LlamaClient:

    def __init__(self):
        self.key = os.getenv("LLAMA_API_KEY")
        self.url = "https://api.llama-api.com"

    async def ask(self, prompt: str):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync, prompt)

    def _sync(self, prompt):
        try:
            r = requests.post(self.url, json={"prompt": prompt})
            return r.json().get("response", "")
        except:
            return ""
