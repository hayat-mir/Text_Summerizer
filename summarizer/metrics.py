# summarizer/metrics.py

from rouge_score import rouge_scorer
import re

def calculate_rouge_scores(reference_text: str, summary_text: str) -> dict:
    """
    Calculate ROUGE scores comparing summary to original text.
    
    Args:
        reference_text: Original document text
        summary_text: Generated summary
    
    Returns:
        dict with rouge1, rouge2, rougeL scores (F1 scores)
    """
    try:
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        scores = scorer.score(reference_text, summary_text)
        
        return {
            'rouge1': round(scores['rouge1'].fmeasure, 4),
            'rouge2': round(scores['rouge2'].fmeasure, 4),
            'rougeL': round(scores['rougeL'].fmeasure, 4)
        }
    except Exception as e:
        return {
            'rouge1': 0.0,
            'rouge2': 0.0,
            'rougeL': 0.0
        }

def calculate_compression_ratio(original_text: str, summary_text: str) -> float:
    """
    Calculate compression ratio (percentage of original length).
    
    Args:
        original_text: Original document text
        summary_text: Generated summary
    
    Returns:
        Compression ratio as percentage (e.g., 15.5 means summary is 15.5% of original)
    """
    try:
        original_words = len(original_text.split())
        summary_words = len(summary_text.split())
        
        if original_words == 0:
            return 0.0
        
        ratio = (summary_words / original_words) * 100
        return round(ratio, 2)
    except Exception:
        return 0.0

def count_sentences(text: str) -> int:
    """Count number of sentences in text."""
    sentences = re.split(r'[.!?]+', text)
    return len([s for s in sentences if s.strip()])

def evaluate_summary(original_text: str, extractive_summary: str, abstractive_summary: str) -> dict:
    """
    Comprehensive evaluation of both summaries.
    
    Returns:
        dict with all metrics for both summary types
    """
    # ROUGE scores
    extractive_rouge = calculate_rouge_scores(original_text, extractive_summary)
    abstractive_rouge = calculate_rouge_scores(original_text, abstractive_summary)
    
    # Compression ratios
    extractive_compression = calculate_compression_ratio(original_text, extractive_summary)
    abstractive_compression = calculate_compression_ratio(original_text, abstractive_summary)
    
    # Word counts
    original_words = len(original_text.split())
    extractive_words = len(extractive_summary.split())
    abstractive_words = len(abstractive_summary.split())
    
    # Sentence counts
    original_sentences = count_sentences(original_text)
    extractive_sentences = count_sentences(extractive_summary)
    abstractive_sentences = count_sentences(abstractive_summary)
    
    return {
        # Original text stats
        'original_words': original_words,
        'original_sentences': original_sentences,
        
        # Extractive metrics
        'extractive_words': extractive_words,
        'extractive_sentences': extractive_sentences,
        'extractive_compression': extractive_compression,
        'extractive_rouge1': extractive_rouge['rouge1'],
        'extractive_rouge2': extractive_rouge['rouge2'],
        'extractive_rougeL': extractive_rouge['rougeL'],
        
        # Abstractive metrics
        'abstractive_words': abstractive_words,
        'abstractive_sentences': abstractive_sentences,
        'abstractive_compression': abstractive_compression,
        'abstractive_rouge1': abstractive_rouge['rouge1'],
        'abstractive_rouge2': abstractive_rouge['rouge2'],
        'abstractive_rougeL': abstractive_rouge['rougeL']
    }