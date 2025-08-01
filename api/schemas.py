# api/schemas.py

from pydantic import BaseModel
from typing import List

# Request schema for Fit Analyzer
class FitAnalyzerRequest(BaseModel):
    resume_text: str
    job_description: str

# Response schema for Fit Analyzer
class FitAnalyzerResponse(BaseModel):
    fit_score: float
    fit_label: str
    missing_skills: List[str]
    explanation: str

# Request schema for Job Recommender
class CareerRecommendationRequest(BaseModel):
    resume_text: str
    top_n: int = 5  # optional, default 5

# Each recommended job field
class CareerMatch(BaseModel):
    role: str
    description: str
    score: float
    matched_keywords: List[str]
    explanation: str

# Response schema for recommender
class CareerRecommendationResponse(BaseModel):
    recommendations: List[CareerMatch]
