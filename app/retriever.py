from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from app.kb_loader import load_kb_and_create_vector_store
import os

from dotenv import load_dotenv
load_dotenv()


def get_retriever():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment.")
    if not os.path.exists("faiss_index"):
        load_kb_and_create_vector_store()
    # Pass API key explicitly
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    db =  FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    return db.as_retriever(search_kwargs={"k": 3})
