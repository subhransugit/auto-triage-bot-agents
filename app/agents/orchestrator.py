from .retrieval_agent import RetrievalAgent
from .reasoning_agent import ReasoningAgent
from .feedback_agent import FeedbackAgent
from app.memory_store import memory

class Orchestrator:
    def __init__(self):
        self.retrieval_agent = RetrievalAgent()
        self.reasoning_agent = ReasoningAgent()
        self.feedback_agent = FeedbackAgent()

    def process(self, query):
        # Step 1: Retrieve relevant documents
        docs = self.retrieval_agent.retrieve_docs(query)
        if not docs:
            return "Sorry, no relevant information found.", docs

        # Step 2: Generate an answer using the retrieved documents
        result = self.reasoning_agent.generate_answer(docs, query,memory.chat_memory.messages)
        memory.save_context({"question": query}, {"answer": result["answer"]})
        return result

        # Step 3: Record feedback (optional)
        # self.feedback_agent.record(query, answer, helpful=True)  # Example usage

    def feedback(self, query, response, helpful):
        self.feedback_agent.record(query, response, helpful)
