import numpy as np
import random
import math
import util

'''Create graph based on (i) in paper.
The graph is a dictionary with nodes as indices and an adjacency
list of nodes on which each depends as values. 
'''

# create / initialize graph based on (i) in paper
# def createGraph(N,sf):
# 	graph = {0:[]}  # adjacency list
# 	degrees = []

# 	for x in xrange(1,N):

# 		graph[x] = []  # initialize as an empty list

# 		# make copy of degree list to get deg dists
# 		degrees_dist = list(degrees)

# 		# first node: set first and zeroth to be interdependent
# 		if sum(degrees_dist) == 0:
# 			graph[x] = [0]
# 			graph[0] = [x]
# 			degrees.append(1)

# 		else:
# 			if sf == True:
# 				# create dependencies
# 				total_deg = float(sum(degrees))
# 				for ix, d in enumerate(degrees):
# 					if random.random() < d / total_deg:
# 						graph[x].append(ix)
# 					if random.random() < d / total_deg:
# 						graph[ix].append(x)
# 						degrees[ix] += 1
# 						total_deg += 1
# 			else:
# 				# create dependencies
# 				cutoff = 1 / float(len(degrees))
# 				for ix, d in enumerate(degrees):
# 					if random.random() < cutoff:
# 						graph[x].append(ix)
# 					if random.random() < cutoff:
# 						graph[ix].append(x)
# 						degrees[ix] += 1

# 		# if no backwards linkages are made, randomly create one
# 		if len(graph[x]) == 0:
# 			graph[x] = [util.weightedChoice(degrees_dist)]

# 		# update degrees
# 		degrees.append(len(graph[x]))

# 	return graph

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
			if sf == True:
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
				cutoff = 1 / float(len(degrees))
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
	for x in igraph:
		igraph[x] = list(set(igraph[x]))


	# make sure that the graph is completely connected
	# always completely random -- change later?
	for elt in igraph:
		if len(igraph[elt]) == 0:
			node = random.randint(0,N-1)
			graph[node] = [elt]
			igraph[elt].append(node)
			
	lens = []
	for x in igraph:
		lens.append(len(igraph[x]))
	print lens

	return graph