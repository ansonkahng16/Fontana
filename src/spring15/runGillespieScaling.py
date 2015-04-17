import numpy as np
import random
import math
from matplotlib import pyplot as plt
import seaborn as sns
import time
import sys
import copy
import csv
import os

# CONSTANTS
gamma_0 = float(sys.argv[1])
# gamma_0 = 0.05
gamma_1 = 0.0
gamma_0_new = 0.05
gamma_1_new = 0.0

## Node structure
class Node:
	def __init__(self,name,t,dep,idep,depnodes,idepnodes,deg,ideg,g0,g1,func):
		self.name = name
		self.t = t
		self.dep = dep
		self.idep = idep
		self.depnodes = depnodes
		self.idepnodes = idepnodes
		self.deg = deg
		self.ideg = ideg
		self.g0 = g0
		self.g1 = g1
		self.func = func

## Graph = list of nodes
class Graph:
	def __init__(self,n,t,sf,d,vitality,lifespan,nodes):
		self.n = n
		self.t = t
		self.sf = sf
		self.d = d
		self.vitality = vitality
		self.lifespan = lifespan
		self.nodes = nodes

# helper function to set dependencies
def setDependency(a,b):  # node a depends on node b
	a.dep.append(b.name)
	b.idep.append(a.name)
	a.deg += 1
	b.ideg += 1

# helper function to get pct functionality of all nodes a depends on
def getFunc(graph,a):  # a = node
	depfuncs = []
	for dep in a.dep:
		depfuncs.append(graph.nodes[dep].func)

	pctfunc = sum(depfuncs) / float(len(depfuncs))

	return pctfunc

# helper function to get total rate for Gillespie step
def getTotalRate(g):  # g = graph
	totalrate = 0
	noderates = []
	nodenames = []
	for n in g.nodes:
		if n.func == 1:  # get g0
			totalrate += n.g0
			noderates.append(n.g0)
			nodenames.append(n.name)
		else:
			totalrate += n.g1
			noderates.append(n.g1)
			nodenames.append(n.name)
	cumulativerates = list(np.cumsum(noderates)/sum(noderates))

	return totalrate,noderates,nodenames,cumulativerates

def createGraph(n,sf,d):
	# initialize graph
	graph = Graph(n,[0],sf,d,[],0,[])
	listofnodes = [Node(x,[0],[],[],[],[],0,0,gamma_0,gamma_1,1) for x in xrange(0,n)]
	graph.nodes = listofnodes

	# set zeroth and first nodes to be interdependent
	setDependency(graph.nodes[0], graph.nodes[1])
	setDependency(graph.nodes[1], graph.nodes[0])

	# scale-free
	if graph.sf == 'sf':
		for x in xrange(2,n):  # starts at 2 for base case -- 0 and 1 forced above
			total_deg = float(sum(c.deg for c in graph.nodes))  # cast to float
			for y in xrange(0,x):
				# new node depends on preexisting ones
				if random.random() < graph.nodes[y].deg / total_deg:
					# make x depend on y
					setDependency(graph.nodes[x],graph.nodes[y])
				if random.random() < graph.nodes[x].deg / total_deg:
					# make y depend on x
					setDependency(graph.nodes[y],graph.nodes[x])
			# if no dependencies created either way, randomly create one
			if graph.nodes[x].deg == 0:
				r = random.randint(0,x-1)
				setDependency(graph.nodes[x],graph.nodes[r])
			if graph.nodes[x].ideg == 0:
				r = random.randint(0,x-1)
				setDependency(graph.nodes[r],graph.nodes[x])
	
	# random
	else:
		# MAKE SURE STATISTICALLY DEFENSIBLE; FIGURE THIS OUT / TALK TO NICK!
		cutoff = 0.005  # cutoff for random edge generation -- prob of new edge
		for x in xrange(2,n):  # starts at 2 for base case -- 0 and 1 forced above
			for y in xrange(0,x):
				# new node depends on preexisting ones
				if random.random() < cutoff:
					# make x depend on y
					setDependency(graph.nodes[x],graph.nodes[y])
				if random.random() < cutoff:
					# make y depend on x
					setDependency(graph.nodes[y],graph.nodes[x])
			# if no dependencies created either way, randomly create one
			if graph.nodes[x].deg == 0:
				r = random.randint(0,x-1)
				setDependency(graph.nodes[x],graph.nodes[r])
			if graph.nodes[x].ideg == 0:
				r = random.randint(0,x-1)
				setDependency(graph.nodes[r],graph.nodes[x])

	return graph

def modifyGraph(graph,k):
	node_idx = list(np.random.choice(graph.n,k,replace=False))
	for idx in node_idx:
		graph.nodes[idx].g0 = gamma_0_new
		graph.nodes[idx].g1 = gamma_1_new
	return graph


def ageGraph(graph):
	# set initial fraction d of nodes to nonfunctional
	initialnonfunc = random.sample(range(0,graph.n),int(graph.d*graph.n))
	for idx in initialnonfunc:
		graph.nodes[idx].func = 0

	# initial update of vitality
	graph.vitality.append(float(sum(c.func for c in graph.nodes)) / graph.n)

	# loop
	while graph.vitality[-1] > 0.01:
		# update lifespan
		graph.lifespan += 1

		# Gillespie

		# get total rate and other meta rate data
		totalrate,noderates,nodenames,cumulativerates = getTotalRate(graph)

		# generate two uniformly distributed random numbers
		utime = random.random()
		ureaction = random.random()

		# draw random waiitng time from exponential distribution; use total rate as param
		tdiff = -math.log(utime)/totalrate
		graph.t.append(graph.t[-1]+tdiff)

		# figure out which reaction
		for i,x in enumerate(cumulativerates):
			if x > ureaction:  # ith reaction
				graph.nodes[i].func = 1 - graph.nodes[i].func
				break  # make sure only that one reaction occurs

		# calculate dependencies, break accordingly
		num_broken = 1
		num_broken_prev = 0
		while num_broken > num_broken_prev:
			num_broken_prev = num_broken
			num_broken = 0
			for g in graph.nodes:
				depfunc = getFunc(graph,g)
				if g.func == 1:
					if depfunc < 0.5:
						g.func = 0
						num_broken += 1

		# update vitality
		graph.vitality.append(float(sum(c.func for c in graph.nodes)) / graph.n)

		# update time
		for g in graph.nodes:
			if g.func == 0:
				g.t.append(0)
			else:
				g.t.append(g.t[-1]+tdiff)

	return graph

def graphResults(graphs,plt_filename):
	plt.clf()
	plt_filename = plt_filename + '.pdf'
	for graph in graphs:
		plt.plot(graph.t,graph.vitality)
	plt.title('Vitality vs. Time')
	plt.ylabel('Vitality (%)')
	plt.xlabel('Time (s)')
	plt.savefig(plt_filename)
	# plt.show()

def constructName(graph):  # get filename for graph
	name = './data/' +str(graph.n) + '_' + str(graph.sf)
	return name

def plotMortalityCurve(graphs,plt_filename):
	plt.clf()
	# process filename
	plt_filename = plt_filename + '_MortalityCurve.pdf'
	# get first passage times
	fpt = []
	for graph in graphs:
		fpt.append(graph.lifespan)
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	sns.kdeplot(np.array(fpt),cumulative=True)
	plt.savefig(plt_filename)

def plotMortalityCurves(graphs_list,plt_filename,ks):
	plt.clf()
	plt_filename = plt_filename + '.pdf'
	fpt = []
	for graphs in graphs_list:
		fpt.append([])
		for graph in graphs:
			fpt[-1].append(graph.lifespan)
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	for i,x in enumerate(fpt):
		sns.kdeplot(np.array(x),cumulative=True,label=str(ks[i]))
	plt.savefig(plt_filename)

def runGillespie(num_trials,n,sf,k):
	graphs = []

	# run with same graph!
	graph = createGraph(n,sf,0.00)

	# check that modifications work (part 1)
	# for x in graph.nodes[0:10]:
	# 	print x.g0

	graph_mod = modifyGraph(graph,k)

	# check that modifications work! (works)
	# for y in  graph_mod.nodes[0:10]:
	# 	print y.g0

	# sys.exit()

	for i in xrange(0,num_trials):
		# time_a = time.time()
		# graph1 = copy.deepcopy(graph)
		# graph1 = createGraph(n,sf,0.00)
		# graph2 = modifyGraph(graph1,k)
		graph2 = copy.deepcopy(graph_mod)
		# time_b = time.time()
		# print time_b - time_a
		graph3 = ageGraph(graph2)
		# time_c = time.time()
		# print time_c - time_b
		# print graph2.vitality
		# print graph2.t
		# print graph2.lifespan
		# print len(graph2.vitality)
		graphs.append(graph3)
		if i % 5 == 0:
			print i
			print time.ctime()

	name = constructName(graph3)
	name = name + '_' + str(num_trials)
	plt_filename = './' + name #+ '.png'

	# graphResults(graphs,plt_filename)
	# plotMortalityCurve(graphs,plt_filename)

	return graphs

def writeCSV(graphslist,csv_filename,ks):
	csv_filename = csv_filename + '.csv'

	with open(csv_filename, 'a') as f:
		writer = csv.writer(f)
		if os.stat(csv_filename).st_size == 0:  # empty file
			writer.writerow(('name','sf','N','num_trials','gamma_0','gamma_0_new','gamma_1','d','fpt','k','alive'))  # write header row
		for i,graphs in enumerate(graphslist):
			num_trials = len(graphs)
			# k = ks[i]
			k = i  # label by index, not by k-value...need to keep track of k-values better
			for graph in graphs:
				name = graph.sf + '_' + str(graph.n) + '_' + str(num_trials) + '_' + str(k)
				writer.writerow((name,graph.sf,graph.n,num_trials,gamma_0,gamma_0_new,gamma_1,graph.d,graph.lifespan,k,0))
		f.close()


## PSEUDOMAIN -- clean up later!!
rgraphs = []
sfgraphs = []
nt = 1500
N = 500
# ks = [0,0,0,int(N/2),int(N/2),int(N/2),N,N,N]
# ks = [0,0,0,int(N/2),int(N/2),int(N/2),N,N,N]
ks = [0,0,0,0,0,0]
for k in ks:
	time_a = time.time()
	gr = runGillespie(nt,N,'r',k)
	rgraphs.append(gr)
	print 'r done', k
	time_b = time.time()
	print time_b - time_a
	gsf = runGillespie(nt,N,'sf',k)
	sfgraphs.append(gsf)
	time_c = time.time()
	print 'sf done', k
	print time_c - time_b

r_filename = './data/v4_' + str(N) + '_' + str(nt) + '_' + str(int(1000*gamma_0)) + '_r'
sf_filename = './data/v4_' + str(N) + '_' + str(nt) + '_' + str(int(1000*gamma_0)) + '_sf'

plotMortalityCurves(rgraphs,r_filename,ks)
plotMortalityCurves(sfgraphs,sf_filename,ks)

writeCSV(rgraphs,r_filename,ks)
writeCSV(sfgraphs,sf_filename,ks)


# time_a = time.time()
# runGillespie(5,250,'r',1)
# time_b = time.time()
# print time_b - time_a
# print 'r done'
# runGillespie(5,250,'sf',1)
# time_c = time.time()
# print time_c - time_b
# print 'sf done'