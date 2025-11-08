# test_metrics.py
from summarizer.metrics import evaluate_summary

# Sample data
original = """
Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to 
the natural intelligence displayed by humans and animals. Leading AI textbooks define 
the field as the study of intelligent agents: any device that perceives its environment 
and takes actions that maximize its chance of successfully achieving its goals. 
Colloquially, the term artificial intelligence is often used to describe machines that 
mimic cognitive functions that humans associate with the human mind, such as learning 
and problem solving.
"""

extractive = """
Artificial intelligence (AI) is intelligence demonstrated by machines. 
Leading AI textbooks define the field as the study of intelligent agents. 
The term artificial intelligence describes machines that mimic cognitive functions.
"""

abstractive = """
AI refers to machines that can perceive their environment and take goal-oriented actions. 
The field focuses on creating intelligent agents that can learn and solve problems like humans.
"""

# Evaluate
metrics = evaluate_summary(original, extractive, abstractive)

# Display results
print("📊 EVALUATION METRICS\n")
print(f"Original Text: {metrics['original_words']} words, {metrics['original_sentences']} sentences\n")

print("🔹 EXTRACTIVE SUMMARY:")
print(f"  Words: {metrics['extractive_words']}")
print(f"  Sentences: {metrics['extractive_sentences']}")
print(f"  Compression: {metrics['extractive_compression']}%")
print(f"  ROUGE-1: {metrics['extractive_rouge1']}")
print(f"  ROUGE-2: {metrics['extractive_rouge2']}")
print(f"  ROUGE-L: {metrics['extractive_rougeL']}\n")

print("🔸 ABSTRACTIVE SUMMARY:")
print(f"  Words: {metrics['abstractive_words']}")
print(f"  Sentences: {metrics['abstractive_sentences']}")
print(f"  Compression: {metrics['abstractive_compression']}%")
print(f"  ROUGE-1: {metrics['abstractive_rouge1']}")
print(f"  ROUGE-2: {metrics['abstractive_rouge2']}")
print(f"  ROUGE-L: {metrics['abstractive_rougeL']}")