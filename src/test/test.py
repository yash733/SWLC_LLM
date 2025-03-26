# from llm_app.src.share import State
from src.structure import graph
from src.log.logger import logging

test_log = logging.getLogger('Test_Run')
test_log.setLevel(logging.DEBUG)

user_requirement_input = 'Snake Game'
initial_input = {'user_requirement_input': user_requirement_input}
config = {'configurable':{'thread':'01'}}

test_log.debug('Invoking')

graph = graph()
for state in graph.stream(input= initial_input, config= config):
    pass
test_log.debug('Interrupt after User_story')
#--- Interrupt after user Story

print('User_Story', state['user_story'])

user_feedback = input('Enter user feedback: ')
graph.update_state(config= config, values= {'user_feedback':user_feedback})

for state in graph.stream(None, config= config):
    pass
test_log.debug('Interrupt after Blue Print')
#--- Interrupt after Create Blue Print

print('System Feedback', state['system_feedback'])
print('Blue Print', state['blue_print'])

user_feedback = input('Enter user feedback Blue print: ')
graph.update_state(config= config, values= {'user_feedback':user_feedback})

for state in graph.stream(None, config= config):
    pass

print('code',state['code'])