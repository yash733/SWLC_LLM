from pydantic import BaseModel, Field
from typing import TypedDict, Literal

class State(TypedDict):
    user_requirement_input : str    #user requirements input 
    user_story : str
    user_feedback : str
    # system_feedback : str
    blue_print : str
    code : str
    file_structure : str
    test_case : str

#----- User Feedback Ananlysis -----#
class Feedback(BaseModel):
    grade : Literal['positive', 'negative']
    user_feedback : str = Field(description= "Holds the feedback input gathered from client or agent generated")

class Improvement(BaseModel):
    problems : Literal['problem','no problem'] = Field(description= 'Problems found or not')
    improvement_feedback : str = Field(description= "Contains Problem's along with threir solution.")

#----- Structuring Code Output -----#
class Code(BaseModel):
    code : str = Field(description= 'Holds the code written in each file.')

class Code_Format(BaseModel):
    file_structure : str = Field(description= 'Holds the file structure of the code in hierarchical format.')
    code : list[Code] = Field(description= 'Collection of all code present under different files.')
