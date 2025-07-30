#Load job listings file
import pandas as pd
import requests
import io

url = "https://github.com/Mbuvi2003/Chatbot-fit-analyzer/sample_data/Occupation Data.xlsx"

response = requests.get(url)
data = response.content

# Load Excel file into DataFrame
df = pd.read_excel(io.BytesIO(data))

df.head()  # View first few roles

#Parse O*NET Job Roles into JSON
roles_list = []

for _, row in df.iterrows():
    title = str(row['Title']).strip()
    desc = str(row['Description']).strip()
    if title and desc:
        roles_list.append({
            "role": title,
            "description": desc
        })

# Optional: Save
import json
with open("career_roles.json", "w") as f:
    json.dump(roles_list, f, indent=2)

print(f"Parsed {len(roles_list)} career roles")

#Install & Load Sentence-BERT
!pip install -U sentence-transformers
from sentence_transformers import SentenceTransformer, util
import torch

#Load model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Fast and effective
#Prepare role embeddings
# Build a list of role descriptions
role_texts = [r['description'] for r in roles_list]

# Embed all role descriptions
role_embeddings = model.encode(role_texts, convert_to_tensor=True, show_progress_bar=True)

#Recommendation function
import re

def extract_keywords(text):
    # Simple tokenizer — split words, remove stopwords and short words
    words = re.findall(r'\b\w+\b', text.lower())
    keywords = [w for w in words if len(w) > 2 and w not in {
        'and', 'for', 'the', 'with', 'you', 'are', 'use', 'have', 'has', 'this',
        'your', 'our', 'can', 'will', 'may', 'their', 'they', 'any', 'job',
        'work', 'role', 'field', 'like', 'such', 'that', 'those'
    }]
    return set(keywords)

def recommend_career_fields_explained(resume_text, roles_data, role_embeddings, top_n=5):
    # Embed the resume
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)

    # Similarity with all roles
    similarities = util.cos_sim(resume_embedding, role_embeddings)[0]
    top_indices = torch.topk(similarities, k=top_n).indices

    # Extract resume keywords
    resume_keywords = extract_keywords(resume_text)

    results = []
    for idx in top_indices:
        role = roles_data[idx]
        role_keywords = extract_keywords(role['description'])

        matched_keywords = resume_keywords.intersection(role_keywords)
        explanation = "Your resume matches key terms: " + ", ".join(sorted(matched_keywords)) if matched_keywords else "Some general alignment found."

        results.append({
            "role": role['role'],
            "description": role['description'],
            "score": float(similarities[idx]),
            "matched_keywords": list(sorted(matched_keywords)),
            "explanation": explanation
        })

    return results

#Test
results = recommend_career_fields_explained(resume_text, roles_list, role_embeddings, top_n=5)

for r in results:
    print(f"\n🔹 {r['role']} ({round(r['score'], 3)})")
    print(f"{r['description']}")
    print(f"✅ {r['explanation']}")

