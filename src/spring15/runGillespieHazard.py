import numpy as np
import random
import math
from matplotlib import pyplot as plt
import seaborn as sns
import time
from math import exp
from math import log
import scipy.integrate
from scipy.integrate import quad
import sys
from scipy.stats import rv_continuous
import scipy.optimize
from scipy.optimize import newton_krylov
import copy
import dill as cPickle

# GOMPERTZ CONSTANTS -- change to change timescale
a = 0.01
b = 0.5

# WEIBULL CONSTANTS
alpha = 3
beta = 2.5

## Node structure
class Node:
	def __init__(self,name,t,dep,idep,depnodes,idepnodes,deg,ideg,g0,g1,func):
		self.name = name  # name: int
		self.t = t  # war clock time - list of times
		self.dep = dep  # dependencies -- names of nodes
		self.idep = idep  # inverse dependencies -- names of nodes
		self.deg = deg  # degree
		self.ideg = ideg  # inverse degree
		self.g0 = g0  # gamma_0
		self.g1 = g1  # gamma_1
		self.func = func  # functional or nonfunctional

## Dist = continuous rv class
class Dist(rv_continuous):
	def __init__(self,CDF):
		super(Dist,self).__init__()
		self.cdf = CDF
	def _cdf(self,x):
		return self.cdf(x)

## Graph = list of nodes
class Graph:
	def __init__(self,n,t,sf,d,vitality,lifespan,nodes,frail):
		self.n = n  # num odes
		self.t = t  # time list
		self.sf = sf  # sf or r
		self.d = d  # initial pct of nonfunctional nodes
		self.vitality = vitality  # list of vitality (pct)
		self.lifespan = lifespan  # total lifespan
		self.nodes = nodes  # list of nodes
		self.frail = frail  # frailty
		self.dist = Dist(self.CDF)  # CDF
		self.utime = 0  # for Gillespie
		self.hazardname = 'Weibull'

	def Hazard(self,t):
		return (a/b)*exp(t/b)  # Gompertz hazard
		# return (alpha/beta)*(t/beta)**(alpha-1)  # Weibull hazard


	def Activity(self,t):  # over all graph
		# return self.Hazard(t)  # testing
		print t
		return self.Hazard(t)*self.n*self.vitality[-1]

	def CDF(self,t):
		return 1 - exp(-quad(self.Activity,0,t)[0])

	def CDF_utime(self,t):
		return 1 - exp(-quad(self.Activity,0,t)[0]) - self.utime

	def CDF_hetero(self,t):
		return 2  # not implemented!


# Gompertz functions
def GompertzHazard(t):  # Gompertz Hazard -- based on time
	return (a/b)*exp(t/b)

def GompertzPDF(t):
	return GompertzHazard(t)*exp(-a*(exp(t/b)-1))

def inverseGompertz(u,g):  # inverse Gompertz CDF; u is uniformly distributed
	return b*(log(1-log(u)/(g.n*g.vitality[-1]*a*exp(g.t[-1]/b))))

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

def createGraph(n,sf,d,f):
	# initialize graph
	graph = Graph(n,[0],sf,d,[1],0,[],f)
	listofnodes = [Node(x,[0],[],[],[],[],0,0,0,0,1) for x in xrange(0,n)]
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

	# initial update of rates
	# update hazard rates based on time
	for n in graph.nodes:
		n.g0 = graph.Hazard(graph.t[-1])  # (a/b)*exp(n.t[-1]/b)  # math overflow error???
		# not using this ^
		n.g1 = 0

	# loop
	while graph.vitality[-1] > 0.01:
		# Gillespie

		# generate two uniformly distributed random numbers
		utime = random.random()
		# print 'utime', utime
		ureaction = random.random()
		graph.utime = utime

		# draw random waiting time from inverse CDF
		# tdiff = graph.dist.ppf(utime)  # most general
		tdiff = graph.CDF_utime(utime)
		print tdiff
		graph.t.append(graph.t[-1]+tdiff)

		# update lifespan
		graph.lifespan += tdiff

		# update time
		for g in graph.nodes:
			if g.func == 0:
				g.t.append(0)
			else:
				g.t.append(g.t[-1]+tdiff)

		# update hazard rates based on time
		for n in graph.nodes:
			n.g0 = graph.Hazard(graph.t[-1]) # (a/b)*exp(n.t[-1]/b) # as above, not used
			n.g1 = 0

		# get total rate and other meta rate data
		totalrate,noderates,nodenames,cumulativerates = getTotalRate(graph)

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

		# print alive nodes
		# print sum(c.func for c in graph.nodes)

		# update vitality
		graph.vitality.append(float(sum(c.func for c in graph.nodes)) / graph.n)
		# print graph.vitality[-1]

	return graph

def graphResults(graphs,plt_filename):
	plt.clf()
	plt_filename = plt_filename + '_Hazard2.pdf'
	for graph in graphs:
		plt.plot(graph.t,graph.vitality)
	plt.title('Vitality vs. Time')
	plt.ylabel('Vitality (%)')
	plt.xlabel('Time (s)')
	plt.savefig(plt_filename)
	# plt.show()

def plotMortalityCurve(graphs,plt_filename):
	plt.clf()
	# process filename
	plt_filename = plt_filename + '_Hazard_MortalityCurve2.pdf'
	# get first passage times
	fpt = []
	for graph in graphs:
		fpt.append(graph.lifespan)
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	sns.kdeplot(np.array(fpt),cumulative=True)
	plt.savefig(plt_filename)

def constructName(graph):  # get filename for graph
	name = './data/' + str(graph.n) + '_' + str(graph.sf) + '_' + str(graph.hazardname)
	if graph.frail == False:
		name = name + '_nofrail'
	elif graph.frail == True:
		name = name + '_frail'
	return name

def runGillespie(num_trials,n,sf,d,f):
	graphs = []

	if f == True:  # frail -- heterogeneous (different networks)
		for i in xrange(0,num_trials):
			graph1 = createGraph(n,sf,d,f)
			graph2 = ageGraph(graph1)
			graphs.append(graph2)
			if i % 5 == 0:
				print i
				print time.ctime()

	elif f == False:  # not frail -- homogeneous (same network)
		print 'starting to create'
		aa = time.time()
		graph = createGraph(n*2,sf,d,f)  # bigger size for this
		bb = time.time()
		print bb - aa, 'created'
		for i in xrange(0,num_trials):
			ab = time.time()
			graph1 = copy.deepcopy(graph)  # make copy to pass to ageGraph
			print time.time() - ab, 'copied'
			bc = time.time()
			graph2 = ageGraph(graph1)
			print time.time() - bc, 'time to age'
			graphs.append(graph2)
			if i % 5 == 0:
				print i
				print time.ctime()

	name = constructName(graph2)
	name = name + '_' + str(num_trials)
	plt_filename = './' + name #+ 'Hazard.pdf'

	graphResults(graphs,plt_filename)
	plotMortalityCurve(graphs,plt_filename)

def main():
	time_a = time.time()
	runGillespie(100,250,'r',0,False)
	time_b = time.time()
	print time_b - time_a
	print 'r done'
	runGillespie(100,250,'sf',0,False)
	time_c = time.time()
	print time_c - time_b
	print 'sf done'

if __name__ == '__main__':
	main()