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

'''Create, age, and process networks.'''


# define parameters
N = 700  # number of nodes
gamma_0 = 0.01  # failure rate << 1
gamma_1 = 0.0045 #0.002  # repair rate << 1
d = 0.024  # initial fraction of nonfunctional nodes
num_trials = 100  # number of trials to run
sf = 'r'  # scale-free ('sf') vs. random ('r')
frailty = True  # frailty - load large graph or generate graphs
save_graph = False  # save the graph or not
mortality_curve = False  # run mortality curve analysis
vitality_cutoff = 0.05  # for mortality analysis


def saveGraph():
	graph = constructGraph.createGraph(N,sf)
	util.saveGraph(graph,N,sf)

def main():
	t0 = time.time()

	if not(mortality_curve):

		if save_graph:
			saveGraph()

		else:
			# run experiment many times and gather vitality data
			vitality_data = []
			if frailty:  # generate graph each time
				for n in xrange(0,num_trials):
					graph = constructGraph.createGraph(N,sf)
					t11 = time.time()
					lifespan, vitality = processGraph.ageGraph(graph,d,gamma_0,gamma_1,N)
					print time.time() - t11
					vitality_data.append(vitality)
					if n % 5 == 0:
						print n
			else:  # no frailty - use same (larger) graph and run many simulations
				graph = util.loadGraph(N,sf)
				print 'graph loaded'
				for n in xrange(0,num_trials):
					tic = time.time()
					# takes an obscenely long time for small gamma_0 and large N
					# remember to run overnight!
					lifespan, vitality = processGraph.ageGraph(graph,d,gamma_0,gamma_1,N)
					toc = time.time()
					print toc - tic
					vitality_data.append(vitality)
					if n % 5 == 0:
						print n

			util.graphResults(vitality_data,N,num_trials,sf,gamma_0,gamma_1,d)

	else:
		fpt = mortalityCurve.plotMortalityCurve(N,num_trials,sf,vitality_cutoff,gamma_0,gamma_1,d)
		mortalityCurve.plotMortalityRate(fpt, N,num_trials,sf,vitality_cutoff,gamma_0,gamma_1,d)

	t1 = time.time()
	print 'time: ', t1 - t0


if __name__ == '__main__':
	main()