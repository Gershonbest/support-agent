from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
import os

embeddings = OpenAIEmbeddings()
faiss_index_path = "episodic_memory.faiss"

# Load or Create FAISS index
if os.path.exists(faiss_index_path):
    episodic_memory = FAISS.load_local(faiss_index_path, embeddings)
else:
    episodic_memory = FAISS.from_texts([], embeddings)

def store_episodic_memory(user_input, bot_response):
    text_data = f"User: {user_input} | Bot: {bot_response}"
    episodic_memory.add_texts([text_data])
    episodic_memory.save_local(faiss_index_path)

def retrieve_episodic_memory(query):
    results = episodic_memory.similarity_search(query, k=3)
    return [res.page_content for res in results]
