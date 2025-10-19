# main_rag.py
from vector_db import VectorDatabase
from ocr import capture_and_extract
from langchain_ollama import OllamaLLM
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Qdrant  # Optional if using LangChain wrapper

# 1️⃣ Initialize Qdrant DB
db = VectorDatabase(collection_name="book_knowledge")

# 2️⃣ Initialize LLM and embeddings (use same model as VectorDatabase)
llm = OllamaLLM(model="llama3.1:8b")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 3️⃣ Capture text (replace region if needed)
print("📸 Capturing screenshot and extracting text...")
text = capture_and_extract(region=None)  # None = full screen
print("✅ Text extracted (first 200 chars):", text[:200])

# 4️⃣ Store in Vector DB
db.add_text(text, metadata={"source": "screenshot"})
print("💾 Text added to Qdrant!")

# 5️⃣ Create LangChain wrapper with retriever
vector_store = Qdrant(
    client=db.client, 
    collection_name="book_knowledge", 
    embeddings=embeddings,
    content_payload_key="text"  # Tell LangChain where to find the text content
)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# 6️⃣ Create QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

query = input("Ask a question about the captured text: ")

# Use the QA chain to get an answer
response = qa_chain.invoke({"query": query})

print("\n🤖 Answer:")
print(response['result'])

print("\n📄 Source Documents:")
for i, doc in enumerate(response['source_documents'], 1):
    print(f"\n{i}. {doc.page_content[:200]}...")
