import numpy as np
import random
import math
import time
from matplotlib import pyplot as plt
import seaborn
import util
import processGraph
import constructGraph
import mortalityCurve
import sys

'''Create, age, and process networks.'''

# read in arguments from command line
# N, gamma_0, gamma_1, d, num_trials, sf, frailty, save_graph, mortality_curve, vitality_cutoff
# arg_list = sys.argv

# N = int(arg_list[1])
# gamma_0 = float(arg_list[2])
# gamma_1 = float(arg_list[3])
# d = float(arg_list[4])
# num_trials = int(arg_list[5])
# sf = arg_list[6]
# frailty = bool(int(arg_list[7]))
# save_graph = bool(int(arg_list[8]))
# mortality_curve = bool(int(arg_list[9]))
# vitality_cutoff = float(arg_list[10])

# # define parameters
# N = 5000  # number of nodes
# gamma_0 = 0.005  # failure rate << 1
# gamma_1 = 0.001 #0.002  # repair rate << 1
# d = 0.0  # initial fraction of nonfunctional nodes
# num_trials = 100  # number of trials to run
# sf = 'r'  # scale-free ('sf') vs. random ('r')
# frailty = True  # frailty - load large graph or generate graphs
# save_graph = False  # save the graph or not
# mortality_curve = False  # run mortality curve analysis
# vitality_cutoff = 0.05  # for mortality analysis

def createGraph(N,sf):
	graph = {0:[]}  # adjacency list
	igraph = {0:[]} # inverse dependencies -- things that the node contributes to
	degrees = []

	# initialize igraph - not made seqentially
	for x in xrange(1,N):
		igraph[x] = []

	for x in xrange(1,N):

		graph[x] = []  # initialize as an empty list

		# make copy of degree list to get deg dists
		degrees_dist = list(degrees)

		# first node: set first and zeroth to be interdependent
		if sum(degrees_dist) == 0:
			graph[x] = [0]
			graph[0] = [x]
			igraph[0] = [x]
			igraph[x] = [0]
			degrees.append(1)

		else:
			if sf == 'sf':
				# create dependencies
				total_deg = float(sum(degrees))
				for ix, d in enumerate(degrees):
					if random.random() < d / total_deg:
						graph[x].append(ix)
						igraph[ix].append(x)
					if random.random() < d / total_deg:
						graph[ix].append(x)
						igraph[x].append(ix)
						degrees[ix] += 1
						total_deg += 1
			else:
				# create dependencies
				cutoff = 0.005
				for ix, d in enumerate(degrees):
					if random.random() < cutoff:
						graph[x].append(ix)
						igraph[ix].append(x)
					if random.random() < cutoff:
						graph[ix].append(x)
						igraph[x].append(ix)
						degrees[ix] += 1

		# if no backwards linkages are made, randomly create one
		if len(graph[x]) == 0:
			q = util.weightedChoice(degrees_dist)
			graph[x] = [q]
			igraph[q] = [x]


		# update degrees
		degrees.append(len(graph[x]))

	# get rid of repeats in igraph
	# make sure graph is completely connected
	for x in igraph:
		igraph[x] = list(set(igraph[x]))
		# if len(igraph[x]) == 0:
		# 	node = random.randint(0,N-1)
		# 	graph[node] = [x]
		# 	igraph[x].append(node)

	return graph, degrees

g,d = createGraph(5000,'r')

# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)
# ax.set_yscale('log')
# ax.set_xscale('log')

plt.hist(d,bins=90)
plt.show()
