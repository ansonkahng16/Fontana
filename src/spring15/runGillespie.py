import numpy as np
import random
import math
from matplotlib import pyplot as plt
import seaborn as sns
import time

# CONSTANTS
gamma_0 = 0.003
gamma_1 = 0.000

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
	# t = war clock time -- list of times
	# dep = dependencies -- names
	# idep = inverse dependencies -- nodes that depend on it -- names
	# depnodes = dependencies -- nodes
	# idepnodes = inverse dependencies -- nodes
	# g0 = gamma_0
	# g1 = gamma_1
	# deg = degree
	# ideg = inverse degree
	# func = functional or not

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
	# n = size
	# t = time list
	# sf = sf or r
	# d = initial percent of nonfunctional nodes
	# vitality = vitality of graph (list)
	# lifespan = total lifespan of graph
	# nodes = list of nodes

# helper function to set dependencies
def setDependency(a,b):  # node a depends on node b
	a.dep.append(b.name)
	b.idep.append(a.name)
	a.depnodes.append(b)
	b.idepnodes.append(a)
	a.deg += 1
	b.ideg += 1

# helper function to get pct functionality of all nodes a depends on
def getFunc(a):  # a = node
	depfuncs = []
	for depnode in a.depnodes:
		depfuncs.append(depnode.func)

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
				depfunc = getFunc(g)
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
	plt_filename = plt_filename + '.png'
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
	# process filename
	plt_filename = plt_filename + '_MortalityCurve.png'
	# get first passage times
	fpt = []
	for graph in graphs:
		fpt.append(graph.lifespan)
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	sns.kdeplot(np.array(fpt),cumulative=True)
	plt.savefig(plt_filename)

def runGillespie(num_trials,n,sf):
	graphs = []

	for i in xrange(0,num_trials):
		# time_a = time.time()
		graph1 = createGraph(n,sf,0.00)
		# time_b = time.time()
		# print time_b - time_a
		graph2 = ageGraph(graph1)
		# time_c = time.time()
		# print time_c - time_b
		# print graph2.vitality
		# print graph2.t
		# print graph2.lifespan
		# print len(graph2.vitality)
		graphs.append(graph2)
		if i % 5 == 0:
			print i
			print time.ctime()

	name = constructName(graph2)
	name = name + '_' + str(num_trials)
	plt_filename = './' + name #+ '.png'

	graphResults(graphs,plt_filename)
	plotMortalityCurve(graphs,plt_filename)


time_a = time.time()
# runGillespie(500,2500,'r')
time_b = time.time()
print time_b - time_a
print 'r done'
runGillespie(500,2500,'sf')
time_c = time.time()
print time_c - time_b
print 'sf done'