import streamlit as st
import os

from src.share import State
from src.structure import graph

user_requirement_input = st.text_area('Enter your requirements: ')
if user_requirement_input:
    initial_input = {'user_requirement_input': user_requirement_input}
    config = {'configurable':{'thread':'01'}}
    
    if st.button('Proceed'):
        # INVOKE MODEL
        graph = graph()
        for state in graph.stream(input= initial_input,config= config):
            pass

        st.subheader("Story")
        # Interrupt 
        #    After User Story 
        st.write(State['user story'])
        user_feedback = st.text_area("Enter you feedback: ")
        graph.update_state(config= config, values= {'user_feedback': user_feedback})

        # Continue
        for state in graph.stream(None, config= config):
            pass

        