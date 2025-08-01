# 📁 File: api/main.py

from fastapi import FastAPI
from api.schemas import (
    FitAnalyzerRequest, FitAnalyzerResponse,
    CareerRecommendationRequest, CareerRecommendationResponse
)
from data_science.fit_analyzer import get_fit_score_with_reason
from data_science.job_recommender import recommend_career_fields, embed_roles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ATS Chatbot API")

# Allow any frontend to access the API (useful during development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "✅ ATS Chatbot API is Live!"}

@app.post("/fit-analyzer", response_model=FitAnalyzerResponse)
def fit_analyzer(payload: FitAnalyzerRequest):
    result = get_fit_score_with_reason(payload.resume_text, payload.job_description)
    return result

@app.post("/recommend-careers", response_model=CareerRecommendationResponse)
def recommend_careers(payload: CareerRecommendationRequest):
    recommendations = recommend_career_fields(payload.resume_text, top_n=payload.top_n)
    return {"recommendations": recommendations}
@app.get("/")
def read_root():
    return {"message": "Welcome to the ATS Resume Fit Analyzer"}

# other endpoints here...
