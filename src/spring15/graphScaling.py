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
import operator

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
	graph_nodedeps = copy.deepcopy(getAdjdict(graph))  # update this to break nodes to graph
	graph_adjdict_list.append(graph_nodedeps)

	initialnonfunc = random.sample(range(0,graph.n),int(graph.d*graph.n))
	for idx in initialnonfunc:
		graph.nodes[idx].func = 0

	functionalnodeslist = []
	functionalnodes = []
	for x in graph.nodes:
		functionalnodes.append(x.func)
	functionalnodeslist.append(functionalnodes)

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

	return graph, graph_adjdict_list,functionalnodeslist

def getAdjdict(graph):
	adjdict = {}
	for i,g in enumerate(graph.nodes):
		adjdict[i] = g.dep
	return adjdict


def getAdjdictPlusCount(graph):
	adjdict = {}
	adjdict_count = []
	for i,g in enumerate(graph.nodes):
		adjdict[i] = g.dep
		adjdict_count.append(len(g.dep))
	return adjdict, adjdict_count

def plotAdjdict(adjdict,livenodes,figname,ctd):
	figname = './graphs/' + figname + '.pdf'
	nodecolors = []

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

	plt.savefig(figname)


def plotCTD(adjdict,livenodes,figname,ctd):
	figname = './graphs/' + figname + '.pdf'
	nodecolors = []

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

	# only plot close to death?
	for i,x in enumerate(nodecolors):
		if x != 'g':
			for e in G.edges(i):
				G.remove_edge(*e)

	nx.draw(G,node_size=50,with_labels=True,font_size=8,node_color=nodecolors)

	# plt.show()

	plt.savefig(figname)

def getFuncCTD(adjdict,adjdict_count):
	ctr = 0
	for k,v in adjdict.items():
		if len(v) / float(adjdict_count[k]) >= 0.5:
			ctr += 1
	return ctr

def analyzeLiveNodes(currentadjdict,adjdict_count,livenodes,idx):
	currentadjdict = currentadjdict[idx]
	livenodes = livenodes[idx]

	ln_dict = {}

	for i,x in enumerate(livenodes):  # for each ctd node
		if x == 1:  # if ctd
			# make copy of adjdict
			tmp = copy.deepcopy(currentadjdict)
			orig_dict_count = getFuncCTD(tmp,adjdict_count)
			broken_node = i # node name
			for k,v in tmp.items():
				if broken_node in v:
					v.remove(broken_node)

			ctr = 1
			# repeatedly break dependencies
			while ctr > 0:
				ctr = 0
				# check if nodes are broken
				for k,v in tmp.items():
					pctalive = len(tmp[k])/float(adjdict_count[k])
					if pctalive < 0.5:
						for k1,v1 in tmp.items():
							if k in v1:
								ctr += 1
								v1.remove(k)

			# ctd node broken: number of nodes still alive
			numfunc = getFuncCTD(tmp,adjdict_count)

			ln_dict[i] = (orig_dict_count,numfunc)


	return ln_dict


def processGraphTimeData(adjdict_list, functional_nodes_list, adjdict_count):
	pct_alive_list = []
	ctd_lists = []
	for j,al in enumerate(adjdict_list):
		pct_alive_list.append({})
		closetodeathlist = []
		for i,k in enumerate(al):
			# print al[k]
			pctalive = len(al[k])/float(adjdict_count[i])
			tmp = len(al[k]) - float(adjdict_count[i])/2
			closetodeath = (tmp < 1 and tmp >= 0)
			pct_alive_list[-1][k] = pctalive

			if functional_nodes_list[j][i] == 1: # node alive:
				closetodeathlist.append((i,closetodeath))

		ctd_lists.append(closetodeathlist)

	# get number of alive vertices at each step close to death
	num_CTD = []
	frac_CTD = []
	for l in ctd_lists:
		# get true vs false count
		x = [int(a[1]) for a in l]
		num_close_to_death = sum(x)
		num_alive_at_this_point = len(l)
		num_CTD.append((num_close_to_death,num_alive_at_this_point))
		if num_alive_at_this_point != 0:
			frac_CTD.append(float(num_close_to_death)/num_alive_at_this_point)
		else:
			frac_CTD.append('div by 0')

	return pct_alive_list, ctd_lists, num_CTD, frac_CTD

def visualizeGraph(n,sf):
	# create and age graph
	graph = createGraph(n,sf,0.0)
	aged_graph, adjdict_list, functional_nodes_list = ageGraph(graph)

	# number of iterations
	len_adjdict_list = len(adjdict_list)

	# get adjacency dictionary and counts for each timestep
	adjdict, adjdict_count = getAdjdictPlusCount(graph)

	# get all other summary statistics 
	pct_alive_list, ctd_lists, num_CTD, frac_CTD = processGraphTimeData(adjdict_list, functional_nodes_list, adjdict_count)

	num_to_zero_list = []
	num_to_zero_prob = 1
	for time_idx in xrange(0,len_adjdict_list):
		possible_death_stats = analyzeLiveNodes(adjdict_list,adjdict_count,functional_nodes_list,time_idx)
		a = [a for (a,_) in possible_death_stats.values()]
		b = [b for (_,b) in possible_death_stats.values()]
		num_to_zero_list.append(str(b.count(0)) + '/' + str(len(b)))
		try: 
			x = float(b.count(0))
			y = float(len(b))
			num_to_zero_prob *= ((y-x)/y)
		except:
			num_to_zero_prob *= 1

	# # ctd statistics
	# possible_death_stats = analyzeCTD(adjdict_list,adjdict_count,functional_nodes_list,ctd_lists,len_adjdict_list-3)
	# a = [a for (a,_) in possible_death_stats.values()]
	# b = [b for (_,b) in possible_death_stats.values()]
	# avg = sum(b)/float(len(b))
	# print a[0], sorted(b)
	# print 'avg', avg, a[0]
	# print 'num to 0', b.count(0), len(b)
	# print 'num to death'  # get number that drops everything below threshold

	# # IMPLEMENT OTHER METRIC OF VITALITY
	# # ALSO REWRITE CODE. THIS IS NASTY AF
	# # print possible_death_stats
	# sorted_x = sorted(possible_death_stats.items(), key=operator.itemgetter(1))
	# print sorted_x
	# sys.exit()

	# write all data to file
	with open('./graphs/datalog.txt','ab') as f:
		print>>f, time.ctime()		
		print>>f, n
		print>>f,sf
		print>>f, len_adjdict_list
		print>>f, zip(num_CTD,frac_CTD)
		print>>f, num_to_zero_list
		print>>f, num_to_zero_prob
		print>>f, '======================================'
	f.close()


	for y in xrange(1,5):
		idx = len_adjdict_list - y

		ctd = ctd_lists[idx]

		# possible_death_stats = analyzeLiveNodes(adjdict_list,adjdict_count,functional_nodes_list,idx)
		# a = [a for (a,_) in possible_death_stats.values()]
		# b = [b for (_,b) in possible_death_stats.values()]
		# try:
		# 	avg = sum(b)/float(len(b))
		# except:
		# 	avg = 'divide by 0'
		# try:
		# 	print a[0], sorted(b)
		# 	print 'avg', avg, a[0]
		# except:
		# 	print 'no a'
		# print 'num to 0', b.count(0), '/', len(b)
		# print '=============================='

		# plot graph with only valid edges
		figname = str(n) + '_' + sf + '_' + str(idx) + '_' + str(len_adjdict_list) + '_valid'
		plotAdjdict(adjdict_list[idx],functional_nodes_list[idx],figname,ctd)

		# plot graph with all edges from nodes that are still alive
		figname = str(n) + '_' + sf + '_' + str(idx) + '_' + str(len_adjdict_list) + '_alive'
		plotAdjdict(adjdict,functional_nodes_list[idx],figname,ctd)

		# plot only close to death nodes
		figname = str(n) + '_' + sf + '_' + str(idx) + '_' + str(len_adjdict_list) + '_ctd'
		plotCTD(adjdict_list[idx],functional_nodes_list[idx],figname,ctd)

def main():
	n = 200
	sf = 'r'

	visualizeGraph(n,sf)

if __name__ == '__main__':
	main()

