"""
Comprehensive Scam Detector combining all scam detection modules
"""
from .email_analyzer import analyze_email_text
from .url_analyzer import analyze_url
from .language_flags import detect_manipulative_language
import re

class ScamDetector:
    """Unified scam detection system"""
    
    def __init__(self):
        pass
    
    def detect(self, text: str):
        """
        Comprehensive scam detection on text
        
        Args:
            text: Text to analyze for scam indicators
            
        Returns:
            dict: Comprehensive scam analysis results
        """
        # Extract URLs from text
        urls = re.findall(r"http[s]?://\S+", text)
        
        # Analyze email patterns
        email_analysis = analyze_email_text(text)
        
        # Analyze manipulative language
        language_analysis = detect_manipulative_language(text)
        
        # Analyze URLs if found
        url_analyses = []
        if urls:
            for url in urls:
                url_analyses.append({
                    "url": url,
                    "analysis": analyze_url(url)
                })
        
        # Calculate overall risk score
        overall_risk = max(
            email_analysis.get("risk_score", 0),
            language_analysis.get("manipulation_score", 0),
            max([ua["analysis"]["risk_score"] for ua in url_analyses], default=0)
        )
        
        return {
            "overall_risk_score": overall_risk,
            "email_analysis": email_analysis,
            "language_analysis": language_analysis,
            "url_analyses": url_analyses,
            "detected_urls": urls,
            "is_scam_risk": overall_risk > 50
        }

