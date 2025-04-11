from configparser import ConfigParser
import os

from src.log.logger import logging

log_conf = logging.getLogger('CONFIG')
log_conf.setLevel(logging.DEBUG)

class Config:
    def __init__(self,config_file=rf"{os.getcwd()}/app/uiconfig.ini"):
        self.config=ConfigParser()
        self.config.read(config_file)

    # - - - - - - - -
    # Return list of options, parsed from uiconfig.ini
    # - - - - - - - -

    def get_llm_options(self):
        log_conf.debug(self.config["DEFAULT"].get("LLM_OPTIONS").split(", "))
        return self.config["DEFAULT"].get("LLM_OPTIONS").split(", ")
    
    def get_groq_model_options(self):
        log_conf.debug(self.config["DEFAULT"].get("GROQ_MODEL_OPTIONS").split(", "))
        return self.config["DEFAULT"].get("GROQ_MODEL_OPTIONS").split(", ")
    
    def get_ollama_model_options(self):
        log_conf.debug(self.config["DEFAULT"].get("OLLAMA_MODEL_OPTIONS").split(', '))
        return self.config["DEFAULT"].get("OLLAMA_MODEL_OPTIONS").split(', ')

    # Reasoning Model
    def get_llm_reasoning(self):
        log_conf.debug(self.config["DEFAULT"].get('REASONING_LLM').split(", "))
        return self.config["DEFAULT"].get('REASONING_LLM').split(", ")
    
    def get_reasoning_model(self):
        log_conf.debug(self.config["DEFAULT"].get('REASONING_MODEL_OPTIONS').split(", "))
        return self.config["DEFAULT"].get('REASONING_MODEL_OPTIONS').split(", ")

    # Page Title
    def get_page_title(self):
        log_conf.debug(self.config["DEFAULT"].get("PAGE_HEADER"))
        return self.config["DEFAULT"].get("PAGE_HEADER")
    
    # Page Header
    def get_page_header(self):
        log_conf.debug(self.config["DEFAULT"].get("PAGE_TITLE"))
        return self.config["DEFAULT"].get("PAGE_TITLE")