from rag.retriever import RAGRetriever
from scam.url_analyzer import analyze_url
from scam.email_analyzer import analyze_email_text
from scam.language_flags import detect_manipulative_language

class BasicAnalysisPipeline:

    def __init__(self):
        self.rag = RAGRetriever()

    def run(self, text: str):
        rag_results = self.rag.retrieve(text)

        scam_lang = detect_manipulative_language(text)
        scam_email = analyze_email_text(text)
        
        return {
            "rag_results": rag_results,
            "scam_language": scam_lang,
            "scam_email": scam_email
        }
