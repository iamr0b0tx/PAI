'''
author: Joshua Christian, r0b0ts.inc
date: Sun 17, june 2018, control lab, unilag.
project: ADAM:The first
file: example.py
'''



# for global import
import sys, os
sys.path.append(os.getcwd()+"/lib/")

# framwork import
from adam import ADAM

#other imports
from functions import _AGENT_VARS
from trainer import *

# functions
def log_dict(d, show=True):
	for x in d:
		print(x)
		for y in d[x]:
			print("  {}=> {}".format(y, d[x][y]))
		print()

#agent states
_AGENT_STATES = _AGENT_VARS["states"]
_AGENT_ACTIONS = _AGENT_VARS["actions"]

AI = ADAM()
SENSORS = Sensors()

# train AI to know its state and actions
for state in _AGENT_ACTIONS:
	actions = _AGENT_ACTIONS[state]
	for action in actions:
		# print(state, action)
		AI.states[state].state = state
		AI.states[state].perform(action)
		
		sensory_data = {} #SENSORS.sense()

		for sense in sensory_data:
			if sensory_data[sense] == action:
				AI.addSenseToState(sense, state)

#train Agent on how to count
train("program")

print('training ended!!!')
print(AI.memory)
log_dict(AI.TextProcessor.memory)

