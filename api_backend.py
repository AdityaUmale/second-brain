#!/usr/bin/env python3
"""
Second Brain API Backend
Flask API service that the Swift menubar app will communicate with
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
from typing import Optional
from vector_db import VectorDatabase
from ocr import capture_and_extract
from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Qdrant

app = Flask(__name__)
CORS(app)

# Global state
vector_db: Optional[VectorDatabase] = None
llm: Optional[OllamaLLM] = None
qa_chain: Optional[RetrievalQA] = None
embeddings: Optional[HuggingFaceEmbeddings] = None
initialization_status = {"ready": False, "message": "Initializing..."}
chat_history = []


def initialize_components():
    """Initialize vector DB, LLM, and RAG chain"""
    global vector_db, llm, qa_chain, embeddings, initialization_status
    
    try:
        print("🚀 Initializing Second Brain backend...")
        
        # Initialize Vector DB
        print("📦 Loading Vector Database...")
        vector_db = VectorDatabase(collection_name="book_knowledge")
        
        # Initialize LLM
        print("🤖 Loading LLM (Ollama)...")
        llm = OllamaLLM(model="llama3.1:8b")
        
        # Initialize embeddings
        print("🧮 Loading Embeddings...")
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Create LangChain wrapper with retriever
        print("🔗 Setting up RAG chain...")
        vector_store = Qdrant(
            client=vector_db.client,
            collection_name="book_knowledge",
            embeddings=embeddings,
            content_payload_key="text"
        )
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        
        # Create QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            return_source_documents=True
        )
        
        initialization_status = {"ready": True, "message": "All systems ready! 🎉"}
        print("✅ Backend initialization complete!")
        
    except Exception as e:
        initialization_status = {"ready": False, "message": f"Error: {str(e)}"}
        print(f"❌ Initialization error: {e}")


# Initialize in background
threading.Thread(target=initialize_components, daemon=True).start()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'initialized': initialization_status['ready'],
        'message': initialization_status['message']
    })


@app.route('/api/query', methods=['POST'])
def query():
    """Handle RAG queries"""
    if not initialization_status['ready']:
        return jsonify({
            'error': 'System not ready yet',
            'message': initialization_status['message']
        }), 503
    
    data = request.json
    user_query = data.get('query', '')
    
    if not user_query:
        return jsonify({'error': 'No query provided'}), 400
    
    try:
        # Use the QA chain to get an answer
        response = qa_chain.invoke({"query": user_query})
        
        # Format the response
        answer = response['result']
        
        # Include source documents
        sources = []
        if response.get('source_documents'):
            for doc in response['source_documents'][:2]:
                sources.append({
                    'content': doc.page_content[:150],
                    'metadata': doc.metadata
                })
        
        # Add to chat history
        chat_history.append({'role': 'user', 'content': user_query})
        chat_history.append({'role': 'assistant', 'content': answer})
        
        return jsonify({
            'response': answer,
            'sources': sources,
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500


@app.route('/api/capture/full', methods=['POST'])
def capture_full_screen():
    """Capture full screen and extract text"""
    if not vector_db:
        return jsonify({'error': 'Vector database not ready'}), 503
    
    try:
        # Capture and extract
        text = capture_and_extract(region=None)
        
        if not text or len(text.strip()) < 10:
            return jsonify({
                'success': False,
                'message': 'No meaningful text found'
            })
        
        # Store in vector DB
        vector_db.add_text(text, metadata={"source": "screenshot_full"})
        
        return jsonify({
            'success': True,
            'message': f'Captured {len(text)} characters',
            'text_length': len(text)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get database statistics"""
    if not vector_db:
        return jsonify({'error': 'Vector database not ready'}), 503
    
    try:
        stats = vector_db.get_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get chat history"""
    return jsonify({'history': chat_history})


@app.route('/api/history', methods=['DELETE'])
def clear_history():
    """Clear chat history"""
    global chat_history
    chat_history = []
    return jsonify({'success': True})


@app.route('/api/database', methods=['DELETE'])
def clear_database():
    """Clear the entire database"""
    if not vector_db:
        return jsonify({'error': 'Vector database not ready'}), 503
    
    try:
        vector_db.delete_collection()
        vector_db._create_collection_if_not_exists()
        return jsonify({
            'success': True,
            'message': 'Database cleared'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("=" * 50)
    print("🧠 Second Brain API Backend")
    print("=" * 50)
    print("Starting server on http://127.0.0.1:5555")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    app.run(host='127.0.0.1', port=5555, debug=False)

