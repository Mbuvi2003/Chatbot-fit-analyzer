# 📁 File: /content/Chatbot-fit-analyzer/api/schemas.py

from pydantic import BaseModel
from typing import List

# 📥 Request schema for resume-to-job fit analyzer
class FitAnalyzerRequest(BaseModel):
    resume_text: str
    job_description: str

# 📤 Response schema for fit analyzer
class FitAnalyzerResponse(BaseModel):
    fit_score: float
    fit_label: str
    missing_skills: List[str]
    explanation: str

# 📥 Request schema for job recommender
class CareerRecommendationRequest(BaseModel):
    resume_text: str
    top_n: int = 5

# 📤 Single recommendation item
class CareerMatch(BaseModel):
    role: str
    description: str
    score: float
    matched_keywords: List[str]
    explanation: str

# 📤 Response schema for recommender
class CareerRecommendationResponse(BaseModel):
    recommendations: List[CareerMatch]
