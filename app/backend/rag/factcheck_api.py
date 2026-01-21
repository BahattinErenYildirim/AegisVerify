import httpx
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Logger yapılandırması
logger = logging.getLogger("AegisRAG")

FACTCHECK_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
API_KEY = os.getenv("GOOGLE_FACTCHECK_KEY")

async def factcheck_lookup(query: str):
    """
    Google FactCheck Tools API üzerinde asenkron arama yapar.
    Geliştirmeler: API Key kontrolü, Async IO, Detaylı hata mesajları.
    """
    if not API_KEY:
        logger.warning("Google FactCheck API Key eksik! .env dosyasını kontrol edin.")
        return []

    if not query:
        return []

    try:
        async with httpx.AsyncClient() as client:
            # Google API bazen yavaş olabilir, timeout'u 8 saniye yaptık
            response = await client.get(FACTCHECK_URL, params={
                "query": query,
                "key": API_KEY
            }, timeout=8.0)

            if response.status_code != 200:
                logger.warning(f"FactCheck API Hatası: {response.status_code} - {response.text}")
                return []

            data = response.json()
            claims = data.get("claims", [])
            
            logger.info(f"FactCheck'te '{query}' için {len(claims)} doğrulama bulundu.")
            return claims

    except httpx.TimeoutException:
        logger.error(f"FactCheck Zaman Aşımı (Timeout): '{query}'")
        return []
    except Exception as e:
        logger.error(f"FactCheck Beklenmeyen Hata: {str(e)}")
        return []