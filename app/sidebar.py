import os
import streamlit as st
from src.log.logger import logging

logui = logging.getLogger('UI')
logui.setLevel(logging.DEBUG)

from app.uiconfig import Config
from src.Model.model import model

class LLM_Selection:
    def __init__(self, user_controls, config):
        self.user_controls = user_controls
        self.config = config

    def sidebar(self):
        with st.sidebar:
            #----- MAIN MODEL -----#
            self.user_controls['LLM'] = st.selectbox(label= "Select LLM", options= self.config.get_llm_options())
            
            # ----- GROQ -----#
            if self.user_controls['LLM'] == 'Groq':
                logui.info('LLM-GROQ')
                self.user_controls['Model'] = st.selectbox(label= 'Choose Model', options= self.config.get_groq_model_options(), key="LLM_Model")
                logui.info(self.user_controls['Model'])
                st.session_state.model = model.groq_llm(self.user_controls['Model'])   #{'type':'GROQ', 'model':self.user_controls['Model']}
            
                #----- API KEY -----#
                self.user_controls['API_KEY'] = st.text_input('Enter Groq API Key: ', type='password')
                if self.user_controls['API_KEY']:
                    os.environ['GROQ_API_KEY'] = self.user_controls['API_KEY']
                    logui.info('GROQ_API_KEY')
                    api = True
                else:
                    api = False
                    st.warning("⚠️ Please enter your GROQ API key to proceed. Don't have? refer : https://console.groq.com/keys ")
                    logui.error('NO API KEY')
            
            # ----- Ollama -----#
            elif self.user_controls['LLM'] == 'Ollama':
                api = True
                logui.info('LLM-OLLAMA')
                self.user_controls['Model'] = st.selectbox(label= 'Choose Model', options= self.config.get_ollama_model_options(), key="LLM_MODEL")
                logui.info(self.user_controls['Model'])
                st.session_state.model = model.ollama_llm(self.user_controls['Model'])  #{'type':'OLLAMA', 'model':self.user_controls['Model']}
                
            #----- REASONING MODEL -----#   
            self.user_controls['LLM_REASONING'] = st.selectbox(label= 'Select Reasoninig LLM', options= self.config.get_llm_reasoning())

            if self.user_controls['LLM_REASONING'] == 'Ollama':
                self.user_controls['Reasoning_Model'] = st.selectbox(label= 'Choose Reasoning Model', options= self.config.get_reasoning_model(), key= "reasoning llm")
                st.session_state.reasoning_model = model.ollama_llm(self.user_controls['Reasoning_Model'])  #{'type':'Ollama', 'model':self.user_controls['Reasoning_Model']}
                logui.info('LLM_reasoning_Ollama')
            
            if st.session_state.save == False and api:
                # print('*'*50)
                # print(self.user_controls)
                if st.button('Save', key='save12'): 
                    st.session_state.save = True
                    return self.user_controls
                else:
                    st.stop()
            return self.user_controls

