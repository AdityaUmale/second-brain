#!/usr/bin/env python3
"""
Test script for the web UI
Run this to verify the web UI works independently
"""

from web_ui import WebChatUI
import time

def mock_query_handler(query: str) -> str:
    """Mock query handler that simulates RAG response"""
    print(f"\n[Test Handler] Received query: {query}")
    time.sleep(1)  # Simulate processing
    response = f"This is a test response to your question: '{query}'\n\nThe system is working correctly!"
    print(f"[Test Handler] Returning response: {response}")
    return response

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Testing Web UI")
    print("=" * 60)
    
    # Create UI with test callback
    ui = WebChatUI(on_query_callback=mock_query_handler, port=5555)
    ui.ensure_templates_dir()
    
    print("\n✅ Templates directory created/verified")
    
    # Start server
    ui.start_server()
    print("✅ Flask server started on http://127.0.0.1:5555")
    
    # Open browser
    ui.open_browser()
    print("✅ Browser opened")
    
    print("\n" + "=" * 60)
    print("🎉 Web UI is running!")
    print("=" * 60)
    print("\nTry typing a question and clicking Send.")
    print("Watch this terminal for debug logs.")
    print("\nPress Ctrl+C to stop")
    print("=" * 60 + "\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 Stopping test server...")

