# --- Streamlit Configuration MUST BE FIRST ---
import streamlit as st
st.set_page_config(
    page_title="Deepseek Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Standard Library Imports ---
import requests
import json
import os
import logging
import numpy as np

# --- File Processing Imports ---
from PyPDF2 import PdfReader
import pandas as pd
import pytesseract
from PIL import Image
from docx import Document
from pptx import Presentation
from openpyxl import load_workbook
from pdf2image import convert_from_path
import fitz  # PyMuPDF

# --- ML/NLP Imports ---
import faiss
import nltk
from sentence_transformers import SentenceTransformer

# --- Initial Configurations ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
nltk.download('punkt', quiet=True)

# --- Platform-Specific Configuration ---
if os.name == 'nt':  # Windows only
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
else:  # Linux/Streamlit Cloud
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# --- Core Functions ---
def categorize_file(file_path):
    """Determine the file type based on extension."""
    extension = os.path.splitext(file_path)[1].lower()
    return {
        '.jpg': 'image', '.jpeg': 'image', '.png': 'image',
        '.gif': 'image', '.bmp': 'image', '.pdf': 'pdf',
        '.csv': 'csv', '.xlsx': 'xlsx', '.pptx': 'pptx',
        '.docx': 'docx', '.txt': 'text', '.md': 'text'
    }.get(extension, 'unknown')

def process_office_file(file_path):
    """Process PPTX/DOCX files for Linux compatibility"""
    file_type = categorize_file(file_path)
    content = []
    
    try:
        if file_type == 'pptx':
            prs = Presentation(file_path)
            return "\n".join([shape.text for slide in prs.slides for shape in slide.shapes if shape.has_text_frame])
        
        if file_type == 'docx':
            doc = Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
            
    except Exception as e:
        logging.error(f"Office processing error: {e}")
    return "Could not extract content"

def process_file(file_path):
    """Process different file types."""
    if not os.path.exists(file_path):
        return None
    
    file_type = categorize_file(file_path)
    
    try:
        if file_type == 'image':
            return pytesseract.image_to_string(Image.open(file_path))
        elif file_type == 'pdf':
            return process_pdf(file_path)
        elif file_type == 'csv':
            return pd.read_csv(file_path).to_string()
        elif file_type == 'xlsx':
            return pd.read_excel(file_path).to_string()
        elif file_type in ['pptx', 'docx']:
            return process_office_file(file_path)
        elif file_type == 'text':
            with open(file_path, 'r') as f:
                return f.read()
    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}")
        return None

def process_pdf(file_path):
    """Extract text from PDF using PyMuPDF."""
    text = ""
    try:
        with fitz.open(file_path) as pdf:
            text = "".join([page.get_text() for page in pdf])
        if not text.strip():  # Fallback to OCR
            images = convert_from_path(file_path)
            text = " ".join([pytesseract.image_to_string(img) for img in images])
    except Exception as e:
        logging.error(f"PDF processing error: {e}")
    return text

def send_request(prompt, file_path=None):
    """Send request to Ollama API."""
    api_url = "http://localhost:11434/api/generate"
    
    if file_path:
        content = process_file(file_path)
        if content:
            prompt += f"\n\nFile Content:\n{content[:3000]}"  # Limit context length
    
    try:
        response = requests.post(
            api_url,
            json={"model": "deepseek-r1:1.5b", "prompt": prompt, "stream": False},
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        return response.json().get('response', 'No response generated')
    except Exception as e:
        logging.error(f"API Error: {e}")
        return "Failed to get response from API"

# --- Streamlit UI Components ---
st.title("Deepseek Chatbot 💬")
st.caption("Powered by Ollama - Upload documents for contextual understanding")

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# Sidebar for file upload
with st.sidebar:
    st.header("Document Upload")
    uploaded_files = st.file_uploader(
        "Choose files (PDF, Images, Docs, Sheets)",
        type=["pdf", "png", "jpg", "jpeg", "csv", "xlsx", "docx", "pptx", "txt"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files
        st.success(f"{len(uploaded_files)} file(s) ready for analysis!")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Process files
    responses = []
    temp_dir = "temp_files"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Generate responses
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Handle file-based queries
        if st.session_state.uploaded_files:
            for file in st.session_state.uploaded_files:
                file_path = os.path.join(temp_dir, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getvalue())
                
                try:
                    response = send_request(prompt, file_path)
                    full_response += f"**{file.name} Analysis:**\n{response}\n\n"
                except Exception as e:
                    full_response += f"⚠️ Error processing {file.name}: {str(e)}\n"
                finally:
                    if os.path.exists(file_path):
                        os.remove(file_path)
        
        # Handle general queries
        else:
            response = send_request(prompt)
            full_response = response
        
        response_placeholder.markdown(full_response)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
