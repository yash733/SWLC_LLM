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
    res = model.invoke([ 
        {'role':'system', 'content':"You are a senior Product Owner generate a user story. It is a short, informal description of a desired feature or functionality,\n"
        " written from the end-user's perspective, to help sofware/application/web developers/engineers understand user needs and requirements."},
        {'role':'user', 'content':f'User requirement: {state["user_requirement_input"]}'}
    ])
    log1.info('Genrated User Story')
    return {'user_story': res.content}

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
    return 'Fail'

def Create_Documentation(state: State):
    pass

def Generate_Code(state: State):
    pass

def Code_review(state: State):
    pass



#----- Graph -----#
def graph():
    graph_ = (
        StateGraph
        .add_node("User Story", User_Story)
        .add_node("Blue Print", Create_Documentation)
        .add_node("Generate Code", Generate_Code)
        .add_conditional_edges("User Story", Sentiment, {'Approve': 'Blue Print', 'Fail': 'User Story'})
        .add_conditional_edges("Blue Print", Sentiment, {'Pass': 'Generate Code', 'Fail': 'Blue Print'})

        .compile(interrupt_after=[User_Story], checkpointer = MemorySaver())
    )
    return graph_