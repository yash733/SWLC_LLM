import streamlit as st
import os, sys
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.structure import setup_environment, graph
from src.share import State

class UI:
    def __init__(self):
        # Initialize session state variables
        if "state" not in st.session_state:
            st.session_state.state = 'START'
        if "work_flow" not in st.session_state:
            st.session_state.work_flow = graph(State)
        if "config" not in st.session_state:
            st.session_state.config = {'configurable': {'thread_id': f'{datetime.now()}'}}

    def run(self):
        # Title
        st.title('Hackathon Project --')
        st.header('End To End Software Development Life Cycle')

        # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Sidebar for metadata
        with st.sidebar:
            GROK_API_KEY = st.text_input('Enter Groq API Key: ', type='password', value='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')
            if st.button('Submit'):
                setup_environment(GROK_API_KEY)
            
        
        if st.session_state.state == 'START':
            # Input fields
            user_requirement_input = st.text_area('Describe your requirements: ', key='user_requirement_input')
            tech_stack = st.text_input('Enter Tech Stack', key='tech_stack', value='Python, Django, Streamlit')

            if st.button('Proceed'):
                # Configurations
                initial_input = {'user_requirement_input': user_requirement_input, 'tech_stack': tech_stack}
                
                # Invoke model
                st.session_state.work_flow.invoke(input=initial_input, config=st.session_state.config)
            
        # Handle different states
        if st.session_state.state == 'User Story':
            st.subheader("User Story")
            state = st.session_state.work_flow.get_state(st.session_state.config)  # Snapshot
            st.write(state.values.get('user_story'))
            user_story_feedback = st.text_area("Enter your feedback:", key='user_story_feedback')

            if st.button('Proceed', key='User Story'):
                st.session_state.work_flow.update_state(config=st.session_state.config, values={'user_feedback': user_story_feedback})
                st.session_state.work_flow.invoke(None, config=st.session_state.config)
            
        elif st.session_state.state in ['Blue Print Feedback', 'Blue Print']:
            state = st.session_state.work_flow.get_state(st.session_state.config)  # Snapshot
            st.subheader('Refined User Story: ')
            st.write(state.values.get('user_story'))

            st.subheader('Design Document: ')
            st.write(state.values.get('blue_print'))

            blue_print_feedback = st.text_input('Provide Your Feedback: ', key = 'Design Documnet')

            if st.button('Proceed', key='Blue Print'):
                st.session_state.work_flow.update_state(config=st.session_state.config, values={'user_feedback': blue_print_feedback})
                st.session_state.work_flow.invoke(None, config=st.session_state.config)
            
        elif st.session_state.state in ['Quality Test', 'Test Case Review', 'Security Review', 'Code Review', 'Generate Code']:
            state = st.session_state.work_flow.get_state(st.session_state.config)  # Snapshot
            st.subheader('Code: ')
            st.write(state.values.get('code'))
            code_feedback = st.text_input('Provide Your Feedback: ', key = 'Code Review')

            if st.button('Proceed', key='generate code'):
                st.session_state.work_flow.update_state(config=st.session_state.config, values={'user_feedback': code_feedback})
                st.session_state.work_flow.invoke(None, config=st.session_state.config)
            
        elif st.session_state.state in ["Quality Test", "Final Review"]:
            state = st.session_state.work_flow.get_state(st.session_state.config)  # Snapshot
            st.subheader('Test Case: ')
            st.write(state.values.get('test_case'))
            
            st.header('Final Output: ')
            st.write(state.values.get('file_structure'))
            st.write(state.values.get('code'))
            
# Create an instance of the UI class and run the app
ui = UI()
ui.run()