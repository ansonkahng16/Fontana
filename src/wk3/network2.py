import numpy as np
import random
import math
import time
from matplotlib import pyplot as plt
import seaborn

'''
This is the same as graph.py but has a different criteria for the
nonfunctionality of nodes. Instead of just having a simple majority
of the nodes determine the functionality of the component, it weights
each of the dependencies by its degree. Now, a majority of the weighted
average is used as a measure of the functionality of nodes.
'''


# define parameters
N = 1000  # number of nodes
gamma_0 = 0.01  # failure rate << 1
gamma_1 = 0.002  # repair rate << 1
d = 0.02  # initial fraction of nonfunctional nodes
num_trials = 100  # number of trials to run
sf = False  # scale-free (T) vs. random (F)

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
			q = weightedChoice(degrees_dist)
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

	return graph, igraph

def ageGraph(graph,igraph):
	# create functional/nonfunctional vector
	# set fraction d of them to 0
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
		num_broken = 1
		num_broken_prev = 0
		while num_broken > num_broken_prev:
			num_broken_prev = num_broken
			num_broken = 0
			for g in graph:
				ctr = 0
				sumg = 0
				for dep in graph[g]:  # dependencies
					ctr += func[dep] * len(igraph[dep])
					sumg += len(igraph[dep])
				# print sumg
				if ctr / sumg < 0.5:
					func[g] = 0

		vitality.append(sum(func) / float(N))

	return lifespan, vitality



def main():

	t0 = time.time()

	# run the experiment many times and gather vitality data
	vitality_data = []

	for n in xrange(0,num_trials):
		graph,igraph = createGraph(N)
		lifespan, vitality = ageGraph(graph,igraph)
		vitality_data.append(vitality)
		if n % 5 == 0:
			print n


	for v in vitality_data:
		xs = np.array(range(0,len(v)))
		plt.plot(xs,v)
	plt.title('Vitality vs. Time')
	plt.ylabel('Vitality (%)')
	plt.xlabel('Time (timesteps)')
	t1 = time.time()
	print t1-t0

	plt.show()


if __name__ == '__main__':
	main()

