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
arg_list = sys.argv

N = int(arg_list[1])
gamma_0 = float(arg_list[2])
gamma_1 = float(arg_list[3])
d = float(arg_list[4])
num_trials = int(arg_list[5])
sf = arg_list[6]
frailty = bool(int(arg_list[7]))
save_graph = bool(int(arg_list[8]))
mortality_curve = bool(int(arg_list[9]))
vitality_cutoff = float(arg_list[10])

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
					graph, node = constructGraph.createGraph(N,sf)
					lifespan, vitality = processGraph.ageGraph(graph,d,gamma_0,gamma_1,N,node)
					vitality_data.append(vitality)
					if n % 5 == 0:
						print n
			else:  # no frailty - use same (larger) graph and run many simulations
				graph = util.loadGraph(N,sf)  # have to fix this for three types of nodes!!
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