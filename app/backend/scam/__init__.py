"""
Scam Detection Module
"""
from .scam_detector import ScamDetector
from .email_analyzer import analyze_email_text
from .url_analyzer import analyze_url
from .language_flags import detect_manipulative_language

__all__ = ['ScamDetector', 'analyze_email_text', 'analyze_url', 'detect_manipulative_language']

