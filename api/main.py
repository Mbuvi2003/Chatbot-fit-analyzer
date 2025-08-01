# 📁 File: /content/Chatbot-fit-analyzer/api/main.py

from fastapi import FastAPI
from api.schemas import (
    FitAnalyzerRequest, FitAnalyzerResponse,
    CareerRecommendationRequest, CareerRecommendationResponse
)
from data_science.fit_analyzer import analyze_resume_fit
from data_science.job_recommender import recommend_career_fields, embed_roles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ATS Chatbot API")

# Allow frontend/JS apps to access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "ATS Chatbot API is live 🚀"}

@app.post("/fit-analyzer", response_model=FitAnalyzerResponse)
def fit_analyzer(payload: FitAnalyzerRequest):
    result = analyze_resume_fit(payload.resume_text, payload.job_description)
    return result

@app.post("/recommend-careers", response_model=CareerRecommendationResponse)
def recommend_careers(payload: CareerRecommendationRequest):
    recommendations = recommend_career_fields(payload.resume_text, top_n=payload.top_n)
    return {"recommendations": recommendations}
