from langchain.prompts import PromptTemplate

support_prompt = PromptTemplate.from_template("""
You are a smart and friendly technical support assistant.
Answer the user's question using only the context below. Be clear and concise.

Context:
{context}
Question:
{question}
Answer:
""")

