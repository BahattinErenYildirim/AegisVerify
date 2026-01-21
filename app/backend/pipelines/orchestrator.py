# app/backend/pipelines/orchestrator.py
from .basic_pipeline import BasicAnalysisPipeline
from .advanced_pipeline import AdvancedPipeline
import logging

logger = logging.getLogger("AegisOrchestrator")

class Orchestrator:
    def __init__(self):
        # Modüllerin yüklenip yüklenmediğini kontrol ederek başlat
        self.basic_pipeline = BasicAnalysisPipeline()
        self.advanced_pipeline = AdvancedPipeline()

    async def run_full_analysis(self, text: str):
        """
        Tüm analizleri tek bir noktadan yönetir.
        Backend/Main.py içindeki karmaşayı buraya topluyoruz.
        """
        results = {
            "reliability": {},
            "scam_analysis": None,
            "rag_results": None,
            "llm_context": ""
        }

        # 1. Temel Analizler (Scam, Dil, URL)
        # BasicPipeline içine scam_detector mantığını da eklemeni öneririm
        basic_res = self.basic_pipeline.run(text)
        results.update(basic_res)

        # 2. RAG Sonuçlarını LLM Prompt'una Hazırlama
        rag_data = results.get("rag_results", {})
        context_str = ""
        if rag_data:
            context_str = f"""
            FOUND EVIDENCE FROM SEARCH:
            - Wikipedia: {len(rag_data.get('wikipedia', []))} articles
            - News: {len(rag_data.get('news', []))} articles
            - FactChecks: {len(rag_data.get('factcheck', []))} checks
            """
        
        results["llm_context"] = context_str
        return results