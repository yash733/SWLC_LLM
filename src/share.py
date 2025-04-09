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
    file_name : str
    test_case : str
    rout : Literal['problem','no problem']
    tech_stack : list[str]

#----- User Feedback Ananlysis -----#
class Feedback(BaseModel):
    grade : Literal['positive', 'negative']
    user_feedback : str = Field(description= "Holds the feedback input gathered from client or agent generated")

class Improvement(BaseModel):
    problems : Literal['problem','no-problem'] = Field(description= 'Problems found or not')
    improvement_feedback : str = Field(description= "Contains proper in deatailed description of problem's along with threir solutions.")

#----- Structuring Code Output -----#
class Code(BaseModel):
    file_name : str = Field(description= 'name of code file')
    code : str = Field(description= 'Code under the file_name.')

class Code_Format(BaseModel):
    file_structure : str = Field(description= 'Represents the file_name in hierarchical format in markdown.')
    code : list[Code] = Field(description= 'All code present under different files, with file_name in markdown.')