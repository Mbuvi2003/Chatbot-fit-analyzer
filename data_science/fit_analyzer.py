#Compares resume to job descriptions


!python -m spacy download en_core_web_sm
#Skills extractor
# Install Hugging Face Transformers and other tools
!pip install transformers datasets torch pdfplumber python-docx

#Load pre-trained BERT NER Model
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

#Load BERT model for NER(named entity recognition)
model_name = "dslim/bert-base-NER"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)

#Create a NER pipeline
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, grouped_entities=True)

#Extract named entities
ner_results = ner_pipeline(text)
#Filter entities
for entity in ner_results:
  print(f"{entity['entity_group']}: {entity['word']} (Score: {round(entity['score'], 2)})")
  
#THE MODEL
from sentence_transformers import SentenceTransformer, util
import numpy as np
#Load pre trained model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Small & fast

import spacy
# Load spaCy model once
nlp = spacy.load("en_core_web_sm")

def extract_skills_spacy(text):
    doc = nlp(text)
    keywords = []

    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT", "WORK_OF_ART", "SKILL", "NORP", "GPE"]:  # Optional labels
            keywords.append(ent.text)

    # Add all capitalized single/multi-word tokens (like Power BI)
    for chunk in doc.noun_chunks:
        if chunk.text.istitle() and len(chunk.text.split()) <= 3:
            keywords.append(chunk.text.strip())

    return list(set([k for k in keywords if len(k) > 2]))
  
  def get_fit_score_with_reason(resume_text, jd_text, threshold=0.65):
    # Embed and score
    embeddings = model.encode([resume_text, jd_text], convert_to_tensor=True)
    score = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()
    score_rounded = round(score, 3)

    label = "Good Fit ✅" if score >= threshold else "Not a Fit ❌"

    # ⬇️ New extractor here
    jd_skills = extract_skills_spacy(jd_text)
    missing = [skill for skill in jd_skills if skill.lower() not in resume_text.lower()]

    # Explanation logic
    if label == "Good Fit ✅" and not missing:
        explanation = "Resume closely matches the job requirements."
    elif label == "Good Fit ✅":
        explanation = f"Strong match, but missing: {', '.join(missing[:5])}."
    else:
        explanation = f"Weak match. Missing important items: {', '.join(missing[:5])}."

    return {
        "fit_score": score_rounded,
        "fit_label": label,
        "missing_skills": missing[:5],
        "explanation": explanation
    }

#Test the model with sample
resume = "Python developer with experience in SQL and Excel. Built dashboards in Power BI."
jd = "Looking for a Data Analyst skilled in SQL, Excel, and Tableau."

result = get_fit_score_with_reason(resume, jd)
print(result)
