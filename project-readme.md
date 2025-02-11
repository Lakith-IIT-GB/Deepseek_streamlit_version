# Deepseek Chatbot with Document Analysis 🤖

A Streamlit-based chatbot application powered by Ollama and Deepseek-R1 that can analyze various document types and engage in contextual conversations.

## Features

- 💬 Interactive chat interface
- 📄 Support for multiple file formats (PDF, Images, CSV, XLSX, DOCX, PPTX, TXT)
- 💾 Chat history saving and loading
- 🔍 OCR capability for images and scanned PDFs
- 🤖 Powered by Deepseek-R1 (1.5B) running locally via Ollama
- 🚀 One-click launch with batch file automation

## Prerequisites

- Python 3.8+
- Ollama installed with Deepseek-R1 model
- Tesseract OCR installed for image processing

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd deepseek-chatbot
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

3. Install Ollama and pull the Deepseek-R1 model:
```bash
# Install Ollama from https://ollama.ai
ollama pull deepseek-r1:1.5b
```

4. Install Tesseract OCR:
- For Ubuntu/Debian:
  ```bash
  sudo apt-get install tesseract-ocr
  ```
- For macOS:
  ```bash
  brew install tesseract
  ```
- For Windows:
  Download and install from [GitHub Tesseract releases](https://github.com/UB-Mannheim/tesseract/wiki)

## Quick Launch Setup

### Creating the Batch File

1. Create a new text file and name it `run_chatbot.bat`
2. Add the following content:
```batch
@echo off
streamlit run "PATH_TO_YOUR_PYTHON_FILE"
```
Replace `PATH_TO_YOUR_PYTHON_FILE` with your actual file path (e.g., `C:\Users\username\Desktop\Deepseek_streamlit_version\Streamlit_ui\app.py`)

### Creating a Shortcut

1. Right-click on the batch file and select "Create shortcut"
2. Move the shortcut to your desired location (desktop, start menu, etc.)
3. (Optional) Customize the shortcut:
   - Right-click the shortcut and select "Properties"
   - Change the icon if desired
   - Set "Run" to "Minimized" if you don't want to see the command window

Now you can launch the chatbot with a single click!

## Manual Usage

If you prefer to run the application manually:

1. Start the Ollama server:
```bash
ollama serve
```

2. Run the Streamlit application:
```bash
streamlit run app.py
```

3. Open your browser and navigate to `http://localhost:8501`

## Project Structure

```
deepseek-chatbot/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── run_chatbot.bat       # Quick launch batch file
├── saved_chats/          # Directory for saved chat histories
└── temp_files/           # Temporary directory for file processing
```

## Contributing

Feel free to open issues or submit pull requests for any improvements.

## License

[Your chosen license]

## Acknowledgments

- Ollama team for the local LLM runtime
- Deepseek AI for the language model
- Streamlit team for the web framework
