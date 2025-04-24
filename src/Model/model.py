from langchain_groq import ChatGroq
from langchain_community.chat_models import ChatOllama

class model:
    def groq_llm(model_name:str):
        model = ChatGroq(model = model_name)
        return model

    def ollama_llm(model_name:str):
        model = ChatOllama(model = model_name)
        return model