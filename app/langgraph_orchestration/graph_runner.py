from langgraph.graph import StateGraph
from .nodes import retrieve_node, reasoning_node, feedback_node
from .edges import should_continue_to_reasoning, should_end

def build_graph():
    builder = StateGraph()
    builder.add_node("retrieval", retrieve_node)
    builder.add_node("reasoning", reasoning_node)
    builder.add_node("feedback", feedback_node)
    builder.set_entry_point("retrieval")
    builder.add_conditional_edges("retrieval", {"yes":"reasoning","no":"feedback"}, should_continue_to_reasoning)
    builder.add_edge("reasoning", "feedback")
    builder.set_finish_point("feedback")
    return builder.compile()


