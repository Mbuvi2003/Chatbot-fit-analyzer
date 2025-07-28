#Extracts info from job descriptions

# Upload one or more job descriptions (as .txt files)
job_files = files.upload()

def read_job_descriptions(file_dict):
    job_data = {}
    for filename in file_dict:
        with open(filename, 'r', encoding='utf-8') as f:
            job_data[filename] = f.read()
    return job_data

job_descriptions = read_job_descriptions(job_files)

# View one job description
for name, jd in job_descriptions.items():
    print(f"\n📄 {name}\n{'='*40}\n{jd[:1000]}")  # Print first 1000 characters

#Extract Education & Experience with NER + Regex
import re

def extract_education(text):
    education_keywords = [
        "Bachelor", "Master", "PhD", "BSc", "MSc", "Diploma", "Degree", "High School"
    ]
    education_matches = [line for line in text.split('\n') if any(k.lower() in line.lower() for k in education_keywords)]
    return education_matches

def extract_experience(text):
    experience_patterns = [
        r"(\d+)\+?\s+years?\s+(?:of\s+)?experience",
        r"experience\s+of\s+(\d+)\s+years?",
        r"worked\s+for\s+(\d+)\s+years?",
    ]
    found = []
    for pattern in experience_patterns:
        found += re.findall(pattern, text, re.IGNORECASE)
    return found

education = extract_education(text)
experience = extract_experience(text)

print("🎓 Education Found:", education)
print("💼 Experience Found:", experience)

#Save All Parsed Info (JSON)
import json

parsed_data = {
    "skills": [e['word'] for e in ner_results if e['entity_group'] == 'MISC'],  # Customize if needed
    "education": education,
    "experience_years": experience
}

# Save to JSON
with open("parsed_resume_data.json", "w") as outfile:
    json.dump(parsed_data, outfile, indent=4)

# Offer download
files.download("parsed_resume_data.json")
