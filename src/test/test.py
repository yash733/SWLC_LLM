from src.share import State
from src.structure import graph
from src.log.logger import logging

test_log = logging.getLogger('Test_Run')
test_log.setLevel(logging.DEBUG)

user_requirement_input = 'Snake Game'
initial_input = {'user_requirement_input': user_requirement_input, 'tech_stack': ['python']}
config = {'configurable':{'thread_id':'01'}}

test_log.debug('Invoking')

graph = graph(State)
graph.invoke(input=initial_input, config=config)

test_log.debug('Interrupt after User_story')
    #--- Interrupt 
state = graph.get_state(config)  # sanapshot
print('User story: \n',state.values.get('user_story'))
user_feedback = input('Enter user feedback: ')
graph.update_state(config= config, values= {'user_feedback':user_feedback})


graph.invoke(None, config=config)

    #--- Interrupt after Create Blue Print
state = graph.get_state(config)
print('='*100)
print('\nSystem Feedback: \n', state.values.get('user_story'))
print('='*100)
print('\nBlue Print: \n', state.values.get('blue_print'))

user_feedback = input('Enter user feedback Blue print: ')
graph.update_state(config= config, values= {'user_feedback':user_feedback})

graph.invoke(None, config=config)

state = graph.get_state(config)
print('='*100)
print('code --> \n',state.values.get('code'))

# print('X'*100)
# print(state) # sanapshot

graph.invoke(None, config=config)
user_feedback = input('Enter user feedback Code Review: ')
graph.update_state(config= config, values= {'user_feedback':user_feedback})

graph.invoke(None, config=config)

state = graph.get_state(config)
print('='*100)
print('\nTest Cases: \n',state.values.get('test_case'))
print('='*100)
print('\nFinal Code: \n',state.values.get('code'))
print('='*100)
print('\nFile Structure\n', state.values.get('file_structure'))




from PIL import Image

data = graph.get_graph().draw_mermaid_png()
image = r'D:\krish\llm_app\flow.png'
with open(image, 'wb') as f:
    f.write(data)
Image.open(image).show()