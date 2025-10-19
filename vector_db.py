from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from datetime import datetime
import uuid

class VectorDatabase:
    """Manages connection to Qdrant vector database"""
    
    def __init__(self, host="localhost", port=6333, collection_name="book_knowledge"):
        print("🔌 Connecting to Qdrant...")
        
        # Connect to Qdrant
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        
        # Initialize embedding model
        print("📦 Loading embedding model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Get embedding dimension
        self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()
        
        # Create collection if it doesn't exist
        self._create_collection_if_not_exists()
        
        print(f"✅ Connected to Qdrant!")
        print(f"📊 Collection: {collection_name}")
        print(f"📏 Embedding dimension: {self.embedding_dim}")
    
    def _create_collection_if_not_exists(self):
        """Create collection if it doesn't exist"""
        
        collections = self.client.get_collections().collections
        collection_names = [col.name for col in collections]
        
        if self.collection_name not in collection_names:
            print(f"📁 Creating new collection: {self.collection_name}")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.embedding_dim,
                    distance=Distance.COSINE
                )
            )
        else:
            print(f"📁 Collection already exists: {self.collection_name}")
    
    def add_text(self, text, metadata=None):
        """Add a single text to the database"""
        
        # Generate embedding
        embedding = self.embedding_model.encode(text).tolist()
        
        # Create point
        point_id = str(uuid.uuid4())
        
        # Add timestamp if not in metadata
        if metadata is None:
            metadata = {}
        
        if 'timestamp' not in metadata:
            metadata['timestamp'] = datetime.now().isoformat()
        
        metadata['text'] = text  # Store original text in metadata
        
        # Upload to Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=metadata
                )
            ]
        )
        
        return point_id
    
    def add_texts_batch(self, texts, metadatas=None):
        """Add multiple texts in batch"""
        
        if metadatas is None:
            metadatas = [{}] * len(texts)
        
        print(f"📤 Adding {len(texts)} texts to database...")
        
        # Generate embeddings for all texts
        embeddings = self.embedding_model.encode(texts).tolist()
        
        # Create points
        points = []
        for text, embedding, metadata in zip(texts, embeddings, metadatas):
            point_id = str(uuid.uuid4())
            
            # Add timestamp and text
            metadata['timestamp'] = metadata.get('timestamp', datetime.now().isoformat())
            metadata['text'] = text
            
            points.append(
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=metadata
                )
            )
        
        # Upload to Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        
        print(f"✅ Added {len(texts)} texts successfully!")
        
        return [p.id for p in points]
    
    def search(self, query, limit=5):
        """Search for similar texts"""
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Search in Qdrant
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit
        )
        
        return results
    
    def get_stats(self):
        """Get database statistics"""
        
        collection_info = self.client.get_collection(self.collection_name)
        
        stats = {
            'total_points': collection_info.points_count,
            'vectors_count': collection_info.vectors_count,
            'status': collection_info.status
        }
        
        return stats
    
    def delete_collection(self):
        """Delete the entire collection"""
        self.client.delete_collection(self.collection_name)
        print(f"🗑️  Deleted collection: {self.collection_name}")

# Test the connection
if __name__ == "__main__":
    print("🧪 Testing Qdrant Connection...\n")
    
    # Initialize
    db = VectorDatabase()
    
    # Test adding data
    print("\n📝 Testing data insertion...")
    test_texts = [
        "Python is a high-level programming language.",
        "Machine learning is a subset of artificial intelligence.",
        "Vector databases enable fast similarity search."
    ]
    
    test_metadata = [
        {"book": "Python Basics", "chapter": "1"},
        {"book": "AI Guide", "chapter": "3"},
        {"book": "Databases", "chapter": "5"}
    ]
    
    db.add_texts_batch(test_texts, test_metadata)
    
    # Test search
    print("\n🔍 Testing search...")
    query = "What is machine learning?"
    results = db.search(query, limit=2)
    
    print(f"\nQuery: '{query}'")
    print(f"Found {len(results)} results:\n")
    
    for i, result in enumerate(results, 1):
        print(f"{i}. Score: {result.score:.4f}")
        print(f"   Book: {result.payload.get('book', 'N/A')}")
        print(f"   Text: {result.payload['text'][:100]}...")
        print()
    
    # Show stats
    print("📊 Database Stats:")
    stats = db.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")