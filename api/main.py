# api/main.py

from fastapi import FastAPI
from api.schemas import *
from data_science.fit_analyzer import analyze_resume_fit
from data_science.job_recommender import recommend_career_fields, embed_roles
import json

# 🔥 FastAPI app object
app = FastAPI(title="ATS Chatbot API", version="1.0")

# 🌍 Load preprocessed job role data
with open("sample_data/career_roles.json", "r") as f:
    roles_list = json.load(f)

role_embeddings = embed_roles(roles_list)  # Precompute once

# 🧪 Test endpoint
@app.get("/health")
def health_check():
    return {"status": "OK"}

# 🎯 Resume-to-Job Fit Analyzer
@app.post("/fit-analyzer", response_model=FitAnalyzerResponse)
def fit_analyzer_api(payload: FitAnalyzerRequest):
    result = analyze_resume_fit(payload.resume_text, payload.job_description)
    return result

# 💡 Career Recommendation Engine
@app.post("/recommend-careers", response_model=CareerRecommendationResponse)
def recommend_careers_api(payload: CareerRecommendationRequest):
    matches = recommend_career_fields(
        payload.resume_text,
        roles_list,
        role_embeddings,
        top_n=payload.top_n
    )
    return {"recommendations": matches}
