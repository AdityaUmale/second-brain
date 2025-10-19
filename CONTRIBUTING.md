# Contributing to Second Brain

## 📦 What to Commit

### ✅ DO Commit
- All Python source files (`*.py`)
- `requirements.txt`
- `docker-compose.yml`
- `templates/` directory (needed for web UI)
- Documentation (`README.md`, `QUICKSTART.md`, etc.)
- `.gitignore` and `.cursorignore`

### ❌ DON'T Commit
- `venv/` - Virtual environment (regenerate with `pip install -r requirements.txt`)
- `qdrant_storage/` - Database data (personal knowledge base)
- `__pycache__/` - Python cache files
- `.DS_Store` - macOS metadata
- `.env` files - May contain sensitive info
- `*.log` - Log files
- Personal screenshots or captures

## 🚀 Setup for New Contributors

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/second-brain.git
cd second-brain

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install prerequisites
brew install tesseract ollama

# Pull LLM model
ollama pull llama3.1:8b

# Start Qdrant
docker-compose up -d

# Run the app
python menubar_app.py
```

## 📝 Before Pushing

1. **Test the app**: Make sure it runs without errors
2. **Check for secrets**: No API keys, passwords, or personal data
3. **Update docs**: If you added features, update README
4. **Clean code**: Remove debug prints and commented code

## 🔒 Security Notes

- Never commit `.env` files
- Don't commit `qdrant_storage/` (contains your personal knowledge)
- Be careful with screenshots that might contain sensitive info
- Keep API keys and credentials out of code

## 📁 File Structure

```
second-brain/
├── menubar_app.py      # Main app - COMMIT
├── web_ui.py           # Web UI logic - COMMIT
├── vector_db.py        # Database wrapper - COMMIT
├── ocr.py              # OCR logic - COMMIT
├── templates/          # HTML templates - COMMIT
│   └── chat.html
├── requirements.txt    # Dependencies - COMMIT
├── docker-compose.yml  # Qdrant setup - COMMIT
├── README.md           # Documentation - COMMIT
├── .gitignore          # Git ignore rules - COMMIT
├── venv/               # Virtual env - DON'T COMMIT
└── qdrant_storage/     # Database - DON'T COMMIT
```

## 🐛 Bug Reports

When reporting bugs, include:
- OS version (macOS version)
- Python version
- Full error message
- Steps to reproduce

## 💡 Feature Requests

Ideas for improvements:
- Keyboard shortcuts for capture
- Multiple knowledge bases
- Export to markdown
- Image OCR from clipboard
- Custom capture regions
- Dark/light theme toggle
- Chat history persistence

