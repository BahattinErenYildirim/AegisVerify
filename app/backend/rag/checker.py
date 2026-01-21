"""
RAG Checker module for fact verification
"""
from .retriever import RAGRetriever

class RAGChecker:
    """RAG-based fact checker that uses multiple sources"""
    
    def __init__(self):
        self.retriever = RAGRetriever()
    
    async def check(self, claim: str):  # <-- 'async' eklendi
        """
        Check a claim against RAG sources (Async)
        """
        # Artık retrieve fonksiyonunu 'await' ile bekliyoruz
        results = await self.retriever.retrieve(claim)
        
        return {
            "claim": claim,
            "sources": results,
            "wikipedia_results": len(results.get("wikipedia", [])),
            "news_results": len(results.get("news", [])),
            "factcheck_results": len(results.get("factcheck", []))
        }   