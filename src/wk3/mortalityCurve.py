import numpy as np
import random
import math
from matplotlib import pyplot as plt
import seaborn
import csv
import bisect
import collections

'''Construct mortality curves based on vitality_data CSV file.'''

def loadData(N,num_trials,sf,sf_str):
	vitality_data = []
	csv_filename = './data_old/'+sf_str[sf]+'_'+str(N)+'_'+str(num_trials)+'.csv'
	with open(csv_filename, 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			vitality_data.append(row)
	return vitality_data

def mortalityCurve(N,num_trials,sf,sf_str,vitality_cutoff):
	vitality_data = loadData(N,num_trials,sf,sf_str)

	# get first passage times for data under vitality_cutoff
	first_passage_times = []
	for v in vitality_data:
		i = bisect.bisect_left(v,vitality_cutoff,lo=len(v),hi=0)
		first_passage_times.append(i-1)  # so hacky pls fix later

	return first_passage_times

def plotMortalityCurve(N,num_trials,sf,sf_str,vitality_cutoff):
	fpt = mortalityCurve(N,num_trials,sf,sf_str,vitality_cutoff)

	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	seaborn.kdeplot(np.array(fpt),cumulative=True)
	# ax.set_yscale('log')
	# plt.show()
	plt.xlabel('Time')
	plt.ylabel('Percent Mortality')
	plt.title('Mortality vs. Time')

	plt_filename = './data_old/'+sf_str[sf]+'_'+str(N)+'_'+str(num_trials)+'_mortality.png'
	plt.savefig(plt_filename)

def mortalityRate(N,num_trials,sf,sf_str,vitality_cutoff):
	fpt = mortalityCurve(N,num_trials,sf,sf_str,vitality_cutoff)

	# get rate per unit time...
	s = len(fpt)  # total number of states

	c = collections.Counter(fpt)

	
	t_vals = []  # time values
	m_vals = []  # mortality values
	# tot = 0

	for k in c:
		t_vals.append(k)
		# tot += c[k]
		m_vals.append(c[k]/float(s))
		# m_vals.append(tot/float(s))
		s -= c[k]
	
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	plt.scatter(t_vals, m_vals)
	plt.title('Mortality Rate vs. Time')
	plt.ylabel('Mortality Rate')
	plt.xlabel('Time')
	ax.set_yscale('log')
	ax.set_xscale('log')

	plt_filename = './data_old/'+sf_str[sf]+'_'+str(N)+'_'+str(num_trials)+'_mortalityrate.png'
	plt.savefig(plt_filename)
	# plt.show()



# fpt = mortalityCurve(5000,1000,False,{True: 'sf', False: 'r'},0.05)

# plotMortalityCurve(50000,100,True,{True: 'sf', False: 'r'},0.05)

# mortalityRate(50000,100,True,{True: 'sf', False: 'r'},0.05)
