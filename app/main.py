import streamlit as st
from dotenv import load_dotenv
from app.memory_store import memory
from app.agents.orchestrator import Orchestrator
from app.langgraph_orchestration.graph_runner import build_graph

load_dotenv()
st.set_page_config(page_title="Auto-Triage Support Bot", layout="centered")
st.title("🤖 Auto-Triage Support Bot")

# Session state init
if "query" not in st.session_state:
    st.session_state.query = ""
if "answer_data" not in st.session_state:
    st.session_state.answer_data = None
if "feedback" not in st.session_state:
    st.session_state.feedback = None
if "mode" not in st.session_state:
    st.session_state.mode = "LangChain Agent"

# Mode toggle
st.radio("Choose agent mode:", ["LangChain Agent", "LangGraph Flow"], key="mode")

# User query
query = st.text_input("💬 Ask your support question:", value=st.session_state.query)

# Submit button
if st.button("Submit"):
    st.session_state.query = query
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        if st.session_state.mode == "LangChain Agent":
            orchestrator = Orchestrator()
            result = orchestrator.process(query)
            st.session_state.answer_data = result
        else:
            graph = build_graph()
            result = graph.invoke({
                "query": query,
                "chat_history": memory.chat_memory.messages
            })
            st.session_state.answer_data = result

        st.session_state.feedback = None

# Display answer + sources
if st.session_state.answer_data:
    st.subheader("📌 Answer")
    st.write(st.session_state.answer_data.get("answer", "⚠️ No answer returned"))

    if "source_documents" in st.session_state.answer_data:
        st.subheader("📚 Source Documents")
        for doc in st.session_state.answer_data["source_documents"]:
            st.text(doc.page_content[:300])

    # Feedback
    st.radio("🗳️ Was this helpful?", ("Yes", "No"), key="feedback")

    if st.button("Submit Feedback"):
        feedback = st.session_state.get("feedback")
        if feedback:
            if st.session_state.mode == "LangGraph Flow":
                # Resubmit to graph with feedback
                graph = build_graph()
                graph.invoke({
                    "query": st.session_state.query,
                    "answer": st.session_state.answer_data.get("answer"),
                    "feedback": feedback,
                    "chat_history": memory.chat_memory.messages
                })
            else:
                orchestrator = Orchestrator()
                orchestrator.feedback(
                    st.session_state.query,
                    st.session_state.answer_data.get("answer"),
                    feedback
                )
            st.success("✅ Feedback submitted!")
        else:
            st.warning("⚠️ Please select feedback before submitting.")

# Sidebar history
with st.sidebar:
    st.subheader("🧠 Chat History")
    for m in memory.chat_memory.messages:
        st.markdown(f"**{m.type.capitalize()}**: {m.content}")
