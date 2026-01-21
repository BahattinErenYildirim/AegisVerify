import re
from typing import Dict

def logic_consistency_check(text: str) -> Dict:
    text_lower = text.lower()

    # ---- 1. Contradiction Detection ----
    contradiction_patterns = [
        (r"\bnever\b.*\bbut\b", "Contradiction: 'never' and 'but' used together"),
        (r"\balways\b.*\bexcept\b", "Contradiction between 'always' and 'except'"),
        (r"\b100%\b.*\bnot sure\b", "Claims of certainty and uncertainty together"),
    ]

    contradictions_found = []
    for pattern, description in contradiction_patterns:
        if re.search(pattern, text_lower):
            contradictions_found.append(description)

    # ---- 2. Overclaiming / Overconfidence Detection ----
    overclaim_keywords = [
        "guaranteed",
        "100% true",
        "absolutely proven",
        "no doubt",
        "undisputed fact"
    ]
    overclaims = [w for w in overclaim_keywords if w in text_lower]

    # ---- 3. Uncertainty Signals ----
    uncertainty_keywords = [
        "maybe",
        "possibly",
        "not sure",
        "uncertain",
        "cannot confirm",
    ]
    uncertainties = [w for w in uncertainty_keywords if w in text_lower]

    # ---- 4. Logical Red Flags ----
    logical_red_flags = [
        ("all people", "Overgeneralization"),
        ("everyone knows", "Unverifiable collective claim"),
        ("they say", "Ambiguous source reference"),
    ]
    red_flags_found = [
        desc for kw, desc in logical_red_flags if kw in text_lower
    ]

    # ---- 5. Score Calculation ----
    score = 100
    score -= len(contradictions_found) * 15
    score -= len(overclaims) * 8
    score -= len(uncertainties) * 5
    score -= len(red_flags_found) * 5

    score = max(0, min(100, score))

    # Final structured report
    return {
        "score": score,
        "contradictions": contradictions_found,
        "overclaims": overclaims,
        "uncertainties": uncertainties,
        "logical_issues": red_flags_found,
    }
