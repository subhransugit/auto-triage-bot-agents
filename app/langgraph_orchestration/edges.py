# app/langgraph_orchestration/edges.py

def should_continue_to_reasoning(state):
    return bool(state["docs"])  # Only reason if docs are found

def should_end(state):
    return not state["docs"]  # End early if nothing found
