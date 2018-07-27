'''
author: Joshua Christian, r0b0ts.inc
date: Fri 6, july 2018, control lab, unilag.
project: ADAM:The first
file: train.py
'''

# for global import
import sys, os, json
sys.path.append(os.getcwd()+"/lib/")

# framwork import
from adam import ADAM

# developer imports
from controller import *
from functions import *
from functions import _AGENT_VARS
from sensors import Sensors

# other imports
from random import randint

try:
	import cv2
	import numpy as np

except ImportError:
	class cv2:
		pass

	class np:
		pass

#agent states
_AGENT_STATES = _AGENT_VARS["states"]
_AGENT_ACTIONS = _AGENT_VARS["actions"]

AI = ADAM()
SENSES = Sensors()

# prepare training data
trainingData = {"numbers":[], "letters of the alphabet":[]}

leters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
for x in range(30):
    trainingData["numbers"].append("number "+str(x))
    trainingData["numbers"].append(None)
    trainingData["numbers"].append(str(x))
    trainingData["numbers"].append(None)

for x in leters:
    trainingData["letters of the alphabet"].append(x)
    trainingData["letters of the alphabet"].append(None)
    trainingData["letters of the alphabet"].append("letter "+ x)
    trainingData["letters of the alphabet"].append(None)
    trainingData["letters of the alphabet"].append(x + " is a letter")
    trainingData["letters of the alphabet"].append(None)
    trainingData["letters of the alphabet"].append("letter "+ x.upper())
    trainingData["letters of the alphabet"].append(None)


trainingData["program"] = [
	"x is 2", 
	"y is 10",
	"x + y is 12", 
	"y / x is 5",
	"what is the value of x", "2",
	"x is 13",
	"what is x", "x is 13", 
	"y is an even number list", 
	"z is an array for images", 
	"stephen is a blogger",
	"chemical engineering is a course in unilag", 
	"the time is 12 O' clock",
	"what is the time", "12 O' clock",
	"an os is a set of instructions", 
	"a mice is a rodent that lives in dirty stuffy places",
	"a computer is an electronic device", 
	"a flash drive is an electronic device for storing data",
	"what is a computer", "a computer is an electronic device",
	"a saturated solution is a solution that contains more solute than it can dissolve",
	"what is a super saturated solution", "a saturated solution is a solution that contains more solute than it can dissolve in the presence of undissolved solute",
	"what is a saturated solution", "a saturated solution is a solution that contains more solute than it can dissolve in the presence of undissolved solute",
	"a saturated solution is a solution that contains more solute than it can dissolve in the presence of undissolved solute",

]

def train(topic, no_iterations=1):
	for iteration in range(no_iterations):
		print("Iteration {}".format(iteration+1))
		
		# set sensors to null
		terminal_data_before, terminal_data = None, None
		eye_data_before, eye_data = None, None
		ear_data_before, ear_data = None, None
		
		for inp in trainingData[topic]:
			terminal_data_before, terminal_data = terminal_data, inp
			eye_data_before, eye_data = eye_data, eye_data
			ear_data_before, ear_data = ear_data, ear_data

			if type(inp) == list and len(inp) > 1:
				eye_data = readImageFile('res/colours/{}.jpg'.format(inp[1]))


			data = {
				"ear": [ear_data_before, ear_data],
				"eye" : [eye_data_before, eye_data],
				"terminal" : [terminal_data_before, terminal_data]
			}

			# if i == 0:
			print("processing data=>")
			for x in data:
				if type(data[x][1]) == np.ndarray:
					disp = [image_before, image]

				else:
					disp = data[x]

				print("{} = {}".format(x, disp))
			

			AI.process(data)
			print()
			if terminal_data.lower().startswith("what"):
				input()