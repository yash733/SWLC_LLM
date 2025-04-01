from configparser import ConfigParser
import os

class Config:
    def __init__(self,config_file=f"{os.getcwd()}\app\uiconfig.ini"):
        self.config=ConfigParser()
        self.config.read(config_file)

    def get_llm_options(self):
        return self.config["DEFAULT"].get("LLM_OPTIONS").split(", ")
    
    def get_groq_model_options(self):
        return self.config["DEFAULT"].get("GROQ_MODEL_OPTIONS").split(", ")
    
    def get_llm_reasoning(self):
        return self.config["DEFAULT"].get('REASONING_LLM').split(", ")
    
    def get_reasoning_model(self):
        return self.config["DEFAULT"].get('OLLAMA_MODEL_OPTIONS').split(", ")

    def get_page_title(self):
        return self.config["DEFAULT"].get("PAGE_HEADER")
    
    def get_page_header(self):
        return self.config["DEFAULT"].get("PAGE_TITLE")