import numpy as np
import random
import math
import time
from matplotlib import pyplot as plt

# define parameters
N = 1000  # number of nodes
gamma_0 = 0.01  # failure rate << 1
gamma_1 = 0.002  # repair rate << 1
d = 0.02  # initial fraction of nonfunctional nodes
num_trials = 1  # number of trials to run

# weighted choice function for making graph
def weightedChoice(choices):
   total = sum(choices)
   r = random.uniform(0, total)
   upto = 0
   for i,c in enumerate(choices):
      if upto + c > r:
         return i
      upto += c

# create / initialize graph based on (i) in paper
def createGraph(N):
	t0 = time.time()
	graph = {0:[]}  # adjacency list
	degrees = []

	for x in xrange(1,N):
	    # get degree of each vertex
	    # for g in graph:
	    #     degrees.append(len(graph[g]))

	    graph[x] = []  # initialize as an empty list

	    # make copy of degree list to get deg dists
	    degrees_dist = list(degrees)

	    # first node: set first and zeroth to be interdependent
	    if sum(degrees_dist) == 0:
	    	graph[x] = [0]
	    	graph[0] = [x]
	    	degrees.append(1)

	    # get probability distribution
	    else:
	    	degrees_dist = [d / float(sum(degrees)) for d in degrees]

	    # create dependencies
	    for ix, d in enumerate(degrees_dist):
	    	if random.random() < d:
	    		graph[x].append(ix)
	    	if random.random() < d:
	    		graph[ix].append(x)
	    		degrees[ix] += 1

	    # if no backwards linkages are made, randomly create one
	    if len(graph[x]) == 0:
	    	graph[x] = [weightedChoice(degrees_dist)]

	    degrees.append(len(graph[x]))


	t1 = time.time()
	print t1-t0

	return graph

def ageGraph(graph):
	# create functional/nonfunctional vector
	# set fraction d of them to 0
	t0 = time.time()
	func = [1]*N
	initialnonfunc = random.sample(range(0,N), int(d*N))
	for n in initialnonfunc:
		func[n] = 0

	# calculate vitality 
	vitality = [sum(func) / float(N)]

	lifespan = 0

	while vitality[-1] > 0.01:
		lifespan += 1

		# update nodes (fix/break them)
		for i in xrange(0,N):
			tmp = random.random()
			if func[i] == 1:
				if tmp < gamma_0:
					func[i] = 0
			if func[i] == 0:
				if tmp < gamma_1:
					func[i] = 1

		# calculate dependencies, break accordingly
		for g in graph:
			ctr = 0
			lg = len(graph[g])
			for dep in graph[g]:  # dependencies
				ctr += func[dep]
			if ctr / float(lg) < 0.5:
				func[g] = 0

		vitality.append(sum(func) / float(N))

	t1 = time.time()

	print t1-t0

	return lifespan, vitality


# run the experiment many times and gather vitality data
vitality_data = []

# graph = createGraph(N)
# lifespan, vitality = ageGraph(graph)

for n in xrange(0,num_trials):
	graph = createGraph(N)
	lifespan, vitality = ageGraph(graph)
	vitality_data.append(vitality)
	print n


for v in vitality_data:
	xs = np.array(range(0,len(v)))
	plt.plot(xs,v)
plt.show()

# xdata0 = np.array(range(0,len(vitality_data[0])))
# xdata1 = np.array(range(0,len(vitality_data[1])))
# # plot the vitality data over time
# plt.plot(xdata0, vitality_data[0])
# plt.plot(xdata1, vitality_data[1])
# plt.show()

