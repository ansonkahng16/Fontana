import numpy as np
import random
import math
from matplotlib import pyplot as plt
import seaborn
import csv
import cPickle as pickle

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

	# write figure to png file
	plt_filename = './data/'+sf_str[sf]+'_'+str(N)+'_'+str(num_trials)+'.png'
	plt.savefig(plt_filename)

	# write vitality data to CSV file
	csv_filename = './data/'+sf_str[sf]+'_'+str(N)+'_'+str(num_trials)+'.csv'
	with open(csv_filename, 'wb') as f:
		writer = csv.writer(f)
		writer.writerows(vitality_data)


# write graph to cPickle file
def saveGraph(graph,N,sf,sf_str):
	graph_filename = './data/'+sf_str[sf]+'_'+str(N)+'.pkl'
	output = open(graph_filename, 'wb')
	pickle.dump(graph, output, protocol=2)


# load graph from cPickle file
def loadGraph(N,sf,sf_str):
	graph_filename = './data/'+sf_str[sf]+'_'+str(N)+'.pkl'
	graph = pickle.load(open(graph_filename,'rb'))
	return graph