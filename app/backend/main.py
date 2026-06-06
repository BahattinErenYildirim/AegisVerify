import logging
import os
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv


BACKEND_DIR = Path(__file__).resolve().parent
ENV_PATH = BACKEND_DIR / ".env"


sys.path.append(str(BACKEND_DIR))

print("========== ENV DEBUG START ==========")
print(f"BACKEND DIR: {BACKEND_DIR}")
print(f"ENV PATH: {ENV_PATH}")
print(f"ENV EXISTS: {ENV_PATH.exists()}")

load_dotenv(ENV_PATH, override=True)

API_KEY = os.getenv("GEMINI_API_KEY")
print(f"Loaded GEMINI_API_KEY: {'***' + API_KEY[-4:] if API_KEY else 'None'}")
print("========== ENV DEBUG END ==========")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AegisBackend")


try:
    from consensus.engine import ConsensusEngine
    from consensus.models import SimpleLLMModel
    from consensus.geminiclient import GeminiClient
    CONSENSUS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Consensus modules not available: {e}")
    CONSENSUS_AVAILABLE = False

try:
    from rag.checker import RAGChecker
    RAG_AVAILABLE = True
except ImportError as e:
    logger.warning(f"RAG modules not available: {e}")
    RAG_AVAILABLE = False

try:
    from scam.scam_detector import ScamDetector
    SCAM_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Scam detection modules not available: {e}")
    SCAM_AVAILABLE = False

try:
    from graphs.graph_builder import GraphBuilder
    GRAPH_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Graph modules not available: {e}")
    GRAPH_AVAILABLE = False

try:
    from pipelines.orchestrator import Orchestrator
    PIPELINE_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Pipeline modules not available: {e}")
    PIPELINE_AVAILABLE = False
=
try:
    # UCANBLEHUB ESSENTIAL NEVER DELETE OR CHANGE
    from core import setup_ucanblehub_essentials
    # ✅ AegisVerify Logic Analyzer Entegrasyonu
    from validators import logic_consistency_check
except ImportError:
    # Eğer root dizinden çalıştırılırsa bu yol gerekebilir
    from app.backend.core import setup_ucanblehub_essentials
    from app.backend.validators import logic_consistency_check


if RAG_AVAILABLE:
    rag_checker = RAGChecker()
    logger.info("✅ RAG Checker initialized")

if SCAM_AVAILABLE:
    scam_detector = ScamDetector()
    logger.info("✅ Scam Detector initialized")

if GRAPH_AVAILABLE:
    graph_builder = GraphBuilder()
    logger.info("✅ Graph Builder initialized")

if PIPELINE_AVAILABLE:
    orchestrator = Orchestrator()
    logger.info("✅ Pipeline Orchestrator initialized")

if CONSENSUS_AVAILABLE:
    logger.info("✅ Consensus Engine modules available")

app = FastAPI(title="Gemini Chat Service - AegisVerify")


setup_ucanblehub_essentials(app)

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

if not API_KEY:
    logger.critical("GEMINI_API_KEY .env dosyasından okunamadı! Lütfen kontrol edin.")
    # Uygulamanın çökmemesi için burada raise etmiyoruz ama logluyoruz, 
    # istek geldiğinde hata verecek.

client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = """
You are **AegisVerify**, an advanced, enterprise-grade 
**Global Information Verification & Risk Analysis AI**.

Your mission is to evaluate any user-provided text, message, claim, link,
document, email, article, or social media content and produce a complete,
evidence-based verification and risk assessment.

-----------------------------------------
### CORE OUTPUTS
1. Truthfulness Score (0–100)
2. Reliability Analysis
3. Source Cross-Check
4. Fraud & Scam Risk Detection
5. Bias Detection
6. Summary of Findings
7. Recommended Action

-----------------------------------------
### REQUIRED BEHAVIORS
- Multi-step reasoning
- No hallucinations
- No invented sources
- Provide uncertainty levels
- Language-agnostic
- Privacy-focused
- Professional forensic analysis style
"""


class Message(BaseModel):
    role: str
    content: str

class ChatInput(BaseModel):
    messages: list[Message]

# ===================================================================
# 🤖 Chat Endpoint (AegisVerify entegre!)
# ===================================================================
# 🔥 GÜNCELLEME: 'async def' kullanıldı
@app.post("/ask")
async def ask_assistant(payload: ChatInput):
    try:
        last_message_content = payload.messages[-1].content if payload.messages else ""

        if not last_message_content:
            raise HTTPException(status_code=400, detail="Mesaj içeriği boş olamaz.")

        logger.info(f"Analiz Başliyor: {last_message_content[:30]}...")

        
        try:
            reliability = logic_consistency_check(last_message_content)
        except Exception as e:
            logger.error(f"Logic Analyzer Hatası: {e}")
            # Hata olsa bile devam et, varsayılan değer ata
            reliability = {
                'score': 0, 
                'contradictions': [], 
                'overclaims': [], 
                'uncertainties': [], 
                'logical_issues': ['Analyzer Error']
            }

       
        scam_analysis = None
        if SCAM_AVAILABLE:
            try:
                # Scam detector şimdilik senkron çalışır (CPU bound)
                scam_analysis = scam_detector.detect(last_message_content)
                logger.info("Scam detection completed")
            except Exception as e:
                logger.error(f"Scam Detection Hatası: {e}")
                scam_analysis = None

        # ===========================================================
        # 📚 3) RAG Checker - Source Verification (if available)
        # ===========================================================
        rag_results = None
        if RAG_AVAILABLE:
            try:
                # 🔥 GÜNCELLEME: 'await' eklendi!
                # Artık checker.py async olduğu için cevabı beklemeliyiz.
                rag_results = await rag_checker.check(last_message_content)
                logger.info("RAG check completed")
            except Exception as e:
                logger.error(f"RAG Checker Hatası: {e}")
                rag_results = None

       
        response = client.models.generate_content(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.6,
                max_output_tokens=5000
            ),
            contents=last_message_content
        )

        if not response.text:
            logger.warning("Model boş yanıt döndürdü.")
            raise HTTPException(status_code=500, detail="Model boş yanıt döndürdü.")

        logger.info("LLM Yanıtı başarıyla oluşturuldu.")

    
        analysis_sections = []
        
        # Reliability Section
        analysis_sections.append(f"""
### 🔍 AegisVerify Reliability (Automated Pre-Analysis)
- **Score:** {reliability.get('score', 0)} / 100
- **Contradictions:** {', '.join(reliability.get('contradictions', [])) if reliability.get('contradictions') else 'None'}
- **Overclaims:** {', '.join(reliability.get('overclaims', [])) if reliability.get('overclaims') else 'None'}
- **Logical Issues:** {', '.join(reliability.get('logical_issues', [])) if reliability.get('logical_issues') else 'None'}
""")

        # Scam Detection Section
        if scam_analysis:
            analysis_sections.append(f"""

- **Overall Risk Score:** {scam_analysis.get('overall_risk_score', 0)} / 100
- **Is Scam Risk:** {'🔴 HIGH RISK' if scam_analysis.get('is_scam_risk', False) else '🟢 Low Risk'}
- **Email Analysis Score:** {scam_analysis.get('email_analysis', {}).get('risk_score', 0)} / 100
- **Language Manipulation Score:** {scam_analysis.get('language_analysis', {}).get('manipulation_score', 0)} / 100
- **Detected URLs:** {len(scam_analysis.get('detected_urls', []))}
- **Flags:** {', '.join(scam_analysis.get('email_analysis', {}).get('flags', [])) if scam_analysis.get('email_analysis', {}).get('flags') else 'None'}
""")

        # RAG Results Section
        if rag_results:
            analysis_sections.append(f"""

- **Wikipedia Results:** {rag_results.get('wikipedia_results', 0)}
- **News Results:** {rag_results.get('news_results', 0)}
- **FactCheck Results:** {rag_results.get('factcheck_results', 0)}
""")

        # LLM Analysis Section
        analysis_sections.append(f"""
---


{response.text}
""")

        final_output = "\n".join(analysis_sections).strip()
        return {
            "status": "success",
            "message": last_message_content,
            "response": final_output.strip()
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Beklenmeyen hata: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Servis hatası: {str(e)}")



@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Gemini Chat Service",
        "model": MODEL_NAME,
        "mode": "AegisVerify Active"
    }

@app.get("/modules/status")
def module_status():
    """Check which modules are loaded and available"""
    return {
        "consensus_available": CONSENSUS_AVAILABLE,
        "rag_available": RAG_AVAILABLE,
        "scam_available": SCAM_AVAILABLE,
        "graph_available": GRAPH_AVAILABLE,
        "pipeline_available": PIPELINE_AVAILABLE,
        "modules_initialized": {
            "rag_checker": RAG_AVAILABLE and 'rag_checker' in globals(),
            "scam_detector": SCAM_AVAILABLE and 'scam_detector' in globals(),
            "graph_builder": GRAPH_AVAILABLE and 'graph_builder' in globals(),
            "orchestrator": PIPELINE_AVAILABLE and 'orchestrator' in globals()
        }
    }
