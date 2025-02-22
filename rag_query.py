import faiss
import numpy as np
import sqlite3
from langchain.embeddings import OpenAIEmbeddings
from transformers import pipeline

# Load FAISS index
index = faiss.read_index("medical_index.faiss")

# Load SQLite database
conn = sqlite3.connect("medical.db")
cursor = conn.cursor()

# Load embeddings
embedding_model = OpenAIEmbeddings()

# Load LLaMA model (change model path if needed)
llama_pipeline = pipeline("text-generation", model="meta-llama/Llama-3-8B-Instruct")

def retrieve_medical_info(query):
    """Retrieves relevant medical information from the database."""
    query_vector = np.array(embedding_model.embed_documents([query])).astype("float32")
    
    # Search FAISS index
    D, I = index.search(query_vector, 3)  # Top 3 results
    
    # Fetch results from database
    retrieved_docs = []
    for idx in I[0]:
        cursor.execute("SELECT condition, description FROM medical_records WHERE id=?", (idx+1,))
        row = cursor.fetchone()
        if row:
            retrieved_docs.append(f"{row[0]}: {row[1]}")
    
    return "\n".join(retrieved_docs)

def generate_response(query):
    """Generates response using LLaMA 3 with RAG-retrieved context."""
    context = retrieve_medical_info(query)
    prompt = f"Context: {context}\n\nQuestion: {query}\nAnswer:"
    
    response = llama_pipeline(prompt, max_length=200, do_sample=True)
    return response[0]['generated_text']

# Example query
user_query = "What is hypertension?"
print(generate_response(user_query))
