import numpy as np
import random
import math
import util

'''Create graph based on (i) in paper.
The graph is a dictionary with nodes as indices and an adjacency
list of nodes on which each depends as values. 
'''

def createGraph(N,sf):
	g00 = 0.003
	g01 = 0.006
	g02 = 0.009
	graph = {0:[]}  # adjacency list
	node = {0:g00}
	igraph = {0:[]} # inverse dependencies -- things that the node contributes to
	degrees = []

	# initialize igraph - not made seqentially
	for x in xrange(1,N):
		igraph[x] = []

	for x in xrange(1,N):

		graph[x] = []  # initialize as an empty list
		# now for type of node
		tmp = random.randint(0,2)
		if tmp == 0:
			node[x] = g00
		elif tmp == 1:
			node[x] = g01
		else:
			node[x] = g02

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
		if len(igraph[x]) == 0:
			nodeval = random.randint(0,N-1)
			graph[nodeval] = [x]
			igraph[x].append(nodeval)

	return graph, node

