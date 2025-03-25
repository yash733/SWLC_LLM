from pydantic import BaseModel, Field
from typing import TypedDict, Literal

class State(TypedDict):
    user_requirement_input : str    #user requirements input 
    user_story : str
    user_feedback : str

class Feedback(BaseModel):
    grade : Literal['positive', 'negative']
    user_feedback : str = Field(description= "Holds the feedback input gathered from client to analyze and if required work on refinement")

class System_Feedback(BaseModel):
    grade : Literal['pass', 'fail'] = Field(description= 'Analysing the Feeback generated/provided by systems/agents')
    system_feedback : str = Field(description= 'Feedback genrated/provided by systems/agents')