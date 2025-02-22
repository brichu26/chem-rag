import sqlite3
import faiss
import numpy as np
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.docstore.document import Document

# Load data from SQLite
conn = sqlite3.connect("medical.db")
cursor = conn.cursor()
cursor.execute("SELECT id, condition, description FROM medical_records")
rows = cursor.fetchall()
conn.close()

# Prepare documents
docs = [Document(page_content=row[2], metadata={"id": row[0], "condition": row[1]}) for row in rows]

# Initialize embeddings
embedding_model = OpenAIEmbeddings()

# Convert documents to vectors
texts = [doc.page_content for doc in docs]
vectors = embedding_model.embed_documents(texts)

# Convert list to numpy array
vectors = np.array(vectors).astype("float32")

# Store in FAISS
index = faiss.IndexFlatL2(vectors.shape[1])  # L2 distance
index.add(vectors)

# Save FAISS index
faiss.write_index(index, "medical_index.faiss")
