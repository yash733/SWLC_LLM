import streamlit as st
import os, sys
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.structure import setup_environment, graph 
from src.share import State

#-----Title
st.title('Hackathon Project --')
st.header('End To End Software Development Life Cycle')

#-----Data Base
if "chat_history" not in st.session_state:
   st.session_state.chat_history = []

#-----Meta data
with st.sidebar:
    GROK_API_KEY = st.text_input('Enter Groq API Key: ', type= 'password', value='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')
    setup_environment(GROK_API_KEY)


#-----input
user_requirement_input = st.text_area('Describe your requirements: ')
tech_stack = st.text_input('Enter Tech Stack', value= 'Python')

if user_requirement_input:
    #----- Confurations
    initial_input = {'user_requirement_input': user_requirement_input, 'tech_stack': tech_stack}
    config = {'configurable':{'thread_id':f'{datetime}'}}
    
    #----- Main -----#
    # INVOKE MODEL
    graph = graph(State)
    graph.invoke(input= initial_input,config= config)

    st.subheader("User Story")
    # Interrupt 
    #    Before ----> User Story Feedback
    state = graph.get_state(config)  # sanapshot
    st.write(state.values.get('user_story'))
    user_story_feedback = st.text_area("Enter you feedback: ")

    if user_story_feedback:
        graph.update_state(config= config, values= {'user_feedback': user_story_feedback})

        # Continue --> User Story Feedback
        graph.invoke(None, config= config)
        state = graph.get_state(config)  # sanapshot
        
        # Interrupt
        #     After ---> Blue Print
        st.subheader('Refined User Story: ')
        st.write_stream(state.values.get('user_story'))

        st.subheader('Design Document: ')
        st.write(state.values.get('blue_print'))

        blue_print_feedback = st.text_input('Provide Your Feedback: ')

        if blue_print_feedback:
            graph.update_state(config= config, values= {'user_feedback': blue_print_feedback})

            # Continue ---> Blue Print Feedback
            graph.invoke(None, config= config)
            state = graph.get_state(config) # snapshot

            # Interrupt 
            #      Before ---> Code Review

            st.subheader('Code: ')
            st.write(state.values.get('code'))
            code_feedback = st.text_input('Provide Your Feedback: ')

            if code_feedback:
                graph.update_state(config= config, values= {'user_feedback': code_feedback})

                # Continue ---> Code Review
                graph.invoke(None, config= config)
                state = graph.get_state(config) #snapshot

                st.subheader('Test Case: ')
                st.write(state.values.get('test_case'))
                
                st.header('Final Output: ')
                st.write(state.values.get('file_structure'))
                st.write(state.values.get('code'))

# import streamlit as st
# import os, sys
# from datetime import datetime
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from src.structure import setup_environment, graph 
# from src.share import State

# #-----Title
# st.title('Hackathon Project --')
# st.header('End To End Software Development Life Cycle')

# #-----Data Base
# if "chat_history" not in st.session_state:
#    st.session_state.chat_history = []

# #-----Meta data
# with st.sidebar:
#     GROK_API_KEY = st.text_input('Enter Groq API Key: ', type= 'password', value='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')
#     setup_environment(GROK_API_KEY)


# #-----input
# import streamlit as st
# from src.structure import Tracking, graph, State

# # Initialize session state
# if "graph" not in st.session_state:
#     st.session_state.graph = None
# if "config" not in st.session_state:
#     st.session_state.config = None
# if "current_state" not in st.session_state:
#     st.session_state.current_state = None
# if "tracking" not in st.session_state:
#     st.session_state.tracking = Tracking()  # Use the Tracking instance


# # Step 1: Initial Input
# if st.session_state.graph is None:
#     with st.container():
#         user_requirement_input = st.text_area('Describe your requirements: ')
#         tech_stack = st.text_input('Enter Tech Stack', value='Python, Django, Fast API')
#         if st.button('Submit Requirements'):
#             # Initialize graph and config
#             initial_input = {'user_requirement_input': user_requirement_input, 'tech_stack': tech_stack}
#             st.session_state.config = {'configurable': {'thread_id': 'unique_thread_id'}}
#             st.session_state.graph = graph(State)
#             st.session_state.tracking.add_state("User Story")
#             st.session_state.graph.invoke(input=initial_input, config=st.session_state.config)
#             st.session_state.current_state = st.session_state.tracking.pop_last_state()

# # Dynamic UI Rendering
# if st.session_state.graph is not None:
#     while True:
#         current_state = st.session_state.current_state

#         if current_state is None:
#             break

#         # Handle "User Story" state
#         if current_state == "User Story":

#             st.subheader("User Story")
#             data = st.session_state.graph.get_state(st.session_state.config)
#             st.write(data.get('user_story'))
#             user_story_feedback = st.text_input("Enter your feedback for User Story:")
#             if st.button('Submit User Story Feedback'):
#                 st.session_state.graph.update_state(
#                     config=st.session_state.config,
#                     values={'user_feedback': user_story_feedback}
#                 )
#                 st.session_state.graph.invoke(None, config=st.session_state.config)
#                 st.session_state.current_state = st.session_state.tracking.pop_last_state()
#                 break

#         # Handle "Blue Print" state
#         elif current_state == "Blue Print":
#             st.subheader("Design Document (Blueprint)")
#             st.write("Provide feedback for the blueprint.")
#             blue_print_feedback = st.text_input("Enter your feedback for Blueprint:")
#             if st.button('Submit Blueprint Feedback'):
#                 st.session_state.graph.update_state(
#                     config=st.session_state.config,
#                     values={'user_feedback': blue_print_feedback}
#                 )
#                 st.session_state.graph.invoke(None, config=st.session_state.config)
#                 st.session_state.current_state = st.session_state.tracking.pop_last_state()
#                 break

#         # Handle "Code Review" state
#         elif current_state == "Code Review":
#             st.subheader("Code Review")
#             st.write("Provide feedback for the code.")
#             code_feedback = st.text_input("Enter your feedback for Code:")
#             if st.button('Submit Code Feedback'):
#                 st.session_state.graph.update_state(
#                     config=st.session_state.config,
#                     values={'user_feedback': code_feedback}
#                 )
#                 st.session_state.graph.invoke(None, config=st.session_state.config)
#                 st.session_state.current_state = st.session_state.tracking.pop_last_state()
#                 break

#         # Handle "Final Review" state
#         elif current_state == "Final Review":
#             st.subheader("Final Review")
#             st.write("Review the final output.")
#             st.success("Process Completed!")
#             break