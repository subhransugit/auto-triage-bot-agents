# app/langgraph_orchestration/nodes.py

from app.agents.retrieval_agent import RetrievalAgent
from app.agents.reasoning_agent import ReasoningAgent
from app.agents.feedback_agent import FeedbackAgent
from app.memory_store import memory

retrieval_agent = RetrievalAgent()
reasoning_agent = ReasoningAgent()
feedback_agent = FeedbackAgent()

def retrieve_node(state):
    query = state["query"]
    docs = retrieval_agent.retrieve_docs(query,memory.chat_memory.messages)
    return {"query": query, "docs": docs, "chat_history": memory.chat_memory.messages}

def reasoning_node(state):
    docs = state["docs"]
    query = state["query"]
    response = reasoning_agent.generate_answer(docs, query,state["chat_history"])
    memory.save_context({"question": query}, {"answer": response["answer"]})
    return {**state, "answer": response["answer"], "source_documents": response["source_documents"]}


def feedback_node(state):
    feedback_agent.record(
        state["query"], state.get("answer", ""), state.get("feedback", "Unspecified")
    )
    return state
