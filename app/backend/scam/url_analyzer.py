import re

SUSPICIOUS_TLDS = [
    ".xyz", ".zip", ".top", ".work", ".info", ".click", ".country", ".viajes"
]

PHISHING_KEYWORDS = [
    "verify", "login", "update", "secure", "alert", "confirm",
    "reset", "banking", "urgent", "unlock", "win"
]

def analyze_url(url: str):
    score = 0
    findings = []

    # 1. HTTP yerine HTTPS yoksa
    if url.startswith("http://"):
        score += 20
        findings.append("Non-HTTPS URL")

    # 2. Şüpheli TLD
    if any(url.endswith(tld) for tld in SUSPICIOUS_TLDS):
        score += 25
        findings.append("Suspicious TLD extension")

    # 3. Phishing kelimeleri
    if any(word in url.lower() for word in PHISHING_KEYWORDS):
        score += 30
        findings.append("Contains known phishing keywords")

    # 4. Çok uzun domain
    if len(url) > 80:
        score += 10
        findings.append("Unusually long URL")

    return {
        "risk_score": min(score, 100),
        "flags": findings
    }
