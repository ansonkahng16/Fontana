import numpy as np
import random
import math
import time
from matplotlib import pyplot as plt
import seaborn
import util
import processGraph
import constructGraph

'''Create, age, and process networks.'''


# define parameters
N = 5000  # number of nodes
gamma_0 = 0.01  # failure rate << 1
gamma_1 = 0 #0.002  # repair rate << 1
d = 0.02  # initial fraction of nonfunctional nodes
num_trials = 100  # number of trials to run
sf = False  # scale-free (T) vs. random (F)
sf_str = {True: 'sf', False: 'r'}  # dictionary to map sf attr to string


def main():
	t0 = time.time()

	# run the experiment many times and gather vitality data
	vitality_data = []
	graph = constructGraph.createGraph(N,sf)
	# graph = util.loadGraph(N,sf,sf_str)

	# util.saveGraph(graph,N,sf,sf_str)

	for n in xrange(0,num_trials):
		# graph = createGraph(N)
		# tb = time.time()
		lifespan, vitality = processGraph.ageGraph(graph,d,gamma_0,gamma_1,N)
		# print 'age', time.time() - tb
		vitality_data.append(vitality)
		if n % 5 == 0:
			print n
		# print n

	util.graphResults(vitality_data,N,num_trials,sf,sf_str)

	t1 = time.time()
	print t1 - t0

if __name__ == '__main__':
	main()