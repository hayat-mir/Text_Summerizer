# process_one.py - Updated with Metrics
import importlib.util, os

spec = importlib.util.spec_from_file_location(
    "summarizer.parsers",
    os.path.join(os.path.dirname(__file__), "summarizer", "parsers.py")
)
parsers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parsers)

extract_text = parsers.extract_text


import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import os, tempfile, csv
from summarizer.drive_client import get_drive_service, list_files_in_folder, download_file
from summarizer.parsers import extract_text
from summarizer.summarizer import summarize_document
from summarizer.metrics import evaluate_summary  # NEW: Import metrics

# === CONFIG ===
FOLDER_ID = "16682ch8bgfH1sqmayPja878O0McKaz__"   # Your folder ID
TARGET_FILENAME = "Resume_AIML-4.pdf"             # File to process

def find_file(files, name):
    for f in files:
        if f['name'] == name:
            return f
    return None

def main():
    print("🚀 Starting Drive Summarizer with Metrics...\n")
    
    service = get_drive_service()
    files = list_files_in_folder(service, FOLDER_ID)
    f = find_file(files, TARGET_FILENAME)
    
    if not f:
        print("❌ File not found in folder. Files available:")
        for x in files:
            print(" -", x['name'])
        return

    tmpdir = tempfile.mkdtemp()
    dest = os.path.join(tmpdir, f['name'])
    print(f"📥 Downloading: {f['name']}")
    download_file(service, f['id'], dest)

    print("📄 Extracting text...")
    text = extract_text(dest)
    print(f"✅ Extracted {len(text)} characters")

    # Check for likely scanned PDF
    if len(text) < 100:
        print("⚠️  Warning: extracted text is very short. This might be a scanned PDF.")
        return

    print("\n🤖 Generating summaries (may take a few seconds)...")
    res = summarize_document(text, extractive_sentences=4)
    print("✅ Summaries generated")

    print("\n📊 Calculating metrics...")
    metrics = evaluate_summary(text, res["extractive"], res["abstractive"])
    print("✅ Metrics calculated")

    # Prepare row with all data
    row = {
        "filename": f['name'],
        "original_words": metrics['original_words'],
        "original_sentences": metrics['original_sentences'],
        
        "extractive_summary": res["extractive"],
        "extractive_words": metrics['extractive_words'],
        "extractive_compression": metrics['extractive_compression'],
        "extractive_rouge1": metrics['extractive_rouge1'],
        "extractive_rouge2": metrics['extractive_rouge2'],
        "extractive_rougeL": metrics['extractive_rougeL'],
        
        "abstractive_summary": res["abstractive"],
        "abstractive_words": metrics['abstractive_words'],
        "abstractive_compression": metrics['abstractive_compression'],
        "abstractive_rouge1": metrics['abstractive_rouge1'],
        "abstractive_rouge2": metrics['abstractive_rouge2'],
        "abstractive_rougeL": metrics['abstractive_rougeL']
    }

    # Save to CSV
    csv_path = "summaries_with_metrics.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=row.keys())
        writer.writeheader()
        writer.writerow(row)

    print(f"\n{'='*60}")
    print("✅ SUCCESS! CSV saved to:", csv_path)
    print(f"{'='*60}")
    
    # Display results
    print("\n📈 SUMMARY STATISTICS:")
    print(f"   Original Document: {metrics['original_words']} words, {metrics['original_sentences']} sentences")
    print(f"\n   🔹 Extractive Summary:")
    print(f"      Words: {metrics['extractive_words']} ({metrics['extractive_compression']}% compression)")
    print(f"      ROUGE-1: {metrics['extractive_rouge1']}")
    print(f"      ROUGE-2: {metrics['extractive_rouge2']}")
    print(f"      ROUGE-L: {metrics['extractive_rougeL']}")
    print(f"\n   🔸 Abstractive Summary:")
    print(f"      Words: {metrics['abstractive_words']} ({metrics['abstractive_compression']}% compression)")
    print(f"      ROUGE-1: {metrics['abstractive_rouge1']}")
    print(f"      ROUGE-2: {metrics['abstractive_rouge2']}")
    print(f"      ROUGE-L: {metrics['abstractive_rougeL']}")
    
    print(f"\n{'='*60}")
    print("\n📝 EXTRACTIVE SUMMARY:")
    print(res["extractive"])
    print("\n📝 ABSTRACTIVE SUMMARY:")
    print(res["abstractive"])
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    main()