#----- Libraries -----#
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_ollama import OllamaLLM
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
import streamlit as st

#----- Dependencies -----#
from src.share import State, Feedback, Code_Format, Improvement
from src.log.logger import logging

#----- LLM -- Model -----#
def get_model():
    model = ChatGroq(model = st.session_state.selected_llm['model'])
    reasoning_model = OllamaLLM(model = st.session_state.selected_reasoning_llm['model'])
    # phi_model = OllamaLLM(model = "Phi-4")
    return model, reasoning_model

   #----- LLM -- Structured -- Output -----#
def structred_output_llm():
    model, reasoning_model = get_model()
    feed_back_model = model.with_structured_output(Feedback)
    code_format_model = model.with_structured_output(Code_Format)
    improvement_model = model.with_structured_output(Improvement)
    return feed_back_model, code_format_model, improvement_model

#----- Setup -----#
load_dotenv()

os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_PROJECT'] = 'llm-app'
os.environ['LANGCHAIN_TRACING_V2'] = 'true'

#----- Logger Setup -----#
log1 = logging.getLogger('Update-Structure')
log1.setLevel(logging.DEBUG)

log2 = logging.getLogger('Error-Structure')
log2.setLevel(logging.INFO)


class graph_node:
    def __init__(self):
        self.model, self.reasoning_model = get_model()
        self.feed_back_model, self.code_format_model, self.improvement_model = structred_output_llm()

    #----- Structure -----#
    def User_Story(self, state: State):
        st.session_state.state = 'User Story'
        if state.get('user_story'):
            res = self.reasoning_model.invoke([ 
                {'role':'system', 'content':f"You are a Senior Product Owner. First analyzise the user story: {state['user_story']}. Now make necessary changes catering to "
                f"clients feedback: {state['user_feedback']}"}
            ])
            log1.info('Implemented Clients feedback - User Story')
        else:
            res = self.reasoning_model.invoke([ 
                {'role':'system', 'content':"You are a Senior Product Owner generate a user story. It is a short, informal description of a desired feature or functionality, "
                " written from the end-user's perspective, to help developers/engineers understand user needs and requirements."},
                {'role':'user', 'content':f'User requirement: {state["user_requirement_input"]}'}
            ])
            log1.info('Genrated - User Story')
        return {'user_story' : res}
        
    #------ Interrupt will happen, input: user feedback -----#
    def User_Story_Sentiment(self, state: State):
        st.session_state.state = 'User Story Feedback'
        log1.info('User_Story_Sentiment')
        return state

    def Sentiment(self, state: State):
        res = self.feed_back_model.invoke([
            {'role':'system','content':'Understand the feedback.'},
            {'role':'user', 'content':f"Feedback: {state['user_feedback']}"}
        ])
        log1.info('Perform Sentiment Analysis')
        state['user_feedback'] = res.user_feedback

        if res.grade == 'positive':
            log1.info('Sentiment - Positive')
            return 'Approve'
        
        log1.info('Sentiemnt - Negative')
        return 'Rejected'

    def System_FeedBack(self, state: State):
        st.session_state.state = 'System Feedback'
        res = self.model.invoke([
            {'role':'system', 'content':f'You are Senior most Product Owner'},
            {'role':'system', 'content':f'After mutiple talks with the client the user story looks like this:{state["user_story"]} as being a senior product owner '
            'refine the user story, validate each and every point so the project can move to next stage of creating blue print/design document.'}
        ])
        log1.info('System_FeedBack - User Story')
        return {"user_story" : res.content}

    def Create_Documentation(self, state: State):
        st.session_state.state = 'Blue Print'
        if state.get('blue_print'):
            res = self.model.invoke([
                {'role':'system', 'content':f'''Given the following user story:{state["user_story"]} and user feedback:{state["user_feedback"]}, 
                improve the generated detailed design document:{state["blue_print"]}, covering both High-Level Design (HLD) and Low-Level Design (LLD)'''}
            ])
            log1.info('User Feedback - Blue Print')
        else:
            res = self.model.invoke([
                {'role':'system','content':f'Given the following user story:{state["user_story"]}, generate a detailed design document covering both High-Level Design (HLD) '
                'and Low-Level Design (LLD)'}
            ])
            log1.info('Created - Blue Print')
        return {'blue_print' : res.content}
        #------ Interrupt will happen, input: user feedback -----#

    def Create_Documentation_Feedback(self, state: State):
        st.session_state.state = 'Blue Print Feedback'
        log1.info('Feedback - Blue Print')
        return state

    def Generate_Code(self, state: State):
        st.session_state.state = 'Generate Code'
        if state.get('code'):
            res = self.code_format_model.invoke([
                {'role':'system', 'content':f'This is the previous code: {state["code"]}. Analyze the feedback provided by the tech lead and client: {state["user_feedback"]}, and improve the code accordingly. Ensure the updated code adheres to best practices, is optimized for performance, and addresses all feedback points.'}
            ])
            log1.info('Feedback - Generate Code')
        
        else:
            res = self.code_format_model.invoke([
                {'role':'system','content':f'Generate a complete file structure and write code using the described tech stack: {state["tech_stack"]}. Ensure the code aligns with the user story: {state["user_story"]} and the design document: {state["blue_print"]}. Provide the output in the following format:\n\n'
                                      '1. File Structure: A hierarchical representation of the files.\n'
                                      '2. Code: Include the code for each file in the structure.'}
            ])
            log1.info('Generate Code')
    #----- File Name -----#
            #file_name = [i.file_name for i in res.code]
        # return {'code': res.content}
        # return {'code' : res.code, 'file_structure' : res.file_structure, 'file_name' : file_name}
        return {'code' : res.code, 'file_structure' : res.file_structure}
    
    #------ Interrupt will happen, input: user feedback -----#
    def Code_review(self, state: State):
        st.session_state.state = 'Code Review'
        res = self.model.invoke([
            {'role': 'system', 'content': f'You are a tech lead. Analyze the following code: {state["code"]} and file structure: {state["file_structure"]}. Provide detailed feedback on the following aspects:\n'
                                  '1. Bugs: Identify any bugs or errors in the code.\n'
                                  '2. Performance: Highlight any performance bottlenecks and suggest optimizations.\n'
                                  '3. Maintainability: Assess the code for readability, modularity, and adherence to best practices.\n'
                                  '4. File Structure: Suggest improvements to the file structure based on the provided file names: {state["file_name"]}.\n\n'
                                  'Ensure the feedback is actionable and includes specific recommendations for improvement.'},
            {'role': 'user', 'content': f'Client Feedback: {state["user_feedback"]}'}
            ])
        file_structure = self.model.invoke([{'role':'system', 'content':f'Improve the file structure:{state["file_structure"]}, with the help of file name:{state["file_name"]}'}])
        log1.info('Code review')
        return {'user_feedback' : res.content, 'file_structure' : file_structure.content}

    def Security_review(self, state: State):
        st.session_state.state = 'Security Review'
        res = self.improvement_model.invoke([
            {'role':'system', 'content':f'You are Tech Lead, carefully analyze the the code: {state["code"]}, look for security lapes and its possibilites.'}
        ])
        log1.info('Security review')
        return {'user_feedback' : res.improvement_feedback, 'rout' : 'Approve' if res.problems == 'no-problem' else 'Rejected'}

    def Write_test_case(self, state: State):
        st.session_state.state = 'Write Test Case'
        res = self.model.invoke([
            {'role':'system', 'content':f'Generate test cases undermining, client requiremrnt: {state["user_requirement_input"]}, user_story:{state["user_story"]} and software blue print:{state["blue_print"]}.\n'
            'Ensure the test cases cover all functional, edge, and boundary scenarios.'}
        ])
        log1.info('Ceating Test Case')
        return {'test_case' : res.content}

    def Test_case_review(self, state: State):
        st.session_state.state = 'Test Case Review'
        res = self.improvement_model.invoke([
            {'role':'system', 'content':f'Run the test case:{state["test_case"]} on code:{state["code"]}. Provide feedback: If all test cases pass, write a positive comment saying "no-problem".\n'
            '- If any test cases fail, describe: 1. The number of test cases that failed. 2. The expected output vs. the actual output. 3. Any other relevant details to help improve the code.'}
        ])
        log1.info('Appling Test Case')
        return {'user_feedback' : res.improvement_feedback, 'rout' : 'Approve' if res.problems == 'no-problem' else 'Rejected'}

    def Quality_testing(self, state: State):
        st.session_state.state = 'Quality Test'
        res = self.improvement_model.invoke([
            {'role':'system', 'content':f'You are a Senior QA Engineer. Perform a detailed quality analysis of the following code: {state["code"]}\n'
            'Check for the following:\n'
            f'1. Functionality: Does the code fulfill the requirements described in the user story: {state["user_story"]}?\n'
            '2. Performance: Are there any performance bottlenecks or inefficiencies in the code?\n'
            '3. Maintainability: Is the code clean, well-documented, and easy to understand?\n'
            '4. Standards Compliance: Does the code adhere to industry best practices and coding standards?\n'
            'Provide a detailed report highlighting any issues found and suggestions for improvement.'}
        ])
        log1.info('Performed Quality Testing')
        return {'user_feedback': res.improvement_feedback, 'rout' : 'Approve' if res.problems == 'no-problem' else 'Rejected'}    

    def Final_Review(self, state: State):
        st.session_state.state = 'Final Review'
        res = self.code_format_model.invoke([
            {'role': 'system', 'content': f'You are a Senior Software Engineer. Perform a comprehensive maintenance update on the following code: {state["code"]}. Ensure the updated code meets the following criteria:\n'
                                  '1. Readability: Refactor the code to improve readability and maintainability.\n'
                                  '2. Efficiency: Optimize the code for better performance.\n'
                                  '3. Standards: Ensure the code adheres to the latest industry standards and best practices.\n'
                                  '4. Documentation: Add or improve inline comments and documentation for better understanding and future maintenance.\n\n'
                                  'Provide the updated code in the following format:\n'
                                  '1. Updated Code: Include the complete updated code.\n'
                                  '2. Summary: Provide a summary of the changes made.'}
            ])
        log1.info('Final Review')
        # return {'code': res.content}
        return {'code' : res.code, 'file_structure' : res.file_structure}



    #----- Graph -----#
    def graph(self, state):
        graph_ = (
            StateGraph(state)
            .add_node("User Story", self.User_Story)
            .add_node("User Story Feedback", self.User_Story_Sentiment)
            .add_node("Blue Print", self.Create_Documentation)
            .add_node("Blue Print Feedback", self.Create_Documentation_Feedback)
            .add_node("System Feedback", self.System_FeedBack)
            .add_node("Generate Code", self.Generate_Code)
            .add_node("Code Review", self.Code_review)
            .add_node("Security Review", self.Security_review)
            .add_node("Write Test Case", self.Write_test_case)
            .add_node("Test Case Review", self.Test_case_review)
            .add_node("Quality Test", self.Quality_testing)
            .add_node("Final Review", self.Final_Review)

            .add_edge(START, "User Story")
            .add_edge("User Story","User Story Feedback")
            .add_conditional_edges("User Story Feedback", self.Sentiment, {'Approve': 'System Feedback', 'Rejected': 'User Story'})
            .add_edge("System Feedback", "Blue Print")
            .add_edge("Blue Print", "Blue Print Feedback")
            .add_conditional_edges("Blue Print Feedback", self.Sentiment, {'Approve': 'Generate Code', 'Rejected': 'Blue Print'})
            .add_edge("Generate Code", "Code Review")
            .add_conditional_edges("Code Review", self.Sentiment, {'Approve': 'Security Review', 'Rejected': "Generate Code"})
            .add_conditional_edges("Security Review", lambda state: state['rout'], {'Approve': 'Write Test Case', 'Rejected': "Generate Code"})
            .add_edge("Write Test Case", "Test Case Review")
            .add_conditional_edges("Test Case Review", lambda state: state['rout'], {'Approve': 'Quality Test', 'Rejected': "Generate Code"})
            .add_conditional_edges("Quality Test", self.Sentiment, {'Approve': 'Final Review', 'Rejected': "Generate Code"})
            .add_edge("Final Review", END)

            .compile(interrupt_before=["User Story Feedback", "Code Review"], interrupt_after=["Blue Print"], checkpointer=MemorySaver())
        )
        return graph_