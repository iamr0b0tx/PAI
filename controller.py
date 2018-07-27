'''
author: Joshua Christian, r0b0ts.inc
date: Sun 17, june 2018, control lab, unilag.
project: ADAM:The first
file: controller.py

'''
from random import randint
from functions import _AGENT_VARS

#agent states
_AGENT_STATES = _AGENT_VARS["states"]
_AGENT_ACTIONS = _AGENT_VARS["actions"]

def speak(output):
    with open('output.txt', 'w') as f:
    	f.write(output)
    