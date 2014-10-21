import numpy as np
import random
import math
import time
from matplotlib import pyplot as plt
import seaborn

# define parameters
N = 5000  # number of nodes
gamma_0 = 0.01  # failure rate << 1
gamma_1 = 0.002  # repair rate << 1
d = 0.02  # initial fraction of nonfunctional nodes
num_trials = 100  # number of trials to run
sf = False  # scale-free (T) vs. random (F)

# dictionary to map sf attr to string
sf_str = {True: 'sf', False: 'r'}

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
			graph[x] = [weightedChoice(degrees_dist)]

		# update degrees
		degrees.append(len(graph[x]))

	return graph

def ageGraph(graph):
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
		# repeat until no new broken nodes
		num_broken = 1
		num_broken_prev = 0
		while num_broken > num_broken_prev:
			num_broken_prev = num_broken
			num_broken = 0
			for g in graph:
				ctr = 0
				lg = len(graph[g])
				for dep in graph[g]:  # dependencies
					ctr += func[dep]
				if ctr / float(lg) < 0.5:
					num_broken += 1
					func[g] = 0


		vitality.append(sum(func) / float(N))

	return lifespan, vitality



def main():

	t0 = time.time()

	# run the experiment many times and gather vitality data
	vitality_data = []

	for n in xrange(0,num_trials):
		# tx = time.time()		
		graph = createGraph(N)
		lifespan, vitality = ageGraph(graph)
		# ty = time.time()
		# print ty-tx
		vitality_data.append(vitality)
		if n % 5 == 0:
			print n
		# print n


	for v in vitality_data:
		xs = np.array(range(0,len(v)))
		plt.plot(xs,v)
	plt.title('Vitality vs. Time')
	plt.ylabel('Vitality (%)')
	plt.xlabel('Time (timesteps)')
	t1 = time.time()
	print t1-t0

	#plt.show()

	filename = './data/'+sf_str[sf]+'_'+str(N)+'_'+str(num_trials)+'.png'
	plt.savefig(filename)


if __name__ == '__main__':
	main()

