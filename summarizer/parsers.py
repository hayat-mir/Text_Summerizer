# summarizer/parsers.py
import os
import pdfplumber
import docx

print(">>> starting summarizer/parsers.py")

import os

try:
    import pdfplumber
    import docx
    print("✅ pdfplumber and docx imported successfully")
except Exception as e:
    print("❌ import failed:", e)
    raise


def parse_txt(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def parse_docx(path):
    doc = docx.Document(path)
    texts = [p.text for p in doc.paragraphs if p.text.strip()]
    return '\n'.join(texts)

def parse_pdf(path):
    texts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            txt = page.extract_text()
            if txt:
                texts.append(txt)
    return '\n'.join(texts)

def extract_text(path):
    _, ext = os.path.splitext(path)
    ext = ext.lower()
    if ext == '.txt':
        return parse_txt(path)
    if ext == '.docx':
        return parse_docx(path)
    if ext == '.pdf':
        return parse_pdf(path)
    raise ValueError(f"Unsupported file type: {ext}")
