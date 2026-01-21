def detect_manipulative_language(text: str):
    flags = []
    score = 0

    manipulation_keywords = [
        "trust me", "don't tell", "nobody will know",
        "you must", "act now", "final warning"
    ]

    for word in manipulation_keywords:
        if word in text.lower():
            flags.append(word)
            score += 15

    return {
        "manipulation_score": min(100, score),
        "flags": flags
    }
