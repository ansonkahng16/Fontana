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
	def __init__(self,name,t,dep,idep,depnodes,idepnodes,deg,ideg,g0,g1,func,loc):
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
		self.loc = loc
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
	# loc = # steps away from root node (weight = discount factor raised to this power)

## Graph = list of nodes
class Graph:
	def __init__(self,n,t,d,vitality,lifespan,nodes):
		self.n = n
		self.t = t
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

def createGraph(n,d):
	graph = Graph(n,[0],d,[],0,[])
	initialnode = Node(0,[0],[],[],[],[],0,0,gamma_0,gamma_1,1,0)
	graph.nodes.append(initialnode)

	# for each additional node, choose a previous node to make them dependent on
	# weight this somehow? or does that come for free via this construction?
	for x in xrange(1,n):
		childnode = Node(x,[0],[],[],[],[],0,0,gamma_0,gamma_1,1,0)
		currentlen = len(graph.nodes)
		parentnodeidx = random.randint(0,currentlen-1)
		parentnode = graph.nodes[parentnodeidx]
		setDependency(childnode,parentnode)
		# should this be undirected?
		#setDependency(parentnode,childnode)
		childnode.loc = parentnode.loc + 1
		graph.nodes.append(childnode)
	
	for i,t in enumerate(graph.nodes):
		print i, t.dep, t.idep, t.loc

def main():
	g = createGraph(10,0)

if __name__ == '__main__':
	main()

