import openai
import os
import asyncio

class OpenAIClient:

    def __init__(self):
        openai.api_key = os.getenv("OPENAI_KEY")

    async def ask(self, prompt: str):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync_call, prompt)

    def _sync_call(self, prompt: str):
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
