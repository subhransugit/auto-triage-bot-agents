from langchain.chains import ConversationalRetrievalChain
import os
from langchain_community.llms import OpenAI

from app.prompts.support_prompt import support_prompt
from app.retriever import get_retriever

from dotenv import load_dotenv
load_dotenv()

class ReasoningAgent:
    def __init__(self):
        self.retriever = get_retriever()




    def generate_answer(self, docs, query: str,chat_history=None):
        chain =  ConversationalRetrievalChain.from_llm(
            llm=OpenAI(temperature=0),
            retriever=self.retriever,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": support_prompt},

        )
        result = chain.invoke({"question": query,
                               "chat_history": chat_history or []})
        return result
