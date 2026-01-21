"""
Hızlı Modül Kontrol Scripti
Backend'in hangi modülleri yüklediğini kontrol eder.
"""
import sys
from pathlib import Path

# Backend klasörünü path'e ekle
BACKEND_DIR = Path(__file__).parent / "app" / "backend"
sys.path.insert(0, str(BACKEND_DIR))

print("=" * 60)
print("🔍 Backend Modül Durumu Kontrolü")
print("=" * 60)

# Modül import testleri
modules_status = {}

# Consensus
try:
    from consensus.engine import ConsensusEngine
    from consensus.geminiclient import GeminiClient
    modules_status["Consensus"] = "✅ Yüklendi"
except Exception as e:
    modules_status["Consensus"] = f"❌ Hata: {e}"

# RAG
try:
    from rag.checker import RAGChecker
    modules_status["RAG"] = "✅ Yüklendi"
except Exception as e:
    modules_status["RAG"] = f"❌ Hata: {e}"

# Scam
try:
    from scam.scam_detector import ScamDetector
    modules_status["Scam"] = "✅ Yüklendi"
except Exception as e:
    modules_status["Scam"] = f"❌ Hata: {e}"

# Graphs
try:
    from graphs.graph_builder import GraphBuilder
    modules_status["Graphs"] = "✅ Yüklendi"
except Exception as e:
    modules_status["Graphs"] = f"❌ Hata: {e}"

# Pipelines
try:
    from pipelines.orchestrator import Orchestrator
    modules_status["Pipelines"] = "✅ Yüklendi"
except Exception as e:
    modules_status["Pipelines"] = f"❌ Hata: {e}"

print("\nModül Durumları:")
for module, status in modules_status.items():
    print(f"  {module:15} - {status}")

print("\n" + "=" * 60)

