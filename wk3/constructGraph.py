import numpy as np
import random
import math
import util

'''Create graph based on (i) in paper.
The graph is a dictionary with nodes as indices and an adjacency
list of nodes on which each depends as values. 
'''

# create / initialize graph based on (i) in paper
def createGraph(N,sf):
	graph = {0:[]}  # adjacency list
	degrees = []

	for x in xrange(1,N):

		graph[x] = []  # initialize as an empty list

		# make copy of degree list to get deg dists
		degrees_dist = list(degrees)

		# first node: set first and zeroth to be interdependent
		if sum(degrees_dist) == 0:
			graph[x] = [0]
			graph[0] = [x]
			degrees.append(1)

		else:
			if sf == True:
				# create dependencies
				total_deg = float(sum(degrees))
				for ix, d in enumerate(degrees):
					if random.random() < d / total_deg:
						graph[x].append(ix)
					if random.random() < d / total_deg:
						graph[ix].append(x)
						degrees[ix] += 1
						total_deg += 1
			else:
				# create dependencies
				cutoff = 1 / float(len(degrees))
				for ix, d in enumerate(degrees):
					if random.random() < cutoff:
						graph[x].append(ix)
					if random.random() < cutoff:
						graph[ix].append(x)
						degrees[ix] += 1

		# if no backwards linkages are made, randomly create one
		if len(graph[x]) == 0:
			graph[x] = [util.weightedChoice(degrees_dist)]

		# update degrees
		degrees.append(len(graph[x]))

	return graph