import streamlit as st
import os, sys
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.structure import graph_node
from src.share import State
from app.uiconfig import Config
import ast

from src.log.logger import logging

logui = logging.getLogger('UI')
logui.setLevel(logging.DEBUG)

class UI:
    def __init__(self):
        # Initialize session state variables
        if "selected_llm" not in st.session_state:
            st.session_state.selected_llm = None
        if "selected_reasoning_llm" not in st.session_state:
            st.session_state.selected_reasoning_llm = None

        if "state" not in st.session_state:
            st.session_state.state = 'START'

        # Configuration
        if "config" not in st.session_state:
            st.session_state.config = {'configurable': {'thread_id': f'{datetime.now()}'}}
        
        # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []   
        
        self.user_controls = {}
        self.config = Config()

        # Defining Workflow stages
        self.stages = [
            "START",
            "User Story",
            "System Feedback",
            "Blue Print",
            "Blue Print Feedback",
            "Generate Code",
            "Code Review",
            "Security Review",
            "Write Test Case",
            "Test Case Review",
            "Quality Test",          
            "Final Review"
        ]

    def render_process(self):
        st.sidebar.markdown("### Workflow Progress")
        logui.info("render_process")
        for stage in self.stages:
            if stage == st.session_state.state:
                st.sidebar.markdown(f"🟢 {stage}")  # Highlight current stage
            else:
                st.sidebar.markdown(f":white_circle: {stage}")  # Other stages

    def run(self):
        # Title
        title = self.config.get_page_title()
        header = self.config.get_page_header()
        st.title(title)
        st.header(header)
        logui.info('Headers')
        
        # Sidebar for metadata
        with st.sidebar:
            #----- MAIN MODEL -----#
            self.user_controls['LLM'] = st.selectbox(label= "Select LLM", options= self.config.get_llm_options())
            
            if self.user_controls['LLM'] == 'Groq':
                logui.info('LLM-GROQ')
                self.user_controls['Model'] = st.selectbox(label= 'Choose Model', options= self.config.get_groq_model_options())
                logui.info(self.user_controls['Model'])
                st.session_state.selected_llm = {'type':'GROQ', 'model':self.user_controls['Model']}

                #----- API KEY -----#
                self.user_controls['API_KEY'] = st.text_input('Enter Groq API Key: ', type='password')
                if self.user_controls['API_KEY']:
                    os.environ['GROQ_API_KEY'] = self.user_controls['API_KEY']
                    logui.info('GROQ_API_KEY')
                else:
                    st.warning("⚠️ Please enter your GROQ API key to proceed. Don't have? refer : https://console.groq.com/keys ")
                    logui.error('NO API KEY')
            
            #----- REASONING MODEL -----#   
            self.user_controls['LLM_REASONING'] = st.selectbox(label= 'Select Reasoninig LLM', options= self.config.get_llm_reasoning())

            if self.user_controls['LLM_REASONING'] == 'Ollama':
                self.user_controls['Reasoning_Model'] = st.selectbox(label= 'Choose Reasoning Model', options= self.config.get_reasoning_model())
                st.session_state.selected_reasoning_llm = {'type':'Ollama', 'model':self.user_controls['Reasoning_Model']}
                logui.info('LLM_reasoning_Ollama')
        
        if st.session_state.selected_llm and st.session_state.selected_reasoning_llm:
            #----- graph.invoke() -----#
            if "work_flow" not in st.session_state: 
                graph_instance = graph_node()
                st.session_state.work_flow = graph_instance.graph(State)
                logui.info("Graph Initialization")
        
        #----- Render progress tracker -----#
        self.render_process()
        
        if st.session_state.state == 'START':
            st.write('''This project is a Streamlit-based application designed to automate and streamline the Software Development Life Cycle (SDLC) 
            using Large Language Models (LLMs). The application provides an interactive interface for users to input their software requirements, 
            receive generated outputs (such as user stories, blueprints, and code), and provide feedback at each stage of the development process. 
            The workflow is powered by a backend graph-based system that manages the state transitions and invokes LLMs to generate outputs dynamically.''')
            
            # Input fields
            user_requirement_input = st.text_area('Describe your requirements: ', key='user_requirement_input')
            tech_stack = st.text_input('Enter Tech Stack', key='tech_stack', value='Python, Django, Streamlit')
            
            logui.info('UI_START')
            if st.button('Proceed'):
                # Configurations
                initial_input = {'user_requirement_input': user_requirement_input, 'tech_stack': tech_stack}
                
                # Invoke model
                st.session_state.work_flow.invoke(input=initial_input, config=st.session_state.config)
                st.rerun()
            
        # Handle different states
        elif st.session_state.state == 'User Story':
            st.markdown("""
                <div style="background-color: #d4edda; padding: 10px; border-radius: 5px; color: #155724; font-size: 18px; font-weight: bold;">
                ✅ User Story
                </div>
            """, unsafe_allow_html=True)
            state = st.session_state.work_flow.get_state(st.session_state.config)  # Snapshot
            st.write(state.values.get('user_story'))
            user_story_feedback = st.text_area("Enter your feedback:", key='user_story_feedback')

            if st.button('Proceed', key='User Story'):
                st.session_state.work_flow.update_state(config=st.session_state.config, values={'user_feedback': user_story_feedback})
                st.session_state.work_flow.invoke(None, config=st.session_state.config)
                st.rerun()
            
        elif st.session_state.state in ['Blue Print Feedback', 'Blue Print']:
            state = st.session_state.work_flow.get_state(st.session_state.config)  # Snapshot
            st.markdown("""
                <div style="background-color: #d4edda; padding: 10px; border-radius: 5px; color: #155724; font-size: 18px; font-weight: bold;">
                ✅ Refined User Story
                </div>
            """, unsafe_allow_html=True)
            st.write(state.values.get('user_story'))

            st.markdown("""
                <div style="background-color: #d4edda; padding: 10px; border-radius: 5px; color: #155724; font-size: 18px; font-weight: bold;">
                ✅ Design Document
                </div>
            """, unsafe_allow_html=True)
            st.write(state.values.get('blue_print'))

            blue_print_feedback = st.text_input('Provide Your Feedback: ', key = 'Design Documnet')

            if st.button('Proceed', key='Blue Print'):
                st.session_state.work_flow.update_state(config=st.session_state.config, values={'user_feedback': blue_print_feedback})
                st.session_state.work_flow.invoke(None, config=st.session_state.config)
                st.rerun()
            
        elif st.session_state.state in ['Quality Test', 'Test Case Review', 'Security Review', 'Code Review', 'Generate Code']:
            state = st.session_state.work_flow.get_state(st.session_state.config)  # Snapshot
            st.markdown("""
                <div style="background-color: #d4edda; padding: 10px; border-radius: 5px; color: #155724; font-size: 18px; font-weight: bold;">
                ✅ Code
                </div>
            """, unsafe_allow_html=True)
        #----- Parsing Code -----#
            st.write(state.values.get('code'))
            code_feedback = st.text_input('Provide Your Feedback: ', key = 'Code Review')
            # with st.expander('Meta data'):
            #     parsed_code = ast.literal_eval(state.values.get('code'))
            #     st.code(parsed_code.code)
            if st.button('Proceed', key='generate code'):
                st.session_state.work_flow.update_state(config=st.session_state.config, values={'user_feedback': code_feedback})
                st.session_state.work_flow.invoke(None, config=st.session_state.config)
                st.rerun()
            
        elif st.session_state.state in ["Quality Test", "Final Review"]:
            state = st.session_state.work_flow.get_state(st.session_state.config)  # Snapshot
            st.subheader('Test Case: ')
            st.write(state.values.get('test_case'))
            
            st.header('Final Output: ')
            st.write(state.values.get('file_structure'))
            st.write(state.values.get('code'))
        
        # Add a button on the right-hand side using HTML and CSS
        st.markdown("""
            <div style="display: flex; justify-content: flex-end;">
                <form action="" method="post">
                    <button style="background-color: #FF0000; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;" type="submit">
                        Clear Cache
                    </button>
                </form>
            </div>
        """, unsafe_allow_html=True)

        # Logic to clear session state when the button is clicked
        if st.session_state.get("clear_cache", False):
            st.session_state.clear()
            st.experimental_rerun()
        
        # Add an expander to display the flow diagram
        with st.expander("View Workflow Diagram"):
            st.image("flow.png", caption="Workflow Diagram", use_column_width=True)
            
# Create an instance of the UI class and run the app

ui = UI()
ui.run()
