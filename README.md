# 🧠 Second Brain - RAG Menu Bar App

A macOS menu bar application that captures screenshots, extracts text via OCR, stores it in a vector database, and provides a floating AI chat interface for querying your knowledge base.

## Features

- 📸 **Screenshot Capture**: Capture full screen or regions with OCR text extraction
- 💾 **Vector Storage**: Store extracted text in Qdrant vector database
- 🤖 **AI Chat Interface**: Query your knowledge base using Llama 3.1 via Ollama
- 🎯 **Floating UI**: Always-on-top chat window accessible from any application
- 🍎 **macOS Native**: Menu bar integration for seamless workflow

## Prerequisites

Before running the app, make sure you have:

1. **Python 3.9+** installed
2. **Tesseract OCR** installed:
   ```bash
   brew install tesseract
   ```

3. **Ollama** installed with Llama 3.1:
   ```bash
   brew install ollama
   ollama pull llama3.1:8b
   ```

4. **Qdrant** running (via Docker):
   ```bash
   docker-compose up -d
   ```

## Installation

1. Clone or navigate to the project directory:
   ```bash
   cd /Users/adityaumale/Desktop/second-brain
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Menu Bar App

1. Start Qdrant (if not already running):
   ```bash
   docker-compose up -d
   ```

2. Start Ollama (if not already running):
   ```bash
   ollama serve
   ```

3. Run the menu bar application:
   ```bash
   python menubar_app.py
   ```

4. You'll see a 🧠 icon in your macOS menu bar. Click it to access:
   - **Toggle Chat Window**: Open/close the floating AI chat interface
   - **Capture Full Screen**: Take a screenshot and extract text
   - **Database Stats**: View stored knowledge statistics
   - **Clear Database**: Remove all stored knowledge

### Using the Floating Chat UI

1. Click "💬 Toggle Chat Window" from the menu bar
2. A floating window will appear that stays on top of all applications
3. Type your questions and press Enter (or click Send)
4. The AI will answer based on your stored knowledge

### Keyboard Shortcuts

- **Enter**: Send query
- **Shift+Enter**: New line in query input

## Project Structure

```
second-brain/
├── menubar_app.py      # Main menu bar application
├── floating_ui.py      # Floating chat window UI
├── vector_db.py        # Qdrant vector database wrapper
├── ocr.py              # Screenshot capture and OCR
├── main_rag.py         # Original RAG logic (reference)
├── requirements.txt    # Python dependencies
├── docker-compose.yml  # Qdrant database setup
└── qdrant_storage/     # Qdrant data directory
```

## How It Works

1. **Capture**: Take screenshots and extract text using Tesseract OCR
2. **Embed**: Convert text to vectors using sentence-transformers
3. **Store**: Save vectors in Qdrant vector database
4. **Query**: Use LangChain + Ollama to answer questions with RAG
5. **Interface**: Interact via floating UI or menu bar

## Configuration

### Changing the LLM Model

Edit `menubar_app.py` line 63:
```python
self.llm = OllamaLLM(model="llama3.1:8b")  # Change to your preferred model
```

### Changing the Embedding Model

Edit `menubar_app.py` line 66 and `vector_db.py` line 19:
```python
self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
```

### Qdrant Connection

Edit `vector_db.py` line 10:
```python
def __init__(self, host="localhost", port=6333, collection_name="book_knowledge"):
```

## Troubleshooting

### "System is still initializing"
Wait a few seconds after launching the app. The models take time to load.

### "No module named 'rumps'"
Make sure you activated the virtual environment:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Tesseract not found
Install Tesseract and verify the path in `ocr.py`:
```bash
brew install tesseract
which tesseract  # Should show /opt/homebrew/bin/tesseract
```

### Qdrant connection error
Ensure Qdrant is running:
```bash
docker-compose up -d
docker-compose ps  # Should show qdrant running
```

### Ollama not responding
Start Ollama service:
```bash
ollama serve
```

## Tips

- **Capture before querying**: The AI can only answer based on captured knowledge
- **Use full sentences**: Better questions get better answers
- **Clear periodically**: Use "Clear Database" to remove old/irrelevant content
- **Check stats**: Monitor how much knowledge is stored

## License

MIT License - Feel free to modify and use!

