# 🚀 Quick Start Guide - Second Brain Swift App

Get up and running in 3 simple steps!

## ⚡ Prerequisites Check

Before starting, ensure you have:

- [x] Python 3.8+ installed
- [x] Docker installed and running
- [x] Ollama installed with `llama3.1:8b` model
- [x] Xcode 15.0+ installed (from Mac App Store)
- [x] Tesseract OCR installed: `brew install tesseract`

## 📦 Step 1: Start the Python Backend

Open a terminal and run:

```bash
cd /Users/adityaumale/Desktop/second-brain
./start_backend.sh
```

Wait until you see:
```
✅ Backend initialization complete!
 * Running on http://127.0.0.1:5555
```

**Keep this terminal window open!** The backend needs to stay running.

## 🎨 Step 2: Build & Run the Swift App

### Option A: Quick Build (Command Line)

In a **new terminal window**:

```bash
cd /Users/adityaumale/Desktop/second-brain
./build_swift_app.sh
```

Then run:
```bash
open SecondBrainApp/build/Build/Products/Release/SecondBrainApp.app
```

### Option B: Development Mode (Xcode)

```bash
open SecondBrainApp/SecondBrainApp.xcodeproj
```

Then press **⌘R** to run.

## 🎉 Step 3: Start Using!

Once the app launches:

1. Look for the **🧠** icon in your menu bar (top right)
2. Click it and select **"💬 Open Chat"** (or press ⌘C)
3. A floating chat window will appear!
4. Start asking questions or capture some text first

### Try These Commands:

1. **Capture Screen**: 
   - Click 🧠 → "📸 Capture Screen"
   - Your screen will be captured and text extracted

2. **Ask Questions**:
   - Type in the floating chat window
   - Press Enter to send

3. **View Stats**:
   - Click 🧠 → "📊 Database Stats"

## 🔍 Troubleshooting

### "Backend not ready" message
- Check that `start_backend.sh` is still running
- Visit http://127.0.0.1:5555/api/health in your browser
- Should show: `{"initialized": true, ...}`

### Build fails
```bash
# Clean and rebuild
cd SecondBrainApp
xcodebuild clean -project SecondBrainApp.xcodeproj
cd ..
./build_swift_app.sh
```

### Floating window doesn't appear
- Check System Preferences → Privacy & Security
- Look for "SecondBrainApp" and grant permissions if prompted

## 🎯 What's Different from the Python Version?

| Feature | Python (rumps) | Swift (Native) |
|---------|---------------|----------------|
| Floating Window | ❌ Opens in browser | ✅ True floating window |
| Stay on Top | ❌ No | ✅ Yes, always visible |
| Native Feel | ⚠️ Web-based | ✅ 100% native macOS |
| Performance | ⚠️ Good | ✅ Excellent |
| Window Management | ❌ Poor | ✅ Perfect |
| Dark Mode | ⚠️ Manual | ✅ Automatic |

## 🎨 Cool Features to Try

### 1. Floating Chat
- The chat window stays on top of **all** your apps
- Work in any app while keeping chat visible
- Resize and position anywhere on screen

### 2. Quick Access
- Press **⌘C** from anywhere to open chat
- Menu bar always accessible
- No Dock icon clutter!

### 3. Screen Capture
- Capture any text on screen
- Automatically stored in vector DB
- Query it instantly in chat

## 📁 File Structure

```
second-brain/
├── api_backend.py           # Python API server (Flask)
├── start_backend.sh         # Start Python backend
├── build_swift_app.sh       # Build Swift app
├── SecondBrainApp/          # Swift app source
│   ├── SecondBrainApp.xcodeproj
│   └── SecondBrainApp/
│       ├── SecondBrainAppApp.swift
│       ├── MenuBarManager.swift
│       ├── FloatingWindow.swift
│       ├── ChatView.swift
│       └── APIClient.swift
├── vector_db.py             # Vector database
├── ocr.py                   # OCR processing
└── requirements.txt         # Python dependencies
```

## 💡 Pro Tips

1. **Keep chat always visible**: Perfect for research while reading documents
2. **Capture as you browse**: Grab interesting text from any app
3. **Ask contextual questions**: The RAG system finds relevant info automatically
4. **Keyboard shortcuts**: Learn ⌘C (chat) and ⌘S (capture) for speed

## 🆘 Need Help?

- Check `README_SWIFT.md` for detailed documentation
- Ensure both terminals (backend + app) are running
- Restart both if things get weird

## 🎊 You're All Set!

Enjoy your native macOS Second Brain experience! 🧠✨

