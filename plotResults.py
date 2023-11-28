import numpy as np

import matplotlib.pyplot as plt

import matplotlib.colors as clrs


def import_data(benchmarkname):
	N_rnd_opt = 3  # number of random optimizers per SAT
	
	#=============
	# IMPORT DATA
	#=============
	
	filename = "final_results/"+benchmarkname+"_results"
	f = open(filename, "r")
	data = f.read()
	f.close()
	
	inf = 123456

	data = data.replace('(',"")
	data = data.replace(')',"")
	data = data.replace('\n',",")
	data = data.replace("SAT ","SAT,")
	data = data.replace("OPT1 ","OPT1,")
	data = data.replace("OPT2 ","OPT2,")
	data = data.replace("OPT_RND ","OPT_RND,")
	data = data.replace("OPTIMIZER_1_RUNTIME ","OPTIMIZER_1_RUNTIME,")
	data = data.replace("OPTIMIZER_2_RUNTIME ","OPTIMIZER_2_RUNTIME,")
	data = data.replace("OPTIMIZER_RND_RUNTIME ","OPTIMIZER_RND_RUNTIME,")
	data = data.replace('inf',str(inf))
	data = data.split(',')
	
	# remove empty elements
	data = np.array(data)
	index = np.argwhere(data=="")
	data = np.delete(data, index)
	
	# TODO: replace inf by number of vertices
	
	
	
	#============
	# PARSE DATA
	#============
	
	seqTime, parTime, pebbles, spooks, runtimes, pebble_constr, spook_constr = [],[],[],[],[],[],[]
	OPT1, OPT2, OPT_RND = [],[],[]
	OPT1_runtimes, OPT2_runtimes, OPT_RND_runtimes = [],[],[]
	
	i=0
	while(i<len(data)):
		if (data[i] == "SAT"):
			i+=1
			pebbles.append(int(data[i]))
			i+=1
			spooks.append(int(data[i]))
			i+=1
			parTime.append(int(data[i]))
			i+=1
			pebble_constr.append(int(data[i]))
			i+=1
			spook_constr.append(int(data[i]))
			i+=1
			runtimes.append(float(data[i]))
			seqTime.append(int(data[i+2]))
			i+=1
			tmp = []
			while(data[i]=="OPT1"):
				i+=1
				tmp.append([int(data[i]),int(data[i+1]),int(data[i+2])])
				i+=3
			OPT1.append(tmp)
			if(data[i]=="OPTIMIZER_1_RUNTIME"):
				i+=1
				OPT1_runtimes.append(float(data[i]))
				i+=1
			else:
				print("[pareto plot] could not find optimizer runtime")
			
			tmp = []
			while(data[i]=="OPT2"):
				i+=1
				tmp.append([int(data[i]),int(data[i+1]),int(data[i+2])])
				i+=3
			OPT2.append(tmp)
			if(data[i]=="OPTIMIZER_2_RUNTIME"):
				i+=1
				OPT2_runtimes.append(float(data[i]))
				i+=1
			else:
				print("[pareto plot] could not find optimizer runtime")
			
			for rnd_opt in range(N_rnd_opt):
				tmp = []
				while(data[i]=="OPT_RND"):
					i+=1
					tmp.append([int(data[i]),int(data[i+1]),int(data[i+2])])
					i+=3
				OPT_RND.append(tmp)
				if(data[i]=="OPTIMIZER_RND_RUNTIME"):
					i+=1
					OPT_RND_runtimes.append(float(data[i]))
					i+=1
				else:
					print("[pareto plot] could not find optimizer runtime")
		else:
			print("[pareto plot] could not parse data")	
			i+=1
	return seqTime, parTime, pebbles, spooks, runtimes, pebble_constr, spook_constr, OPT1, OPT2, OPT_RND, OPT1_runtimes, OPT2_runtimes, OPT_RND_runtimes




def plotParetoFront(benchmarkname,ax=None):
	seqTime, parTime, pebbles, spooks, runtimes, pebble_constr, spook_constr, OPT1, OPT2, OPT_RND, OPT1_runtimes, OPT2_runtimes, OPT_RND_runtimes = import_data(benchmarkname)
	
	if ax==None:
		fig = plt.figure()
		ax = fig.add_subplot(1,1,1)
		
	ax.set_ylabel('sequential time')
	ax.set_xlabel('pebbles')


	
	
	min_spooks = min(spooks)
	max_spooks = max(spooks)

	
	
	for path in OPT1+OPT2+OPT_RND:
		xdata, ydata, cdata = [],[],[]
		for [a,b,c] in path:
			xdata.append(b)
			ydata.append(a)
			cdata.append(c)
		#ax.plot(xdata,ydata,color="grey",linewidth=0.5,markersize=1,marker=None,alpha=0.1)
		ax.scatter(xdata, ydata, c = cdata, cmap='viridis',s=1,alpha=0.15,vmin=min_spooks,vmax=max_spooks)
	print(benchmarkname)
	print("Minimal sequential time",min(xdata))
	print("Minimal number of pebbles",min(ydata))
	print("Maximal runtime solver",max(runtimes))
	print("Maximal runtime optimizer",max(OPT1_runtimes+OPT2_runtimes+OPT_RND_runtimes))
	
	xdata = pebbles
	ydata = seqTime
	
	scatterplot = ax.scatter(xdata, ydata, c = spooks, cmap='viridis',s=10,vmin=min_spooks,vmax=max_spooks)
	
	ax.set_title(benchmarkname)

	plt.colorbar(scatterplot, label='spooks')
	
	#plt.show()
	return


def plotParetoFronts(benchmarknames):
	fig = plt.figure(figsize=(8,12))
	nrows=5
	ncols=2
	#fig2 = plt.figure(figsize=(10,15))


	for i, benchmarkname in enumerate(benchmarknames):
		#print(i)
		ax = fig.add_subplot(nrows,ncols, i+1)
		plotParetoFront(benchmarkname,ax)
		
	fig.tight_layout()
	#plt.savefig("final_results/images/ParetoFrontsBenchmarksOptimizers_without_paths.pdf")
	#plt.show()
	plt.close()
	return

#plotParetoFront("c432")


# plot benchmarks results
benchmarknames = ["c432","c499","c880","c1355","c1908","c2670","c3540","c5315","c6288","c7552"]
plotParetoFronts(benchmarknames)
#plotConstraintRuntimes(benchmarknames)


# plot large benchmarks results
#benchmarknames = ["c3540","c5315","c6288","c7552"]
#plotParetoFrontsLargeBM(benchmarknames)
#plotConstraintRuntimesLargeBM(benchmarknames)


