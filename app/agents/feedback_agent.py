# app/agents/feedback_agent.py

import os

class FeedbackAgent:
    def __init__(self, log_path="data/feedback_log.txt"):
        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

    def record(self, query, response, helpful):
        with open(self.log_path, "a") as f:
            f.write(f"QUERY: {query}\nRESPONSE: {response}\nHELPFUL: {helpful}\n---\n")
