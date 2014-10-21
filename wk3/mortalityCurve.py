import numpy as np
import random
import math
from matplotlib import pyplot as plt
import seaborn
import csv
import bisect

'''Construct mortality curves based on vitality_data CSV file.'''

def loadData(N,num_trials,sf,sf_str):
	vitality_data = []
	csv_filename = './data/'+sf_str[sf]+'_'+str(N)+'_'+str(num_trials)+'.csv'
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
	ax.set_yscale('log')
	# plt.show()
	plt.xlabel('Time')
	plt.ylabel('Percent Mortality')
	plt.title('Mortality vs. Time')

	plt_filename = './data/'+sf_str[sf]+'_'+str(N)+'_'+str(num_trials)+'_mortality.png'
	plt.savefig(plt_filename)


# fpt = mortalityCurve(5000,1000,False,{True: 'sf', False: 'r'},0.05)

plotMortalityCurve(5000,1000,True,{True: 'sf', False: 'r'},0.05)