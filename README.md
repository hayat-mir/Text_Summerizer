📄 Drive Summarizer Dashboard

An AI-powered document summarization web app built with Streamlit that integrates seamlessly with Google Drive.
It supports both local uploads and Drive-based document processing, combining extractive and abstractive summarization techniques — ideal for research papers, reports, and text-heavy PDFs.


<img width="1896" height="927" alt="Screenshot 2025-11-08 104424" src="https://github.com/user-attachments/assets/bbae2b34-3272-4500-856a-9c7963aca4e0" />


🚀 Overview

The Drive Summarizer Dashboard allows users to:

fetch them directly from Google Drive or Upload documents.

Automatically extract text, generate extractive and abstractive summaries.

Evaluate summary quality using ROUGE metrics and compression ratios.

Export all processed results as a CSV file for further analysis.


<img width="1873" height="808" alt="Screenshot 2025-11-08 104509" src="https://github.com/user-attachments/assets/24a18c28-bf87-4410-8258-e4ed05ab6208" />


✨ Key Features

✅ Dual Summarization

Extractive Summary using LSA (Latent Semantic Analysis).

Abstractive Summary using advanced AI models (e.g., Gemini API).

<img width="1915" height="733" alt="Screenshot 2025-11-08 105216" src="https://github.com/user-attachments/assets/6ce4079d-fd40-42e5-a340-57874d86c2b8" />



✅ Google Drive Integration

Browse and process multiple files directly from your Drive folder.

✅ Comprehensive Metrics

ROUGE-1, ROUGE-2, and ROUGE-L scores.

Word count, sentence count, and compression percentage.

✅ Interactive UI

Built with Streamlit for a smooth and intuitive dashboard experience.

✅ Batch Processing

Summarize multiple Drive documents in one go.

✅ CSV Export

Download all processed summaries and metrics in a single click.

<img width="1893" height="759" alt="Screenshot 2025-11-08 105234" src="https://github.com/user-attachments/assets/a0feba7b-df82-4476-9fc8-8903c7e84842" />



🧩 Directory Structure
summarizer/
│
├── app.py                      # Main Streamlit app
│
├── summarizer/
│   ├── parsers.py              # Text extraction logic (PDF/DOCX/TXT)
│   ├── summarizer.py           # Extractive & abstractive summarization
│   ├── metrics.py              # ROUGE and compression metric calculations
│   ├── drive_client.py         # Google Drive authentication & file handling
│   └── __init__.py
│
└── requirements.txt            # Dependencies list

⚙️ Installation
1. Clone the Repository
git clone [https://github.com/<your-username>/drive-summarizer.git](https://github.com/hayat-mir/Text_Summerizer.git)
cd drive-summarizer


3. Create a Virtual Environment
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate



4. Install Dependencies
pip install -r requirements.txt



6. Configure Google Drive API

Go to Google Cloud Console
.

Create a new project and enable the Google Drive API.

Create OAuth 2.0 credentials → Download the JSON file.

Save it as credentials.json in your project root.

The app will prompt you to authenticate during first Drive access.



▶️ Running the App
streamlit run app.py


Then open the provided localhost URL in your browser.

📁 Usage Guide
🧾 Local Upload Mode

Select 📤 Local Upload in the sidebar.

Upload a .pdf, .docx, or .txt file.

Click 🚀 Generate Summaries.



View:

Extractive & Abstractive summaries.

Metrics comparison table.

ROUGE scores and compression statistics.

☁️ Google Drive Mode

Select ☁️ Google Drive in the sidebar.

Enter your Drive Folder ID (from the URL).

Click 🔍 List Files from Drive.

Select one or multiple files → 🚀 Process Selected Files.

Download all results as a CSV via the 💾 Export Results section.

🧠 Evaluation Metrics
Metric	Description
ROUGE-1	Overlap of unigrams between original and summary
ROUGE-2	Overlap of bigrams
ROUGE-L	Longest common subsequence measure
Compression %	Percentage reduction in words compared to the original
