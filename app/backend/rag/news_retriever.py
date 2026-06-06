import httpx
import os
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("AegisRAG")

NEWS_API_URL = "https://newsapi.org/v2/everything"
API_KEY = os.getenv("NEWS_API_KEY")

async def search_news(query: str):
   
    if not API_KEY:
        logger.warning("NewsAPI Key eksik! .env dosyasını kontrol edin.")
        return []

    if not query:
        return []

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(NEWS_API_URL, params={
                "q": query,
                "sortBy": "relevancy",
                "language": "en",
                "apiKey": API_KEY
            }, timeout=6.0)

            if response.status_code != 200:
                logger.warning(f"NewsAPI Hatası: {response.status_code}")
                return []

            return response.json().get("articles", [])

    except Exception as e:
        logger.error(f"NewsAPI Beklenmeyen Hata: {str(e)}")
        return []
