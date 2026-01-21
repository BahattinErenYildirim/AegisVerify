def detect_scam_signals(text):
    red_flags = [
        "money",
        "urgent",
        "immediately",
        "account locked",
        "password reset",
        "verification needed",
    ]
    score = sum([1 for word in red_flags if word in text.lower()]) * 10

    return {
        "score": score,
        "flags": [w for w in red_flags if w in text.lower()]
    }


def detect_bias(text):
    political_words = ["left wing", "right wing", "liberal", "conservative"]
    score = sum(1 for w in political_words if w in text.lower()) * 7

    return {
        "score": score,
        "keywords": [w for w in political_words if w in text.lower()]
    }
