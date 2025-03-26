#----- Libraries -----#
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver

#----- Dependencies -----#
from share import State, Feedback
from log.logger import logging

#----- LLM -- Model -----#
model = ChatGroq(model = "llama3-70b-8192")

   #----- LLM -- Structured -- Output -----#
feed_back_model = model.with_structured_output(Feedback)

#----- Setup -----#
load_dotenv()

os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_PROJECT'] = 'llm-app'
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

log1 = logging.getLogger('Update')
log1.setLevel(logging.DEBUG)

log2 = logging.getLogger('Error')
log2.setLevel(logging.INFO)

#----- Structure -----#

def User_Story(state: State):
    if state.get('user_feedback') and state.get('user_story'):
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

def Sentiment(state: State):
    res = feed_back_model.invoke([
        {'role':'system','content':'Understand the clint feedback.'},
        {'role':'user', 'content':f"Clients feedback: {state['user_feedback']}"}
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
        {'role':'system', 'content':f'You are Senior most Product Owner, after mutiple talks with the client the user story looks like this:{state["user_story"]}\n'
        'as being a senior product owner refine the user story, validate each and every point so the project can move to next stage of creating blue print/design document.'}
    ])
    log1.info('System_FeedBack - User Story')
    return {"user_story" : res.content}

def Create_Documentation(state: State):
    if state.get('blue_print') and state.get('user_feedback'):
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

def Generate_Code(state: State):
    res = model.invoke([
        {'role':'system','content':f'Setup file structure and write code, with the help of user story:{state["user_story"]} and design document:{state["blue_print"]}]'}
    ])
    log1.info('Generate Code')
    return {'code' : res.content}

def Code_review(state: State):
    pass



#----- Graph -----#
def graph():
    graph_ = (
        StateGraph
        .add_node("User Story", User_Story)
        .add_node("Blue Print", Create_Documentation)
        .add_node("System Feedback", System_FeedBack)
        .add_node("Generate Code", Generate_Code)
        .add_conditional_edges("User Story", Sentiment, {'Approve': 'System Feedback', 'Rejected': 'User Story'})
        .add_edge("System Feedback", "Blue Print")
        .add_conditional_edges("Blue Print", Sentiment, {'Approve': 'Generate Code', 'Rejected': 'Blue Print'})
        .add_edge('Generate Code',END)
        .compile(interrupt_after=[User_Story,Create_Documentation], checkpointer = MemorySaver())
    )
    return graph_