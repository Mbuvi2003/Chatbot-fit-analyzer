#Resume parser script
#Upload resume file
from google.colab import files

#Import DOCX or PDF files
uploaded = files.upload()

#Install required libraries
!pip install python-docx pdfminer.six

#Text Extractor
import os
from pdfminer.high_level import extract_text
from docx import Document

def extract_resume_text(file_path):
  ext=os.path.splitext(file_path)[1].lower()

  if ext == '.pdf':
    text = extract_text(file_path)
  elif ext == '.docx':
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
  else:
    raise ValueError("Unsupported file format. Please upload .pdf or .docx file")

  return text

#Test with uploaded resume
for filename in uploaded.keys():
  text = extract_resume_text(filename)
  print("Resume text extracted")
  print(text[:1000])
#Save output to a 'txt' file
with open("resume_text_output.txt", "w", encoding="utf-8") as f:
    f.write(text)

files.download("resume_text_output.txt")
