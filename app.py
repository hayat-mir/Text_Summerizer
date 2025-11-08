# app.py - Enhanced with Google Drive Integration

import streamlit as st
import tempfile
import os
from summarizer.parsers import extract_text
from summarizer.summarizer import summarize_document
from summarizer.metrics import evaluate_summary
from summarizer.drive_client import get_drive_service, list_files_in_folder, download_file
import pandas as pd

# Page config
st.set_page_config(
    page_title="Drive Summarizer",
    page_icon="📄",
    layout="wide"
)

# Title
st.title("📄 Drive Summarizer Dashboard")
st.markdown("Process documents from Google Drive or upload locally")

# Sidebar
st.sidebar.header("⚙️ Settings")
extractive_sentences = st.sidebar.slider("Extractive Summary Sentences", 3, 10, 5)
abstractive_sentences = st.sidebar.slider("Abstractive Summary Sentences", 3, 10, 5)

# Source selection
st.sidebar.header("📂 Document Source")
source = st.sidebar.radio(
    "Choose source:",
    ["📤 Local Upload", "☁️ Google Drive"],
    index=0
)

# Initialize session state for results
if 'results' not in st.session_state:
    st.session_state.results = []

def process_file(file_path, file_name):
    """Process a single file and return results"""
    # Extract text
    text = extract_text(file_path)
    
    if len(text) < 100:
        return None, "⚠️ Text too short (possible scanned PDF)"
    
    # Generate summaries
    summaries = summarize_document(
        text, 
        extractive_sentences=extractive_sentences,
        abstractive_sentences=abstractive_sentences
    )
    
    # Calculate metrics
    metrics = evaluate_summary(
        text, 
        summaries['extractive'], 
        summaries['abstractive']
    )
    
    result = {
        'filename': file_name,
        'text': text,
        'summaries': summaries,
        'metrics': metrics
    }
    
    return result, None

def display_results(result):
    """Display results for a single document"""
    metrics = result['metrics']
    summaries = result['summaries']
    
    st.success(f"✅ Processed: {result['filename']}")
    
    # Display metrics
    st.subheader("📊 Summary Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Original Words", metrics['original_words'])
        st.metric("Original Sentences", metrics['original_sentences'])
    
    with col2:
        st.metric("Extractive Compression", f"{metrics['extractive_compression']}%")
        st.metric("Extractive ROUGE-L", f"{metrics['extractive_rougeL']:.4f}")
    
    with col3:
        st.metric("Abstractive Compression", f"{metrics['abstractive_compression']}%")
        st.metric("Abstractive ROUGE-L", f"{metrics['abstractive_rougeL']:.4f}")
    
    # Detailed metrics table
    st.subheader("📈 Detailed Metrics Comparison")
    
    comparison_data = {
        "Metric": ["Words", "Sentences", "Compression %", "ROUGE-1", "ROUGE-2", "ROUGE-L"],
        "Extractive": [
            metrics['extractive_words'],
            metrics['extractive_sentences'],
            f"{metrics['extractive_compression']}%",
            f"{metrics['extractive_rouge1']:.4f}",
            f"{metrics['extractive_rouge2']:.4f}",
            f"{metrics['extractive_rougeL']:.4f}"
        ],
        "Abstractive": [
            metrics['abstractive_words'],
            metrics['abstractive_sentences'],
            f"{metrics['abstractive_compression']}%",
            f"{metrics['abstractive_rouge1']:.4f}",
            f"{metrics['abstractive_rouge2']:.4f}",
            f"{metrics['abstractive_rougeL']:.4f}"
        ]
    }
    
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Display summaries side by side
    st.subheader("📝 Summaries")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔹 Extractive Summary**")
        st.info(summaries['extractive'])
    
    with col2:
        st.markdown("**🔸 Abstractive Summary**")
        st.success(summaries['abstractive'])
    
    # Show original text (expandable)
    with st.expander("📄 View Original Text"):
        st.text_area("Original Document Text", result['text'], height=300, disabled=True)

# ==================== LOCAL UPLOAD MODE ====================
if source == "📤 Local Upload":
    st.header("📤 Upload Document")
    
    uploaded_file = st.file_uploader(
        "Choose a document (PDF, DOCX, or TXT)", 
        type=['pdf', 'docx', 'txt']
    )
    
    if uploaded_file:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        st.info(f"📊 File: {uploaded_file.name} ({len(uploaded_file.getvalue())} bytes)")
        
        if st.button("🚀 Generate Summaries", type="primary"):
            with st.spinner("🤖 Processing... This may take 10-20 seconds..."):
                result, error = process_file(tmp_path, uploaded_file.name)
                
                if error:
                    st.error(error)
                else:
                    display_results(result)
                    st.session_state.results = [result]
        
        # Clean up temp file
        try:
            os.unlink(tmp_path)
        except:
            pass
    
    else:
        st.info("👆 Upload a document to get started!")

# ==================== GOOGLE DRIVE MODE ====================
elif source == "☁️ Google Drive":
    st.header("☁️ Google Drive Integration")
    
    folder_id = st.text_input(
        "Enter Google Drive Folder ID:",
        placeholder="e.g., 16682ch8bgfH1sqmayPja878O0McKaz__",
        help="Find this in the Drive folder URL: drive.google.com/drive/folders/[FOLDER_ID]"
    )
    
    if folder_id:
        if st.button("🔍 List Files from Drive", type="primary"):
            with st.spinner("🔐 Authenticating with Google Drive..."):
                try:
                    service = get_drive_service()
                    files = list_files_in_folder(service, folder_id)
                    
                    # Filter for supported files
                    supported_files = [
                        f for f in files 
                        if any(f['name'].lower().endswith(ext) for ext in ['.pdf', '.docx', '.txt'])
                    ]
                    
                    if not supported_files:
                        st.warning("⚠️ No supported documents found in this folder (PDF, DOCX, TXT)")
                    else:
                        st.success(f"✅ Found {len(supported_files)} document(s)")
                        
                        # Store in session state
                        st.session_state.drive_files = supported_files
                        st.session_state.drive_service = service
                        
                except Exception as e:
                    st.error(f"❌ Error connecting to Drive: {str(e)}")
        
        # Show files if available
        if 'drive_files' in st.session_state and st.session_state.drive_files:
            st.subheader("📁 Available Files")
            
            # Let user select files
            selected_files = st.multiselect(
                "Select files to process:",
                options=[f['name'] for f in st.session_state.drive_files],
                default=[st.session_state.drive_files[0]['name']]
            )
            
            if st.button("🚀 Process Selected Files", type="primary"):
                results = []
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                tmpdir = tempfile.mkdtemp()
                
                for idx, file_name in enumerate(selected_files):
                    status_text.text(f"Processing {idx+1}/{len(selected_files)}: {file_name}")
                    
                    # Find file info
                    file_info = next(f for f in st.session_state.drive_files if f['name'] == file_name)
                    
                    # Download
                    dest_path = os.path.join(tmpdir, file_name)
                    download_file(st.session_state.drive_service, file_info['id'], dest_path)
                    
                    # Process
                    result, error = process_file(dest_path, file_name)
                    
                    if result:
                        results.append(result)
                    else:
                        st.warning(f"⚠️ Skipped {file_name}: {error}")
                    
                    progress_bar.progress((idx + 1) / len(selected_files))
                
                status_text.text("✅ Processing complete!")
                st.session_state.results = results
                
                # Display all results
                for result in results:
                    st.divider()
                    display_results(result)
    
    else:
        st.info("👆 Enter a Google Drive folder ID to get started!")
        st.markdown("""
        **How to find your Folder ID:**
        1. Open Google Drive folder in browser
        2. Copy the ID from URL: `drive.google.com/drive/folders/[THIS_IS_THE_ID]`
        3. Paste it above
        """)

# ==================== DOWNLOAD RESULTS ====================
if st.session_state.results:
    st.divider()
    st.header("💾 Export Results")
    
    # Prepare CSV data
    csv_data = []
    for result in st.session_state.results:
        csv_data.append({
            "Filename": result['filename'],
            "Original Words": result['metrics']['original_words'],
            "Extractive Summary": result['summaries']['extractive'],
            "Extractive Compression": f"{result['metrics']['extractive_compression']}%",
            "Extractive ROUGE-L": f"{result['metrics']['extractive_rougeL']:.4f}",
            "Abstractive Summary": result['summaries']['abstractive'],
            "Abstractive Compression": f"{result['metrics']['abstractive_compression']}%",
            "Abstractive ROUGE-L": f"{result['metrics']['abstractive_rougeL']:.4f}"
        })
    
    csv_df = pd.DataFrame(csv_data)
    csv_string = csv_df.to_csv(index=False)
    
    st.download_button(
        label="📥 Download All Results as CSV",
        data=csv_string,
        file_name="drive_summaries.csv",
        mime="text/csv"
    )

# Instructions
if not st.session_state.results:
    st.divider()
    st.markdown("""
    ### 🎯 Features:
    - ✅ **Local Upload**: Quick testing with single files
    - ✅ **Google Drive**: Process multiple files from Drive folders
    - ✅ **Dual Summarization**: Extractive (LSA) + Abstractive (Gemini AI)
    - ✅ **Quality Metrics**: ROUGE scores and compression ratios
    - ✅ **Batch Processing**: Handle multiple documents at once
    - ✅ **CSV Export**: Download all results
    """)