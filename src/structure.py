#----- Libraries -----#
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver

#----- Dependencies -----#
from src.share import State, Feedback, Code_Format, Improvement
from src.log.logger import logging

#----- LLM -- Model -----#
model = ChatGroq(model = "llama3-70b-8192")

   #----- LLM -- Structured -- Output -----#
feed_back_model = model.with_structured_output(Feedback)
code_format_model = model.with_structured_output(Code_Format)
improvement_model = model.with_structured_output(Improvement)

#----- Setup -----#
load_dotenv()

os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_PROJECT'] = 'llm-app'
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

log1 = logging.getLogger('Update-Structure')
log1.setLevel(logging.DEBUG)

log2 = logging.getLogger('Error-Structure')
log2.setLevel(logging.INFO)

#----- Structure -----#

def User_Story(state: State):
    if state.get('user_story'):
        res = model.invoke([ 
            {'role':'system', 'content':f"You are a Senior Product Owner. First analyzise the user story: {state['user_story']}. Now make necessary changes catering to \n"
            f"clients feedback: {state['user_feedback']}"}
        ])
        log1.info('Implemented Clients feedback - User Story')
    else:
        res = model.invoke([ 
            {'role':'system', 'content':"You are a Senior Product Owner generate a user story. It is a short, informal description of a desired feature or functionality,\n"
            " written from the end-user's perspective, to help developers/engineers understand user needs and requirements."},
            {'role':'user', 'content':f'User requirement: {state["user_requirement_input"]}'}
        ])
        log1.info('Genrated - User Story')
    return {'user_story': res.content}
    
 #------ Interrupt will happen, input: user feedback -----#
def User_Story_Sentiment(state: State):
    return state

def Sentiment(state: State):
    res = feed_back_model.invoke([
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

def System_FeedBack(state: State):
    res = model.invoke([
        {'role':'system', 'content':f'You are Senior most Product Owner'},
        {'role':'system', 'content':f'After mutiple talks with the client the user story looks like this:{state["user_story"]} as being a senior product owner \n'
        'refine the user story, validate each and every point so the project can move to next stage of creating blue print/design document.'}
    ])
    log1.info('System_FeedBack - User Story')
    return {"user_story" : res.content}

def Create_Documentation(state: State):
    if state.get('blue_print'):
        res = model.invoke([
            {'role':'system', 'content':f'Given the following user story:{state["user_story"]} and user feedback:{state["user_feedback"]}, improve the generated detailed design \n'
            f'document:{state["blue_print"]}, covering both High-Level Design (HLD) and Low-Level Design (LLD)'}
        ])
        log1.info('User Feedback - Blue Print')
    else:
        res = model.invoke([
            {'role':'system','content':f'Given the following user story:{state["user_story"]}, generate a detailed design document covering both High-Level Design (HLD) \n'
            'and Low-Level Design (LLD)'}
        ])
        log1.info('Created - Blue Print')
    return {'blue_print' : res.content}
    #------ Interrupt will happen, input: user feedback -----#

def Create_Documentation_Feedback(state: State):
    log1.info('Feedback - Blue Print')
    return state

def Generate_Code(state: State):
    if state.get('code'):
        res = code_format_model.invoke([
            {'role':'system', 'content':f'This is previous code: {state["code"]} and file structure: {state["file_structure"]}. Now analyze the feedback prvided by tech lead and client: {state["user_feedback"]} to improve upon.'}
        ])
        log1.info('Feedback - Generate Code')
    
    else:
        res = code_format_model.invoke([
            {'role':'system','content':f'Setup file structure(in hierarchical form) and write code, with the help of user story:{state["user_story"]} and design document:{state["blue_print"]}]'}
        ])
        log1.info('Generate Code')
    return {'code' : res.code, 'file_structure' : res.file_structure}

 #------ Interrupt will happen, input: user feedback -----#
def Code_review(state: State):
    res = model.invoke([
        {'role':'system', 'content':f'You are tech lead "prvide feedback". Analyse the code: {state["code"]} and file structure: {state["file_structure"]}. Now check for any sort of bugs, errors or issues \n'
        'in the code or file format/structuring. Also take client feedback under consideration if any improvemnet is required.'},
        {'role':'user', 'content':f'Client Feedback: {state["user_feedback"]}'}
    ])
    log1.info('Code review')
    return {'user_feedback' : res.content}

def Security_review(state: State):
    res = model.invoke([
        {'role':'system', 'content':f'You are Tech Lead, carefully analyze the the code: {state["code"]}, look for security lapes and its possibilites.'}
    ])
    log1.info('Security review')
    return {'user_feedback' : res.content}

def Write_test_case(state: State):
    res = model.invoke([
        {'role':'system', 'content':f'Generate test cases undermining, client requiremrnt: {state["user_requirement_input"]}, user_story:{state["user_story"]} and software blue print:{state["blue_print"]}\n'
        'Ensure the test cases cover all functional, edge, and boundary scenarios.'}
    ])
    log1.info('Ceating Test Case')
    return {'test_case' : res.content}

def Test_case_review(state: State):
    res = model.invoke([
        {'role':'system', 'content':f'Run the test case:{state["test_case"]} on code:{state["code"]}. Provide feedback: If all test cases pass, write a positive comment.\n'
        '- If any test cases fail, describe: 1. The number of test cases that failed. 2. The expected output vs. the actual output. 3. Any other relevant details to help improve the code.'}
    ])
    log1.info('Appling Test Case')
    return {'user_feedback' : res.content}

def Quality_testing(state: State):
    res = model.invoke([
        {'role':'system', 'content':f'You are a Senior QA Engineer. Perform a detailed quality analysis of the following code: {state["code"]}\n'
        'Check for the following:\n'
        f'1. Functionality: Does the code fulfill the requirements described in the user story: {state["user_story"]}?\n'
        '2. Performance: Are there any performance bottlenecks or inefficiencies in the code?\n'
        '3. Maintainability: Is the code clean, well-documented, and easy to understand?\n'
        '4. Standards Compliance: Does the code adhere to industry best practices and coding standards?\n'
        'Provide a detailed report highlighting any issues found and suggestions for improvement.'}
    ])
    log1.info('Performed Quality Testing')
    return {'user_feedback': res.content}    

def Maintenance_Update(state: State):
    pass



#----- Graph -----#
def graph(state: State):
    graph_ = (
        StateGraph(state)
        .add_node("User Story", User_Story)
        .add_node("User Story Feedback",User_Story_Sentiment)
        .add_node("Blue Print", Create_Documentation)
        .add_node("Blue Print Feedback", Create_Documentation_Feedback)
        .add_node("System Feedback", System_FeedBack)
        .add_node("Generate Code", Generate_Code)
        .add_node("Code Review", Code_review)
        .add_node("Security Review", Security_review)
        .add_node("Write Test Case", Write_test_case)
        .add_node("Test Case Review", Test_case_review)
        .add_node("Quality Test", Quality_testing)
        .add_node("Maintenance Update", Maintenance_Update)

        .add_edge(START, "User Story")
        .add_edge("User Story","User Story Feedback")
        .add_conditional_edges("User Story Feedback", Sentiment, {'Approve': 'System Feedback', 'Rejected': 'User Story'})
        .add_edge("System Feedback", "Blue Print")
        .add_edge("Blue Print", "Blue Print Feedback")
        .add_conditional_edges("Blue Print Feedback", Sentiment, {'Approve': 'Generate Code', 'Rejected': 'Blue Print'})
        .add_edge("Generate Code", "Code Review")
        .add_conditional_edges("Code Review", Sentiment, {'Approve': 'Security Review', 'Rejected': "Generate Code"})
        .add_conditional_edges("Security Review", Sentiment, {'Approve': 'Write Test Case', 'Rejected': "Generate Code"})
        .add_edge("Write Test Case", "Test Case Review")
        .add_conditional_edges("Test Case Review", Sentiment, {'Approve': 'Quality Test', 'Rejected': "Generate Code"})
        .add_conditional_edges("Quality Test", Sentiment, {'Approve': 'Maintenance Update', 'Rejected': "Generate Code"})
        .add_edge("Maintenance Update",)

        .compile(interrupt_before=["User Story Feedback", "Code Review"], interrupt_after=["Blue Print"], checkpointer=MemorySaver())
    )
    return graph_