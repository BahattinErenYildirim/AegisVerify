# app/backend/risk_engine.py

from .detectors import detect_scam_signals, detect_bias
from .search_module import cross_check_sources
from .validators import logic_consistency_check

class AegisVerifyEngine:
    def process(self, text: str):
        result = {}

        # 1 — Logic & Reliability
        result["reliability"] = logic_consistency_check(text)

        # 2 — Scam / Fraud
        result["scam_risk"] = detect_scam_signals(text)

        # 3 — Bias Detection
        result["bias"] = detect_bias(text)

        # 4 — Source Cross Check
        result["source_validation"] = cross_check_sources(text)

        # 5 — Final Truthfulness Score
        result["truth_score"] = self.calculate_truth_score(result)

        return result

    def calculate_truth_score(self, features):
        base = 100
        base -= features["scam_risk"]["score"] * 1.2
        base -= features["bias"]["score"] * 0.8
        base -= (100 - features["reliability"]["score"]) * 0.7

        # Sınırla
        return max(0, min(100, round(base)))
