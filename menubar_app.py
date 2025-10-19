#!/usr/bin/env python3
"""
Second Brain - macOS Menu Bar Application
Integrates OCR, Vector DB, and RAG with a floating UI
"""

import rumps
import threading
from typing import Optional
from vector_db import VectorDatabase
from ocr import capture_and_extract
from web_ui import WebChatUI
from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Qdrant


class SecondBrainApp(rumps.App):
    """Main menu bar application for Second Brain"""
    
    def __init__(self):
        super(SecondBrainApp, self).__init__(
            "🧠",  # Menu bar icon
            title="Second Brain",
            quit_button=None  # We'll add a custom quit button
        )
        
        # Initialize components
        self.vector_db: Optional[VectorDatabase] = None
        self.llm: Optional[OllamaLLM] = None
        self.qa_chain: Optional[RetrievalQA] = None
        self.web_ui: Optional[WebChatUI] = None
        self.embeddings: Optional[HuggingFaceEmbeddings] = None
        
        # Capture settings
        self.auto_store = True  # Auto-store captured text
        
        # Setup menu items
        self.setup_menu()
        
        # Initialize in background to avoid blocking UI
        threading.Thread(target=self.initialize_components, daemon=True).start()
        
    def setup_menu(self):
        """Setup the menu bar menu items"""
        
        # Capture section
        self.menu = [
            "💬 Open Chat Window",
            None,  # Separator
            "📸 Capture Full Screen",
            "📸 Capture Region",  # TODO: implement region selection
            None,
            "⚙️ Settings",
            None,
            "📊 Database Stats",
            "🗑️  Clear Database",
            None,
            "❌ Quit"
        ]
        
    def initialize_components(self):
        """Initialize vector DB, LLM, and floating UI"""
        try:
            rumps.notification(
                title="Second Brain",
                subtitle="Initializing...",
                message="Loading models and connecting to database..."
            )
            
            # Initialize Vector DB
            self.vector_db = VectorDatabase(collection_name="book_knowledge")
            
            # Initialize LLM
            self.llm = OllamaLLM(model="llama3.1:8b")
            
            # Initialize embeddings (same model as VectorDB)
            self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            
            # Create LangChain wrapper with retriever
            vector_store = Qdrant(
                client=self.vector_db.client,
                collection_name="book_knowledge",
                embeddings=self.embeddings,
                content_payload_key="text"
            )
            retriever = vector_store.as_retriever(search_kwargs={"k": 3})
            
            # Create QA chain
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                retriever=retriever,
                return_source_documents=True
            )
            
            # Initialize web UI with query callback
            self.web_ui = WebChatUI(on_query_callback=self.handle_query, port=5555)
            self.web_ui.ensure_templates_dir()
            self.web_ui.start_server()
            
            rumps.notification(
                title="Second Brain",
                subtitle="Ready! 🎉",
                message="All systems initialized. Click the brain icon to get started."
            )
            
        except Exception as e:
            rumps.notification(
                title="Second Brain",
                subtitle="Initialization Error",
                message=f"Failed to initialize: {str(e)}"
            )
            print(f"Initialization error: {e}")
    
    @rumps.clicked("💬 Open Chat Window")
    def open_chat(self, _):
        """Open the web-based chat window in browser"""
        if not self.web_ui:
            rumps.alert(
                title="Not Ready",
                message="System is still initializing. Please wait a moment.",
                ok="OK"
            )
            return
        
        # Open browser window
        self.web_ui.open_browser()
    
    @rumps.clicked("📸 Capture Full Screen")
    def capture_full_screen(self, _):
        """Capture full screen, extract text, and store in vector DB"""
        if not self.vector_db:
            rumps.alert(
                title="Not Ready",
                message="Vector database is still initializing.",
                ok="OK"
            )
            return
        
        # Show notification
        rumps.notification(
            title="Second Brain",
            subtitle="Capturing Screenshot",
            message="Extracting text from screen..."
        )
        
        # Run capture in background thread
        def capture_and_store():
            try:
                # Capture and extract
                text = capture_and_extract(region=None)
                
                if not text or len(text.strip()) < 10:
                    rumps.notification(
                        title="Second Brain",
                        subtitle="No Text Found",
                        message="Could not extract meaningful text from the screenshot."
                    )
                    return
                
                # Store in vector DB
                self.vector_db.add_text(text, metadata={"source": "screenshot_full"})
                
                # Show success notification
                rumps.notification(
                    title="Second Brain",
                    subtitle="Text Captured! ✅",
                    message=f"Stored {len(text)} characters in knowledge base."
                )
                
                # Add system message to chat UI
                if self.web_ui:
                    self.web_ui.add_system_message(
                        f"Captured and stored {len(text)} characters from screenshot"
                    )
                
            except Exception as e:
                rumps.notification(
                    title="Second Brain",
                    subtitle="Capture Failed",
                    message=f"Error: {str(e)}"
                )
                print(f"Capture error: {e}")
        
        threading.Thread(target=capture_and_store, daemon=True).start()
    
    @rumps.clicked("📸 Capture Region")
    def capture_region(self, _):
        """Capture a specific region (placeholder for now)"""
        rumps.alert(
            title="Capture Region",
            message="Region selection coming soon! For now, use 'Capture Full Screen'.",
            ok="OK"
        )
    
    @rumps.clicked("⚙️ Settings")
    def show_settings(self, _):
        """Show settings dialog"""
        response = rumps.alert(
            title="Settings",
            message="Auto-store captured text in database?",
            ok="Yes",
            cancel="No"
        )
        
        if response == 1:
            self.auto_store = True
            rumps.notification(
                title="Settings Updated",
                subtitle="Auto-store enabled",
                message="Captured text will be automatically stored."
            )
        else:
            self.auto_store = False
            rumps.notification(
                title="Settings Updated",
                subtitle="Auto-store disabled",
                message="You'll be prompted before storing text."
            )
    
    @rumps.clicked("📊 Database Stats")
    def show_stats(self, _):
        """Show database statistics"""
        if not self.vector_db:
            rumps.alert(
                title="Not Ready",
                message="Vector database is still initializing.",
                ok="OK"
            )
            return
        
        try:
            stats = self.vector_db.get_stats()
            
            message = f"""
Total Documents: {stats['total_points']}
Vectors Count: {stats['vectors_count']}
Status: {stats['status']}
            """
            
            rumps.alert(
                title="Database Statistics",
                message=message.strip(),
                ok="OK"
            )
        except Exception as e:
            rumps.alert(
                title="Error",
                message=f"Could not fetch stats: {str(e)}",
                ok="OK"
            )
    
    @rumps.clicked("🗑️  Clear Database")
    def clear_database(self, _):
        """Clear all data from the database"""
        if not self.vector_db:
            rumps.alert(
                title="Not Ready",
                message="Vector database is still initializing.",
                ok="OK"
            )
            return
        
        response = rumps.alert(
            title="Clear Database",
            message="Are you sure you want to delete all stored knowledge? This cannot be undone!",
            ok="Delete All",
            cancel="Cancel"
        )
        
        if response == 1:
            try:
                self.vector_db.delete_collection()
                # Recreate the collection
                self.vector_db._create_collection_if_not_exists()
                
                rumps.notification(
                    title="Second Brain",
                    subtitle="Database Cleared",
                    message="All knowledge has been removed."
                )
            except Exception as e:
                rumps.alert(
                    title="Error",
                    message=f"Could not clear database: {str(e)}",
                    ok="OK"
                )
    
    @rumps.clicked("❌ Quit")
    def quit_app(self, _):
        """Quit the application"""
        response = rumps.alert(
            title="Quit Second Brain",
            message="Are you sure you want to quit?",
            ok="Quit",
            cancel="Cancel"
        )
        
        if response == 1:
            # Clean up (web server will auto-stop as daemon thread)
            rumps.quit_application()
    
    def handle_query(self, query: str) -> str:
        """
        Handle a query from the floating UI
        
        Args:
            query: User's question
            
        Returns:
            Response text from the RAG system
        """
        try:
            if not self.qa_chain:
                return "❌ RAG system is not initialized yet. Please wait..."
            
            # Use the QA chain to get an answer
            response = self.qa_chain.invoke({"query": query})
            
            # Format the response
            answer = response['result']
            
            # Optionally include source documents
            if response.get('source_documents'):
                answer += "\n\n📚 Sources:\n"
                for i, doc in enumerate(response['source_documents'][:2], 1):
                    snippet = doc.page_content[:150].replace('\n', ' ')
                    answer += f"\n{i}. {snippet}..."
            
            return answer
            
        except Exception as e:
            return f"❌ Error processing query: {str(e)}"


def main():
    """Main entry point"""
    app = SecondBrainApp()
    app.run()


if __name__ == "__main__":
    main()

