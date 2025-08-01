# 📦 Required imports
import spacy
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from sentence_transformers import SentenceTransformer, util

# ✅ Load Models
# Load BERT NER pipeline
def load_ner_pipeline():
    model_name = "dslim/bert-base-NER"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    return pipeline("ner", model=model, tokenizer=tokenizer, grouped_entities=True)

# Load sentence transformer for similarity scoring
similarity_model = SentenceTransformer('all-MiniLM-L6-v2')  # Fast & light
spacy_model = spacy.load("en_core_web_sm")  # SpaCy for skills extraction
ner_pipeline = load_ner_pipeline()  # Load once

# ✅ Skill extractor using SpaCy
def extract_skills_spacy(text):
    doc = spacy_model(text)
    keywords = []

    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT", "WORK_OF_ART", "SKILL", "NORP", "GPE"]:
            keywords.append(ent.text)

    for chunk in doc.noun_chunks:
        if chunk.text.istitle() and len(chunk.text.split()) <= 3:
            keywords.append(chunk.text.strip())

    return list(set([k for k in keywords if len(k) > 2]))

# ✅ Main function for resume vs JD matching
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

