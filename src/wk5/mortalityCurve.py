import numpy as np
import random
import math
from matplotlib import pyplot as plt
import seaborn
import csv
import bisect
import collections
import os

'''Construct mortality curves based on vitality_data CSV file.'''

def loadData(N,num_trials,sf,gamma_0,gamma_1):
	vitality_data = []
	gamma0 = str.replace(str(gamma_0),'.','d')
	gamma1 = str.replace(str(gamma_1),'.','d')

	csv_filename = '/Users/ansonkahng/Fontana/data/wk5/'+sf+'_'+str(N)+'_'+str(num_trials)+'_'+gamma0+'_'+gamma1+'.csv'
	with open(csv_filename, 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			vitality_data.append(row)
	return vitality_data

def mortalityCurve(N,num_trials,sf,vitality_cutoff,gamma_0,gamma_1,d):
	vitality_data = loadData(N,num_trials,sf,gamma_0,gamma_1)

	# get first passage times for data under vitality_cutoff
	first_passage_times = []
	for v in vitality_data:
		i = bisect.bisect_left(v,vitality_cutoff,lo=len(v),hi=0)
		first_passage_times.append(i-1)  # so hacky...please fix later

	# write data to CSV file
	# columns: sf/r, N, num_trials, gamma_0, gmama_1, d, fpt
	# csv_filename = '/Users/ansonkahng/Fontana/data/wk5/'+sf+'_'+str(N)+'_'+str(num_trials)+'_data.csv'
	# csv_filename = '/Users/ansonkahng/Fontana/data/wk5/'+str(N)+'_'+str(num_trials)+'_data.csv'
	csv_filename = '/Users/ansonkahng/Fontana/data/wk5/gamma0.csv'
	with open(csv_filename, 'a') as f:
		writer = csv.writer(f)
		if os.stat(csv_filename).st_size == 0:  # empty file
			writer.writerow(('name','sf','N','num_trials','gamma_0','gamma_1','d','fpt','alive'))  # write header row
		for i in first_passage_times:
			name = sf + '_' + str(N) + '_' + str(num_trials) + '_' + str(gamma_0) + '_' + str(gamma_1) + '_' + str(d)
			writer.writerow((name, sf,N,num_trials,gamma_0,gamma_1,d,i,0))
		f.close()

	return first_passage_times

def plotMortalityCurve(N,num_trials,sf,vitality_cutoff,gamma_0,gamma_1,d):
	fpt = mortalityCurve(N,num_trials,sf,vitality_cutoff,gamma_0,gamma_1,d)

	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	seaborn.kdeplot(np.array(fpt),cumulative=True)
	# ax.set_yscale('log')
	# plt.show()
	plt.xlabel('Time')
	plt.ylabel('Percent Mortality')
	plt.title('Mortality vs. Time')

	plt_filename = '/Users/ansonkahng/Fontana/data/wk5/'+sf+'_'+str(N)+'_'+str(num_trials)+'_mortality.png'
	plt.savefig(plt_filename)

	return fpt

def plotMortalityRate(fpt, N,num_trials,sf,vitality_cutoff,gamma_0,gamma_1,d):

	s = len(fpt)  # total number of states

	c = collections.Counter(fpt)

	t_vals = []  # time values
	m_vals = []  # mortality values

	for k in c:
		t_vals.append(k)
		m_vals.append(c[k]/float(s))
		s -= c[k]
	
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	plt.scatter(t_vals, m_vals)
	plt.title('Mortality Rate vs. Time')
	plt.ylabel('Mortality Rate')
	plt.xlabel('Time')
	ax.set_yscale('log')
	ax.set_xscale('log')

	plt_filename = '/Users/ansonkahng/Fontana/data/wk5/'+sf+'_'+str(N)+'_'+str(num_trials)+'_mortalityrate.png'
	plt.savefig(plt_filename)
	# plt.show()

