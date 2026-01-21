from google import genai
from google.genai import types
import os
import asyncio

class GeminiClient:

    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    async def ask(self, prompt: str):
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self._sync_call, prompt)
        return result

    def _sync_call(self, prompt: str):
        response = self.client.models.generate_content(
            model=self.model,
            config=types.GenerateContentConfig(
                temperature=0.6,
                max_output_tokens=1000
            ),
            contents=prompt
        )
        return response.text
