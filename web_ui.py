"""
Web-based floating UI for Second Brain
Uses Flask to serve a chat interface that opens in a browser window
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import threading
import webbrowser
import time
import os
from typing import Callable, Optional

class WebChatUI:
    """Web-based chat UI that runs in browser"""
    
    def __init__(self, on_query_callback: Optional[Callable] = None, port: int = 5555):
        """
        Initialize the web chat UI
        
        Args:
            on_query_callback: Function to call when user submits a query
            port: Port to run the Flask server on
        """
        self.on_query_callback = on_query_callback
        self.port = port
        self.app = Flask(__name__)
        CORS(self.app)
        
        self.server_thread = None
        self.is_running = False
        self.chat_history = []
        
        self._setup_routes()
        
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            """Serve the main chat interface"""
            return render_template('chat.html')
        
        @self.app.route('/favicon.ico')
        def favicon():
            """Return empty favicon to prevent 404"""
            return '', 204
        
        @self.app.route('/api/query', methods=['POST'])
        def query():
            """Handle query requests"""
            print(f"[API] Received query request")  # Debug log
            data = request.json
            user_query = data.get('query', '')
            print(f"[API] Query text: {user_query}")  # Debug log
            
            if not user_query:
                return jsonify({'error': 'No query provided'}), 400
            
            # Add user message to history
            self.chat_history.append({
                'role': 'user',
                'content': user_query
            })
            
            try:
                if self.on_query_callback:
                    print(f"[API] Calling query callback...")  # Debug log
                    response = self.on_query_callback(user_query)
                    print(f"[API] Got response: {response[:100]}...")  # Debug log
                else:
                    response = "No query callback configured."
                    print(f"[API] No callback configured!")  # Debug log
                
                # Add assistant response to history
                self.chat_history.append({
                    'role': 'assistant',
                    'content': response
                })
                
                return jsonify({
                    'response': response,
                    'success': True
                })
                
            except Exception as e:
                print(f"[API] Error processing query: {e}")  # Debug log
                import traceback
                traceback.print_exc()
                error_msg = f"Error: {str(e)}"
                self.chat_history.append({
                    'role': 'system',
                    'content': error_msg
                })
                return jsonify({
                    'response': error_msg,
                    'success': False
                }), 500
        
        @self.app.route('/api/history', methods=['GET'])
        def get_history():
            """Get chat history"""
            return jsonify({'history': self.chat_history})
        
        @self.app.route('/api/clear', methods=['POST'])
        def clear_history():
            """Clear chat history"""
            self.chat_history = []
            return jsonify({'success': True})
        
        @self.app.route('/api/system-message', methods=['POST'])
        def add_system_message():
            """Add a system message"""
            data = request.json
            message = data.get('message', '')
            
            if message:
                self.chat_history.append({
                    'role': 'system',
                    'content': message
                })
            
            return jsonify({'success': True})
    
    def add_system_message(self, message: str):
        """Add a system message to chat history"""
        self.chat_history.append({
            'role': 'system',
            'content': message
        })
    
    def start_server(self):
        """Start the Flask server in a background thread"""
        if self.is_running:
            return
        
        def run_server():
            # Disable Flask's startup messages
            import logging
            log = logging.getLogger('werkzeug')
            log.setLevel(logging.ERROR)
            
            self.app.run(host='127.0.0.1', port=self.port, debug=False, use_reloader=False)
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        self.is_running = True
        
        # Give server time to start
        time.sleep(1)
    
    def open_browser(self):
        """Open the chat UI in default browser"""
        if not self.is_running:
            self.start_server()
        
        url = f'http://127.0.0.1:{self.port}'
        webbrowser.open(url)
    
    def ensure_templates_dir(self):
        """Create templates directory and HTML file if they don't exist"""
        templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        os.makedirs(templates_dir, exist_ok=True)
        
        html_path = os.path.join(templates_dir, 'chat.html')
        
        if not os.path.exists(html_path):
            html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 Second Brain</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
            color: #ffffff;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            background: #1a1a1a;
            padding: 20px;
            text-align: center;
            border-bottom: 2px solid #4a9eff;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        
        .header h1 {
            font-size: 24px;
            font-weight: 600;
        }
        
        .chat-container {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .message {
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 12px;
            line-height: 1.5;
            animation: fadeIn 0.3s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .message.user {
            background: #4a9eff;
            align-self: flex-end;
            margin-left: auto;
        }
        
        .message.assistant {
            background: #50fa7b;
            color: #1e1e1e;
            align-self: flex-start;
        }
        
        .message.system {
            background: #ff79c6;
            color: #1e1e1e;
            align-self: center;
            font-style: italic;
            font-size: 14px;
            max-width: 90%;
        }
        
        .message-label {
            font-weight: bold;
            margin-bottom: 5px;
            font-size: 12px;
            opacity: 0.8;
        }
        
        .input-container {
            background: #1a1a1a;
            padding: 20px;
            border-top: 2px solid #4a9eff;
            display: flex;
            gap: 10px;
            align-items: flex-end;
        }
        
        #queryInput {
            flex: 1;
            background: #2d2d2d;
            border: 2px solid #3d3d3d;
            color: #ffffff;
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 14px;
            resize: none;
            min-height: 50px;
            max-height: 150px;
            font-family: inherit;
        }
        
        #queryInput:focus {
            outline: none;
            border-color: #4a9eff;
        }
        
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .btn-primary {
            background: #4a9eff;
            color: white;
        }
        
        .btn-secondary {
            background: #6272a4;
            color: white;
        }
        
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .status {
            text-align: center;
            padding: 10px;
            font-size: 12px;
            color: #888;
        }
        
        .loading {
            display: inline-block;
            width: 12px;
            height: 12px;
            border: 2px solid #888;
            border-top-color: #4a9eff;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #1a1a1a;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #4a9eff;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 Second Brain - RAG Assistant</h1>
    </div>
    
    <div class="chat-container" id="chatContainer">
        <div class="message system">
            Welcome! Ask questions about your captured knowledge.
        </div>
    </div>
    
    <div class="status" id="status">Ready</div>
    
    <div class="input-container">
        <textarea id="queryInput" placeholder="Ask a question... (Press Enter to send, Shift+Enter for new line)"></textarea>
        <button class="btn btn-secondary" onclick="clearChat()">Clear</button>
        <button class="btn btn-primary" onclick="sendQuery()" id="sendBtn">Send</button>
    </div>
    
    <script>
        const chatContainer = document.getElementById('chatContainer');
        const queryInput = document.getElementById('queryInput');
        const sendBtn = document.getElementById('sendBtn');
        const status = document.getElementById('status');
        
        // Load chat history on page load
        window.addEventListener('load', loadHistory);
        
        // Handle Enter key
        queryInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendQuery();
            }
        });
        
        async function loadHistory() {
            try {
                const response = await fetch('/api/history');
                const data = await response.json();
                
                data.history.forEach(msg => {
                    addMessageToUI(msg.role, msg.content);
                });
            } catch (error) {
                console.error('Error loading history:', error);
            }
        }
        
        async function sendQuery() {
            const query = queryInput.value.trim();
            if (!query) return;
            
            // Add user message
            addMessageToUI('user', query);
            queryInput.value = '';
            
            // Disable send button
            sendBtn.disabled = true;
            sendBtn.textContent = 'Thinking...';
            status.innerHTML = '<span class="loading"></span> Processing query...';
            
            try {
                const response = await fetch('/api/query', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ query })
                });
                
                const data = await response.json();
                
                // Add assistant response
                addMessageToUI('assistant', data.response);
                
            } catch (error) {
                addMessageToUI('system', `Error: ${error.message}`);
            } finally {
                sendBtn.disabled = false;
                sendBtn.textContent = 'Send';
                status.textContent = 'Ready';
            }
        }
        
        function addMessageToUI(role, content) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${role}`;
            
            // Convert newlines to <br> for display
            const formattedContent = content.replace(/\\n/g, '<br>');
            messageDiv.innerHTML = formattedContent;
            
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        async function clearChat() {
            if (!confirm('Clear all chat history?')) return;
            
            try {
                await fetch('/api/clear', { method: 'POST' });
                chatContainer.innerHTML = '<div class="message system">Chat history cleared</div>';
            } catch (error) {
                console.error('Error clearing chat:', error);
            }
        }
    </script>
</body>
</html>'''
            
            with open(html_path, 'w') as f:
                f.write(html_content)


# Test the UI
if __name__ == "__main__":
    def mock_query_handler(query: str) -> str:
        """Mock query handler for testing"""
        import time
        time.sleep(1)
        return f"This is a mock response to: '{query}'"
    
    ui = WebChatUI(on_query_callback=mock_query_handler)
    ui.ensure_templates_dir()
    ui.start_server()
    ui.open_browser()
    
    print("Web UI running at http://127.0.0.1:5555")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")

