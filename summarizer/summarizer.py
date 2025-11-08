# summarizer.py - FIXED VERSION

import google.generativeai as genai
import os
from dotenv import load_dotenv  # Import this
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

# ✅ CRITICAL: Load .env when module is imported
load_dotenv()

def generate_extractive_summary(text: str, sentences_count: int = 5) -> str:
    """Generate extractive summary using LSA algorithm"""
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        stemmer = Stemmer("english")
        summarizer = LsaSummarizer(stemmer)
        summarizer.stop_words = get_stop_words("english")
        
        summary_sentences = summarizer(parser.document, sentences_count)
        return " ".join([str(sentence) for sentence in summary_sentences])
    except Exception as e:
        return f"[Extractive Error: {str(e)}]"

def generate_abstractive_summary(text: str, max_sentences: int = 5) -> str:
    """Generate abstractive summary using Gemini 2.5 Flash"""
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            return "[Error: GEMINI_API_KEY not found in environment]"
        
        genai.configure(api_key=api_key)
        
        # Use Gemini 2.5 Flash
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        # Limit text to reasonable size
        text_sample = text[:10000] if len(text) > 10000 else text
        
        prompt = f"""Provide a concise summary of the following document in exactly {max_sentences} sentences. Focus on the main ideas and key information:

{text_sample}"""
        
        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        return f"[Abstractive Error: {str(e)}]"

def summarize_document(text: str, extractive_sentences: int = 5, abstractive_sentences: int = 5) -> dict:
    """
    Generate both extractive and abstractive summaries for a document.
    
    Args:
        text: The document text to summarize
        extractive_sentences: Number of sentences for extractive summary
        abstractive_sentences: Number of sentences for abstractive summary
    
    Returns:
        dict with 'extractive' and 'abstractive' keys containing the summaries
    """
    return {
        'extractive': generate_extractive_summary(text, extractive_sentences),
        'abstractive': generate_abstractive_summary(text, abstractive_sentences)
    }