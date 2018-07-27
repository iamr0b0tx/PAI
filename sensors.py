'''
author: Joshua Christian, r0b0ts.inc
date: Fri 6, july 2018, control lab, unilag.
project: ADAM:The first
file: adam.py

'''

from functions import _AGENT_VARS


##constants
_AGENT_STATES = _AGENT_VARS["states"]
_AGENT_SENSORS = _AGENT_VARS["sensors"]

class Sensors:
	def sense(self):
		data = {}
		for s in _AGENT_SENSORS:
			data[s] = eval("{}()".format(s))
		
		return data

def eye():
	return ''

def ear():
	return ''

def terminal():
	return input("\\> ")