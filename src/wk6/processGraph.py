import numpy as np
import random
import math
from matplotlib import pyplot as plt
import time

'''Age graph based on (ii) in paper.
Input: graph
Output: lifespan (time before vitality < 0.01),
		vitality (vitality at every unit time)
'''


def ageGraph(graph,d,gamma_0,gamma_1,N,node):
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
				if tmp < node[i]:
					func[i] = 0
			elif func[i] == 0:
				if tmp < gamma_1:
					func[i] = 1

		# calculate dependencies, break accordingly
		# recursively repeat until no new broken nodes
		# each loops takes ~1 second for 50K nodes; too slow!
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
