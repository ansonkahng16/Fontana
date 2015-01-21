import math
l = 1
class Dist(rv_continuous):
	def __init__(self,PDF):
		super(Dist,self).__init__()
		self.pdf = PDF
	def _pdf(self,x):
		return self.pdf(x)
class Graph:
	def __init__(self,t):
		self.t = t
		self.dist = Dist(self.PDF)
	def PDF(self,t):
		return l*math.exp(-l*t) # expo pdf
graph = Graph(1)


# OLD CODE
class Dist(rv_continuous):
	def __init__(self,PDF):
		def _pdf(self,x):
			return PDF(x)

## TESTING BEFORE
# get distribution
# dist = Dist()
xs = range(1,100)
xs = [x/float(100) for x in xs]
y1 = [inverseGompertz(1-x,graph) for x in xs]
y2 = []
for x in xs:
	graph.utime = x
	y2.append(newton_krylov(graph.CDF_utime,0.5))
y3 = [graph.dist.ppf(x) for x in xs]
plt.clf()
plt.plot(xs,y1)
plt.plot(xs,y2)
plt.plot(xs,y3)
plt.show()
# print graph.dist.pdf(0.4)  # make sure that this is right with the nodes* factor
# it's right when using the Hazard function itself -- not the overall nodes* factor one
# print GompertzPDF(0.4)
# print GompertzPDF(1)*2500
# print GompertzHazard(0.4)
# print graph.vitality[-1]*graph.n
# print graph.Hazard(1)
# print inverseGompertz(1,graph)
# sys.exit()