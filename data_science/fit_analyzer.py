#Compares resume to job descriptions

!pip install spacy
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
