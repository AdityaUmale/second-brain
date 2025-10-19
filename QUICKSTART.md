# 🚀 Quick Start Guide

## The Problem We Fixed

Your original setup used `tkinter` for the floating UI, but `tkinter` and `rumps` (macOS menu bar framework) can't work together—they both want exclusive control of the GUI event loop. This caused the fatal GIL error you saw.

## The Solution

We replaced the tkinter UI with a **web-based interface** that opens in your browser. This is actually better because:
- ✅ No threading conflicts
- ✅ Works with rumps perfectly  
- ✅ Better UI/UX with modern web technologies
- ✅ Can access from any device on your network

## Installation Steps

### 1. Install New Packages

```bash
cd /Users/adityaumale/Desktop/second-brain
source venv/bin/activate
pip install flask flask-cors langchain-huggingface langchain-ollama
```

### 2. Make Sure Prerequisites Are Running

**Start Qdrant:**
```bash
docker-compose up -d
```

**Start Ollama (in a separate terminal):**
```bash
ollama serve
```

### 3. Run the App

```bash
python menubar_app.py
```

You should see:
1. A 🧠 brain icon appear in your macOS menu bar
2. A notification saying "Initializing..."
3. Another notification saying "Ready! 🎉"

## How to Use

### Capturing Screenshots

1. **Click the 🧠 icon** in your menu bar
2. Select **"📸 Capture Full Screen"**
3. Wait 2-3 seconds for OCR processing
4. You'll get a notification showing how many characters were captured

**Tip:** Make sure there's readable text on your screen before capturing!

### Asking Questions

1. **Click the 🧠 icon** in your menu bar
2. Select **"💬 Open Chat Window"**
3. A browser window will open with the chat interface
4. Type your question and press Enter
5. The AI will search your captured knowledge and answer

## Menu Options

- **💬 Open Chat Window** - Opens the web chat interface in your browser
- **📸 Capture Full Screen** - Takes screenshot, extracts text via OCR, stores in DB
- **📸 Capture Region** - Coming soon
- **⚙️ Settings** - Configure auto-store behavior
- **📊 Database Stats** - View how much knowledge is stored
- **🗑️ Clear Database** - Delete all stored knowledge
- **❌ Quit** - Exit the application

## Troubleshooting

### "System is still initializing"
The app takes 10-15 seconds to load models on first run. Wait for the "Ready! 🎉" notification.

### No notification when capturing
Check that you're capturing a screen with actual text. Try opening a text document first, then capture.

### Browser doesn't open automatically
Manually go to: http://127.0.0.1:5555

### Port 5555 already in use
Edit `menubar_app.py` line 98 and change the port:
```python
self.web_ui = WebChatUI(on_query_callback=self.handle_query, port=5556)
```

### Chat says "No query callback configured"
The system is still initializing. Wait a bit longer.

## Testing the Full Workflow

1. **Open a text document** or webpage with readable text
2. **Capture it**: 🧠 → 📸 Capture Full Screen
3. **Wait for confirmation** notification
4. **Open chat**: 🧠 → 💬 Open Chat Window  
5. **Ask a question** about what you captured
6. **Get your answer!** The AI will cite sources

## What Changed From Before

| Old (tkinter) | New (Web UI) |
|--------------|-------------|
| ❌ Crashed with GIL error | ✅ Works perfectly |
| Toggle window show/hide | Opens in browser |
| Native window | Modern web interface |
| Threading conflicts | No conflicts |

## File Structure

```
second-brain/
├── menubar_app.py       # Main app (UPDATED)
├── web_ui.py            # New web-based UI
├── templates/
│   └── chat.html        # Auto-generated chat interface
├── vector_db.py         # Vector DB (unchanged)
├── ocr.py               # OCR logic (unchanged)
└── requirements.txt     # Updated dependencies
```

## Next Steps

Want to improve it? Here are ideas:
- Add keyboard shortcuts for capturing
- Implement region selection for captures
- Add dark/light theme toggle
- Save chat history to disk
- Export captured knowledge to markdown
- Add image display in chat
- Multi-collection support

Enjoy your Second Brain! 🧠✨

