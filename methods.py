'''
author: Joshua Christian, r0b0ts.inc
date: Sun 17, june 2018, control lab, unilag.
project: ADAM:The first
file: methods.py

'''

from controller import *

from threading import Thread


def SPEAKER(action):
	T = Thread(target=speak, args=(action,))
	T.start()


