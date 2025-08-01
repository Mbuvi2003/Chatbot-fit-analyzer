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
def get_fit_score_with_reason(resume_text_
