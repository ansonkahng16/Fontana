import numpy as np
import random
import math
from matplotlib import pyplot as plt
import seaborn
import csv
import bisect
import collections
import os
import mortalityCurve


def plot_data(N,num_trials,sf,gamma_0,gamma_1,d,vitality_cutoff,col,mkr):

	vitality_data = mortalityCurve.loadData(N,num_trials,sf,gamma_0,gamma_1)

	# get first passage times for data under vitality_cutoff
	fpt = []
	for v in vitality_data:
		i = bisect.bisect_left(v,vitality_cutoff,lo=len(v),hi=0)
		fpt.append(i-1)  # so hacky...please fix later

	s = len(fpt)  # total number of individuals

	c = collections.Counter(fpt)

	t_vals = []  # time values
	m_vals = []  # mortality values

	for k in c:
		t_vals.append(k)
		m_vals.append(c[k]/float(s))
		s -= c[k]

	t_vals = sorted(t_vals)

	gamma0 = str.replace(str(gamma_0),'.','d')
	gamma1 = str.replace(str(gamma_1),'.','d')
	dstr = str.replace(str(d),'.','d')

	plt.scatter(t_vals, m_vals, color=col, marker=mkr)
	plt.title('Mortality Rate vs. Time')
	plt.ylabel('Mortality Rate')
	plt.xlabel('Time')
	ax.set_yscale('log')



# main function
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

# # gamma_0
# plot_data(2500,100,'sf',0.0075,0.0,0.0,0.05,'b','d')
# plot_data(2500,100,'r',0.0075,0.0,0.0,0.05,'b','o')
# plot_data(2500,100,'sf',0.00375,0.0,0.0,0.05,'k','d')
# plot_data(2500,100,'r',0.00375,0.0,0.0,0.05,'k','o')
# plot_data(2500,100,'sf',0.0025,0.0,0.0,0.05,'r','d')
# plot_data(2500,100,'r',0.0025,0.0,0.0,0.05,'r','o')

# # gamma_1
# plot_data(2500,100,'sf',0.00625,0.003,0.0,0.05,'b','d')
# plot_data(2500,100,'r',0.00625,0.003,0.0,0.05,'b','o')
# plot_data(2500,100,'sf',0.00625,0.006,0.0,0.05,'k','d')
# plot_data(2500,100,'r',0.00625,0.006,0.0,0.05,'k','o')
# plot_data(2500,100,'sf',0.00625,0.009,0.0,0.05,'r','d')
# plot_data(2500,100,'r',0.00625,0.009,0.0,0.05,'r','o')

# # N
# plot_data(2500,100,'sf',0.00625,0.0,0.0,0.05,'b','d')
# plot_data(2500,100,'r',0.00625,0.0,0.0,0.05,'b','o')
# plot_data(250,100,'sf',0.00625,0.0,0.0,0.05,'k','d')
# plot_data(250,100,'r',0.00625,0.0,0.0,0.05,'k','o')
# plot_data(25,100,'sf',0.00625,0.0,0.0,0.05,'r','d')
# plot_data(25,100,'r',0.00625,0.0,0.0,0.05,'r','o')


plt_filename = '/Users/ansonkahng/Fontana/data/wk5/combined.png'
plt.savefig(plt_filename)