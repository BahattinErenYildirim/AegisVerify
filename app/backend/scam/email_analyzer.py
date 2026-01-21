import re

SUSPICIOUS_WORDS = [
    "urgent", "act now", "limited time", "verify immediately",
    "password expires", "click here", "you have won"
]

def analyze_email_text(text: str):
    score = 0
    findings = []

    # Phishing language pattern
    for word in SUSPICIOUS_WORDS:
        if word.lower() in text.lower():
            score += 20
            findings.append(f"Contains phishing word: {word}")

    # Too many links
    links = re.findall(r"http[s]?://\S+", text)
    if len(links) > 3:
        score += 20
        findings.append("Email contains too many links")

    # Suspicious urgency
    if "!" in text:
        score += 10
        findings.append("Contains excessive exclamation marks")

    return {
        "risk_score": min(score, 100),
        "flags": findings,
        "links": links
    }
