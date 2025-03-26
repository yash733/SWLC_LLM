from pydantic import BaseModel, Field
from typing import TypedDict, Literal

class State(TypedDict):
    user_requirement_input : str    #user requirements input 
    user_story : str
    user_feedback : str
    system_feedback : str
    blue_print : str
    code : str


#----- User Feedback Ananlysis -----#
class Feedback(BaseModel):
    grade : Literal['positive', 'negative']
    user_feedback : str = Field(description= "Holds the feedback input gathered from client or agent generated")

