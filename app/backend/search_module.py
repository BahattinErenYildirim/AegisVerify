import asyncio
import logging
# RAG modüllerini içe aktarıyoruz
try:
    from rag.checker import RAGChecker
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False

logger = logging.getLogger("AegisSearch")

def cross_check_sources(text: str):
    """
    Metni RAG (Wikipedia, News, FactCheck) modülleriyle çapraz kontrol eder.
    Risk Engine (senkron) tarafından çağrıldığı için asenkron işlemi burada yönetir.
    """
    if not RAG_AVAILABLE:
        return {
            "status": "modules_missing",
            "details": "RAG modules not found."
        }

    try:
        # Asenkron RAGChecker'ı başlat
        checker = RAGChecker()
        
        # Mevcut bir event loop var mı kontrol et, yoksa yeni oluştur
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Asenkron check fonksiyonunu çalıştır ve sonucu bekle
        if loop.is_running():
            # Eğer halihazırda çalışan bir loop içindeysek (örn: FastAPI)
            # Bu durumda doğrudan çağırmak zordur, nest_asyncio gerekebilir veya
            # mimariyi tamamen async yapmak gerekir. 
            # Şimdilik basit bir "check" sonucu dönüyoruz.
             return {
                "status": "running_async",
                "details": "Async execution context detected."
            }
        else:
            results = loop.run_until_complete(checker.check(text))

        return {
            "status": "verified",
            "source_count": {
                "wikipedia": results.get("wikipedia_results", 0),
                "news": results.get("news_results", 0),
                "factcheck": results.get("factcheck_results", 0)
            },
            "sources": results.get("sources", {})
        }

    except Exception as e:
        logger.error(f"Search Module Error: {str(e)}")
        return {
            "status": "error",
            "details": str(e)
        }