import numpy as np
import random
import math
from matplotlib import pyplot as plt
import seaborn

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

# graph + record results
def graphResults(vitality_data,N,num_trials,sf,sf_str):
	for v in vitality_data:
		xs = np.array(range(0,len(v)))
		plt.plot(xs,v)
	plt.title('Vitality vs. Time')
	plt.ylabel('Vitality (%)')
	plt.xlabel('Time (timesteps)')

	#plt.show()

	filename = './data/'+sf_str[sf]+'_'+str(N)+'_'+str(num_trials)+'.png'
	plt.savefig(filename)
