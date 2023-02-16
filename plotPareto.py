import numpy as np

import matplotlib.pyplot as plt

import matplotlib.colors as clrs


def import_data(filename):

	#f = open("final_results/"+benchmarkname+"_results_new_Tmax=8m_Twait=60s", "r")
	#f = open("final_results/"+benchmarkname+"_results_new_Tmax=2m_Twait=15s", "r")
	f = open(filename, "r")

	data = f.read()

	f.close()

	inf = 123456

	data = data.replace('(',"")
	data = data.replace(')',"")
	data = data.replace('\n',"")
	data = data.replace('inf',str(inf))
	data = data.split(',')

	solutionsstr = np.array(data[:-1]).reshape(int(len(data)/11),11)
	solutions = np.zeros((int(len(data)/11),11))
	solutions[:,:-1] = solutionsstr[:,:-1].astype(int)
	solutions[:,-1] = solutionsstr[:,-1].astype(float)


	solutions[solutions == inf] = solutions[0][0]  # replace inf by number of vertices


	return solutions


def convertSolutions(solutions):
	seqTime = []
	pebbles = []
	spooks = []


	runtimes = []
	pebble_constr = []
	spook_constr = []


	for max_pebbles,max_spooks,pebbles_used,spooks_used,count,seqT,opt_pebbles_used,opt_spooks_used,opt_count,opt_seqT,runtime in solutions:
		seqTime.append(opt_seqT)
		pebbles.append(opt_pebbles_used)
		spooks.append(opt_spooks_used)
		
		runtimes.append(runtime)
		pebble_constr.append(max_pebbles)
		spook_constr.append(max_spooks)
	return seqTime, pebbles, spooks, runtimes, pebble_constr, spook_constr
	

def plotParetoFronts(benchmarknames):
	fig = plt.figure(figsize=(8,12))
	nrows=5
	ncols=2
	#fig2 = plt.figure(figsize=(10,15))


	for i, benchmarkname in enumerate(benchmarknames):
		try:
			solutions = import_data("final_results/"+benchmarkname+"_results_new_Tmax=2m_Twait=15s")
		except:
			solutions = import_data("final_results/"+benchmarkname+"_results_new_Tmax=8m_Twait=60s")
		seqTime, pebbles, spooks, runtimes, pebble_constr, spook_constr = convertSolutions(solutions)
		
		ax = fig.add_subplot(nrows,ncols, i+1)
		ax.set_ylabel('sequential time')
		ax.set_xlabel('pebbles')


		xdata = pebbles
		ydata = seqTime

		scatterplot = ax.scatter(xdata, ydata, c = spooks, cmap='viridis',s=10)

		ax.set_title(benchmarkname)

		plt.colorbar(scatterplot, label='spooks')
		
		
	fig.tight_layout()
	plt.savefig("final_results/images/ParetoFrontsBenchmarks.pdf")
	#plt.show()
	plt.close()
	return

def plotConstraintRuntimes(benchmarknames):
	fig = plt.figure(figsize=(8,12))
	nrows=5
	ncols=2

	for i, benchmarkname in enumerate(benchmarknames):
		try:
			solutions = import_data("final_results/"+benchmarkname+"_results_new_Tmax=2m_Twait=15s")
		except:
			solutions = import_data("final_results/"+benchmarkname+"_results_new_Tmax=8m_Twait=60s")
		seqTime, pebbles, spooks, runtimes, pebble_constr, spook_constr = convertSolutions(solutions)
		
		ax = fig.add_subplot(nrows,ncols, i+1)
		ax.set_ylabel('runtime (seconds)')
		ax.set_xlabel('pebbles constraint')


		xdata = pebble_constr
		ydata = runtimes
		zdata = spook_constr

		xdata = np.array(xdata)

		scatterplot = ax.scatter(xdata, ydata, c = zdata, cmap='viridis', s = 10, norm=clrs.PowerNorm(gamma=1./3.5))
		#label = z)#,label="x")
		#norm=clrs.BoundaryNorm([0,1,int(max(spook_constr)/20),int(max(spook_constr)/10),int(max(spook_constr)/5), max(spook_constr)],256),#norm=clrs.LogNorm())# norm=clrs.PowerNorm(gamma=1./3.5))
		if benchmarkname == "c7552": xdata[xdata == 944] = 988  # fix due to small data error
		ax.set_xlim([min(xdata)-1,max(xdata[xdata<max(xdata)])+1])

		ax.set_title(benchmarkname)

		plt.colorbar(scatterplot, label='spooks constraint')
		#ax.legend()
		
		

	fig.tight_layout()
	plt.savefig("final_results/images/ConstraintRuntimesBenchmarks.pdf")
	#plt.show()
	plt.close()
	return


benchmarknames = ["c432","c499","c880","c1355","c1908","c2670","c3540","c5315","c6288","c7552"]
plotParetoFronts(benchmarknames)
plotConstraintRuntimes(benchmarknames)


