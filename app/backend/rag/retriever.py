import asyncio
import re
from .wiki_scraper import search_wikipedia
from .news_retriever import search_news
from .factcheck_api import factcheck_lookup

class RAGRetriever:

    def _clean_query(self, text: str):
        """
        Arama terimini 'gürültüden' ve dolgu kelimelerden temizler.
        Hedef: 'You Have a Pending Google Settlement Payout' -> 'Google Settlement Payout'
        """
       
        text = re.sub(r"\*\*|Subject:|Konu:|URGENT|NOTICE|FINAL|WARNING|ALERT|IMPORTANT|ATTENTION", " ", text, flags=re.IGNORECASE)
        
        
        text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
        
        
        stopwords = {
            "you", "have", "has", "had", "been", "a", "an", "the", "in", "on", "at", "to", "for", 
            "of", "with", "by", "from", "up", "about", "into", "over", "after", "is", "are", "was", 
            "were", "be", "being", "been", "do", "does", "did", "can", "could", "will", "would", 
            "should", "pending", "dear", "user", "customer", "member", "regards", "sincerely", 
            "hello", "hi", "payment", "transaction", "transfer", "click", "here", "link", "reply"
        }
        
        
        words = text.split()
        filtered_words = [w for w in words if w.lower() not in stopwords and len(w) > 2]
        
       
        if len(filtered_words) < 2:
             
             return " ".join([w for w in words if len(w) > 3])

        return " ".join(filtered_words)

    def _extract_keywords(self, text: str):
       
        subject_match = re.search(r"(?:Subject|Konu):\s*(.*)", text, re.IGNORECASE)
        if subject_match:
            raw_subject = subject_match.group(1)
            cleaned = self._clean_query(raw_subject)
           
            if len(cleaned) > 3:
                return cleaned
        
       
        first_sentence = text.split('.')[0]
        
      
        if len(first_sentence) > 150:
             first_sentence = " ".join(text.split()[:10])
            
        return self._clean_query(first_sentence)

    async def retrieve(self, query: str):
       
        search_query = self._extract_keywords(query)
        print(f"DEBUG: Smart RAG Search Query -> '{search_query}'")

        
        if len(search_query) < 3:
            return {"wikipedia": [], "news": [], "factcheck": []}

        
        try:
            wiki_task = search_wikipedia(search_query)
            news_task = search_news(search_query)
            fact_task = factcheck_lookup(search_query)

            results_list = await asyncio.gather(wiki_task, news_task, fact_task)

            return {
                "wikipedia": results_list[0],
                "news": results_list[1],
                "factcheck": results_list[2]
            }
        except Exception as e:
            print(f"RAG Error: {e}")
            return {"wikipedia": [], "news": [], "factcheck": []}
