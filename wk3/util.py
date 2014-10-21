import numpy as np
import random
import math

'''Misc useful functions.'''

# weighted choice function for making graph
def weightedChoice(choices):
   total = sum(choices)
   r = random.uniform(0, total)
   upto = 0
   for i,c in enumerate(choices):
	  if upto + c > r:
		 return i
	  upto += c

