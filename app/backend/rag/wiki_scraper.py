import httpx
import logging

# Profesyonel Loglama: Print yerine logger kullanıyoruz
logger = logging.getLogger("AegisRAG")

WIKI_API = "https://en.wikipedia.org/w/api.php"

async def search_wikipedia(query: str):
    """
    Wikipedia üzerinde asenkron arama yapar.
    Geliştirmeler: AsyncClient, Timeout yönetimi, Hata yakalama.
    """
    if not query:
        return []

    try:
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "utf8": 1,
            "format": "json"
        }
        
        # AsyncClient ile non-blocking (bloklamayan) istek
        async with httpx.AsyncClient() as client:
            response = await client.get(WIKI_API, params=params, timeout=5.0)
            
            if response.status_code != 200:
                logger.warning(f"Wikipedia API Hatası: {response.status_code}")
                return []

            data = response.json()
            results = data.get("query", {}).get("search", [])
            
            logger.info(f"Wikipedia'da '{query}' için {len(results)} sonuç bulundu.")
            return results

    except httpx.TimeoutException:
        logger.error(f"Wikipedia Zaman Aşımı (Timeout): '{query}'")
        return []
    except Exception as e:
        logger.error(f"Wikipedia Beklenmeyen Hata: {str(e)}")
        return []