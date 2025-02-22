# chem-rag

To install dependencies, run this in chem-rag directory: 
pip install faiss-cpu langchain transformers sqlite3 pandas openai

To populate the database, run medical_db.py. 
To generate the FAISS vector index, run index_medical_data.py.  
To query and generate responses with Llama3, run rag_query.py.  