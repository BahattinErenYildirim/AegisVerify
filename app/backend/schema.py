from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    text: str

class AnalyzeResponse(BaseModel):
    truth_score: int
    reliability: dict
    scam_risk: dict
    bias: dict
    source_validation: dict
