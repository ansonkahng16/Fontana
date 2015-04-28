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
import networkx as nx

# CONSTANTS
# gamma_0 = float(sys.argv[1])
gamma_0 = 0.05
gamma_1 = 0.0
gamma_0_new = 0.01
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

	# print depfuncs

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
	graph_adjdict_list = []
	graph_nodedeps = copy.deepcopy(getadjdict(graph))  # update this to break nodes to graph
	graph_adjdict_list.append(graph_nodedeps)

	initialnonfunc = random.sample(range(0,graph.n),int(graph.d*graph.n))
	for idx in initialnonfunc:
		graph.nodes[idx].func = 0

	functionalnodeslist = []
	functionalnodes = []
	for x in graph.nodes:
		functionalnodes.append(x.func)
	functionalnodeslist.append(functionalnodes)

	# print graph_nodedeps
	# print functionalnodes
	# print graph_adjdict_list

	# initial update of vitality
	graph.vitality.append(float(sum(c.func for c in graph.nodes)) / graph.n)

	# loop
	while graph.vitality[-1] > 0.01:

		graph_nodedeps = copy.deepcopy(graph_nodedeps)
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
				# print 'i reaction', i
				graph.nodes[i].func = 1 - graph.nodes[i].func
				for k,v in graph_nodedeps.items():
					if graph.nodes[i].name in v:
						v.remove(graph.nodes[i].name)
				graph_nodedeps[i] = []
				break  # make sure only that one reaction occurs

		# calculate dependencies, break accordingly
		num_broken = 1
		# num_broken_prev = 0
		while num_broken > 0:
			# num_broken_prev = num_broken
			num_broken = 0
			for g in graph.nodes:
				depfunc = getFunc(graph,g)
				if g.func == 1:
					if depfunc < 0.5:
						g.func = 0
						# print g.name
						for k,v in graph_nodedeps.items():
							if g.name in v:
								v.remove(g.name)
						graph_nodedeps[g.name] = []
						num_broken += 1

		# update vitality
		graph.vitality.append(float(sum(c.func for c in graph.nodes)) / graph.n)

		# update time
		for g in graph.nodes:
			if g.func == 0:
				g.t.append(0)
			else:
				g.t.append(g.t[-1]+tdiff)

		# update adjacency dictionary based on broken nodes
		graph_adjdict_list.append(graph_nodedeps)

		# get functionality of all nodes
		functionalnodes = []
		for x in graph.nodes:
			functionalnodes.append(x.func)
		functionalnodeslist.append(functionalnodes)

		# print 'nodedeps:', graph_nodedeps
		# print 'functional nodes:', functionalnodes
		# print 'adjdict list:', graph_adjdict_list[0]

	return graph, graph_adjdict_list,functionalnodeslist

def getadjdict(graph):
	adjdict = {}
	for i,g in enumerate(graph.nodes):
		adjdict[i] = g.dep
	return adjdict


def getadjdictplus(graph):
	adjdict = {}
	adjdictcount = []
	for i,g in enumerate(graph.nodes):
		adjdict[i] = g.dep
		adjdictcount.append(len(g.dep))
	return adjdict, adjdictcount

def plotadjdict(adjdict,livenodes,figname,ctd):
	figname = './graphs/' + figname + '.pdf'
	nodecolors = []
	# print 'livenodes', livenodes
	# print 'ctd', ctd
	for i,x in enumerate(livenodes):
		if x == 0:
			nodecolors.append('r')
		else:
			nodecolors.append('b')

	# edit nodecolors to find nodes close to death
	for x in ctd:
		if x[1]:
			nodecolors[x[0]] = 'g'

	plt.figure(figsize=(12,12))
	G=nx.DiGraph(adjdict)
	for i,x in enumerate(livenodes):
		if x == 0:
			if len(G.edges(i)) > 0:
				for e in G.edges(i):
					G.remove_edge(*e)

	nx.draw_circular(G,node_size=50,with_labels=True,font_size=8,node_color=nodecolors)

	# plt.show()

	plt.savefig(figname)

def visualizedict(graph):
	adjdict = getadjdict(graph)
	plotadjdict(adjdict)

def processGraphTimeData(graph2_adjdict_list, graph2_functionalnodeslist, adjdictcount):
	pctalivelist = []
	closetodeathll = []
	for j,al in enumerate(graph2_adjdict_list):
		pctalivelist.append({})
		closetodeathlist = []
		for i,k in enumerate(al):
			# print al[k]
			pctalive = len(al[k])/float(adjdictcount[i])
			tmp = len(al[k]) - float(adjdictcount[i])/2
			closetodeath = (tmp < 1 and tmp >= 0)
			pctalivelist[-1][k] = pctalive

			if graph2_functionalnodeslist[j][i] == 1: # node alive:
				closetodeathlist.append((i,closetodeath))

		closetodeathll.append(closetodeathlist)

	# get number of alive vertices at each step close to death
	numclosetodeath = []
	fracclosetodeath = []
	for l in closetodeathll:
		# get true vs false count
		x = [int(a[1]) for a in l]
		num_close_to_death = sum(x)
		num_alive_at_this_point = len(l)
		numclosetodeath.append((num_close_to_death,num_alive_at_this_point))
		if num_alive_at_this_point != 0:
			fracclosetodeath.append(float(num_close_to_death)/num_alive_at_this_point)
		else:
			fracclosetodeath.append('div by 0')

	return pctalivelist, closetodeathll, numclosetodeath, fracclosetodeath

def visualize(n,sf):
	# graph visualization

	graph = createGraph(n,sf,0.0)
	graph2, graph2_adjdict_list, graph2_functionalnodeslist = ageGraph(graph)

	len_adjdict_list = len(graph2_adjdict_list)

	adjdict, adjdictcount = getadjdictplus(graph)

	pctalivelist, closetodeathll, numclosetodeath, fracclosetodeath = processGraphTimeData(graph2_adjdict_list, graph2_functionalnodeslist, adjdictcount)


	# write all data to file
	with open('./graphs/datalog.txt','ab') as f:
		print>>f, time.ctime()		
		print>>f, n
		print>>f,sf
		print>>f, len_adjdict_list
		print>>f, zip(numclosetodeath,fracclosetodeath)
		print>>f, '======================================'
	f.close()


	for y in xrange(1,5):
		idx = len_adjdict_list - y

		ctd = closetodeathll[idx]

		# plot graph with only valid edges
		figname = str(n) + '_' + sf + '_' + str(idx) + '_' + str(len_adjdict_list) + '_valid'
		plotadjdict(graph2_adjdict_list[idx],graph2_functionalnodeslist[idx],figname,ctd)

		# plot graph with all edges from nodes that are still alive
		figname = str(n) + '_' + sf + '_' + str(idx) + '_' + str(len_adjdict_list) + '_alive'
		plotadjdict(adjdict,graph2_functionalnodeslist[idx],figname,ctd)

def main():
	n = 200
	sf = 'sf'

	visualize(n,sf)

if __name__ == '__main__':
	main()

