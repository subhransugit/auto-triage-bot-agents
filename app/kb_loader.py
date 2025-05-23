from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os

from dotenv import load_dotenv
load_dotenv()

def load_kb_and_create_vector_store(path="data/support_kb/"):
    """
    Load the knowledge base from the specified path and create a vector store.
    """


    # Load documents from the specified directory
    loader = DirectoryLoader(path, glob="**/*.txt")
    documents = loader.load()

    # Split documents into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    # Create embeddings for the text chunks
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found")

    embeddings = OpenAIEmbeddings(openai_api_key=api_key)

    # Create a vector store using Chroma
    vector_store = FAISS.from_documents(texts, embeddings)
    vector_store.save_local("faiss_index")


