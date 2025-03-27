from src.share import State
from src.structure import graph
from src.log.logger import logging

test_log = logging.getLogger('Test_Run')
test_log.setLevel(logging.DEBUG)

user_requirement_input = 'Snake Game'
initial_input = {'user_requirement_input': user_requirement_input}
config = {'configurable':{'thread_id':'01'}}

test_log.debug('Invoking')

graph = graph(State)
graph.invoke(input=initial_input, config=config)
# for state in graph.stream(input= initial_input, config= config):
#     # print('state', state)
#     pass
test_log.debug('Interrupt after User_story')
    #--- Interrupt 
state = graph.get_state(config)  # sanapshot
# print(state)
print('User story---------------------------------\n',state.values.get('user_story'))


user_feedback = input('Enter user feedback: ')
graph.update_state(config= config, values= {'user_feedback':user_feedback})


graph.invoke(None, config=config)
# for state in graph.stream(None, config= config):
#     pass
# test_log.debug('Interrupt after Blue Print')
# #--- Interrupt after Create Blue Print
state = graph.get_state(config)
# print('\nSystem Feedback\n',state.values.get('user_story'))
# print('\nUser Story after\n', state.values.get('user_story'))
print('\nSystem Feedback----------------------\n', state.values.get('user_story'))
print('\nBlue Print---------------------\n', state.values.get('blue_print'))
# print('\n',state)


user_feedback = input('Enter user feedback Blue print: ')
graph.update_state(config= config, values= {'user_feedback':user_feedback})

graph.invoke(None, config=config)
# for state in graph.stream(None, config= config):
#     pass
state = graph.get_state(config)
print('code --> \n',state.values.get('code'))

from PIL import Image

data = graph.get_graph().draw_mermaid_png()
image = r'D:\krish\llm_app\flow.png'
with open(image, 'wb') as f:
    f.write(data)
Image.open(image).show()