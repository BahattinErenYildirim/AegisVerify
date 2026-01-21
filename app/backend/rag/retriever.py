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
        # 1. Gereksiz prefixleri ve noktalama işaretlerini kaldır
        # (Case insensitive search için (?i) flag'i veya re.IGNORECASE kullanılır)
        text = re.sub(r"\*\*|Subject:|Konu:|URGENT|NOTICE|FINAL|WARNING|ALERT|IMPORTANT|ATTENTION", " ", text, flags=re.IGNORECASE)
        
        # 2. Özel karakterleri temizle (Sadece harf, rakam ve boşluk bırak)
        text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
        
        # 3. STOPWORDS (Etkisiz Kelimeler) Listesi
        # Bu kelimeler arama motorlarını şaşırtır, bunları çıkarıyoruz.
        stopwords = {
            "you", "have", "has", "had", "been", "a", "an", "the", "in", "on", "at", "to", "for", 
            "of", "with", "by", "from", "up", "about", "into", "over", "after", "is", "are", "was", 
            "were", "be", "being", "been", "do", "does", "did", "can", "could", "will", "would", 
            "should", "pending", "dear", "user", "customer", "member", "regards", "sincerely", 
            "hello", "hi", "payment", "transaction", "transfer", "click", "here", "link", "reply"
        }
        
        # Kelimeleri ayır ve filtrele
        words = text.split()
        filtered_words = [w for w in words if w.lower() not in stopwords and len(w) > 2]
        
        # Eğer filtreleme sonucu çok az kelime kaldıysa (riskli), orijinalden daha az filtreleyerek dön
        if len(filtered_words) < 2:
             # Yedeği: Sadece çok kısa kelimeleri at
             return " ".join([w for w in words if len(w) > 3])

        return " ".join(filtered_words)

    def _extract_keywords(self, text: str):
        # 1. Önce Konu (Subject) satırını bulmaya çalış
        subject_match = re.search(r"(?:Subject|Konu):\s*(.*)", text, re.IGNORECASE)
        if subject_match:
            raw_subject = subject_match.group(1)
            cleaned = self._clean_query(raw_subject)
            # Eğer konu satırı temizlendikten sonra anlamlıysa onu kullan
            if len(cleaned) > 3:
                return cleaned
        
        # 2. Konu yoksa veya çok kısaysa metnin ilk anlamlı cümlesini al
        # Genellikle scam maillerde ilk cümle "Google has a settlement" gibi başlar.
        first_sentence = text.split('.')[0]
        
        # Eğer ilk cümle çok uzunsa, sadece ilk 10 kelimeyi alıp temizle
        if len(first_sentence) > 150:
             first_sentence = " ".join(text.split()[:10])
            
        return self._clean_query(first_sentence)

    async def retrieve(self, query: str):
        # Temizlenmiş sorguyu al
        search_query = self._extract_keywords(query)
        print(f"DEBUG: Smart RAG Search Query -> '{search_query}'")

        # Eğer sorgu çok kısaysa aramayı iptal et
        if len(search_query) < 3:
            return {"wikipedia": [], "news": [], "factcheck": []}

        # Paralel Arama Başlat 🚀
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