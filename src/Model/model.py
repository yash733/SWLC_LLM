from langchain_groq import ChatGroq
from langchain_ollama import OllamaLLM
import streamlit as st

class model:
    def groq_llm(model_name:str):
        model = ChatGroq(model = model_name)
        return model

    def ollama_llm(model_name:str):
        model = OllamaLLM(model = model_name)
        return model