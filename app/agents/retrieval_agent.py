
from app.retriever import get_retriever

from dotenv import load_dotenv
load_dotenv()

class RetrievalAgent:
    def __init__(self):
        self.retriever = get_retriever()

    def retrieve_docs(self, query: str,chat_history=None):
        docs = self.retriever.get_relevant_documents(query)
        return docs
