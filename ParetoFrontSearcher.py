import gameSolver
from solutionOptimizer import *
import numpy as np
import signal
import time


import Convert_bench_file_to_DAG as bench2DAG

#from bmcFormula import *



def optimizeSolution(states,n,count,edges,(max_pebbles,max_spooks),f):
	edgelist,inv_edgelist = gameSolver.edges2edgelist(n,edges)
	
	starttime = time.time()
	standardOptimizer1(states,n,(edgelist,inv_edgelist),(max_pebbles,max_spooks),count,f)
	endtime = time.time()
	runtime = endtime-starttime
	f.write("(OPTIMIZER_1_RUNTIME "+str(runtime)+")\n")
	
	starttime = time.time()
	standardOptimizer2(states,n,(edgelist,inv_edgelist),(max_pebbles,max_spooks),count,f)
	endtime = time.time()
	runtime = endtime-starttime
	f.write("(OPTIMIZER_2_RUNTIME "+str(runtime)+")\n")
	
	for i in range(3):
		starttime = time.time()
		randomOptimizer(states,n,(edgelist,inv_edgelist),(max_pebbles,max_spooks),count,f,i)
		endtime = time.time()
		runtime = endtime-starttime
		f.write("(OPTIMIZER_RND_RUNTIME "+str(runtime)+")\n")
		
	return

def standardOptimizer1(states,n,(edgelist,inv_edgelist),(max_pebbles,max_spooks),count,f):
	
	old_seqT, old_pebbles_used, old_spooks_used = gameSolver.calc_solution_info(states,n)
	seqT = 0
	pebbles_used = 0
	spooks_used = 0
	
	while(old_seqT != seqT or old_pebbles_used != pebbles_used or old_spooks_used != spooks_used):
		old_seqT = seqT
		old_pebbles_used = pebbles_used
		old_spooks_used = spooks_used
		
		(states,count) = par2seq(states,n,count,(max_pebbles,max_spooks))
		
		states = remove_useless_spookings(states,n,inv_edgelist,count)
		seqT, pebbles_used, spooks_used = gameSolver.calc_solution_info(states,n)
		f.write("(OPT1 "+str(seqT)+","+str(pebbles_used)+","+str(spooks_used)+")\n")
		
		states = remove_useless_pebbling(states,n,edgelist,count)
		seqT, pebbles_used, spooks_used = gameSolver.calc_solution_info(states,n)
		f.write("(OPT1 "+str(seqT)+","+str(pebbles_used)+","+str(spooks_used)+")\n")
		
		states = delay_pebble_placement(states,n,(edgelist,inv_edgelist),count)  
		seqT, pebbles_used, spooks_used = gameSolver.calc_solution_info(states,n)
		f.write("(OPT1 "+str(seqT)+","+str(pebbles_used)+","+str(spooks_used)+")\n")
		
		states = expedite_unpebbling(states,n,(edgelist,inv_edgelist),count)
		seqT, pebbles_used, spooks_used = gameSolver.calc_solution_info(states,n)
		f.write("(OPT1 "+str(seqT)+","+str(pebbles_used)+","+str(spooks_used)+")\n")

		states = delay_spook_placement(states,n,max_pebbles,count)
		seqT, pebbles_used, spooks_used = gameSolver.calc_solution_info(states,n)
		f.write("(OPT1 "+str(seqT)+","+str(pebbles_used)+","+str(spooks_used)+")\n")
		
		states = replace_spook_by_pebble_asap(states,n,inv_edgelist,max_pebbles,count)
		seqT, pebbles_used, spooks_used = gameSolver.calc_solution_info(states,n)
		f.write("(OPT1 "+str(seqT)+","+str(pebbles_used)+","+str(spooks_used)+")\n")
		
	return
	
def standardOptimizer2(states,n,(edgelist,inv_edgelist),(max_pebbles,max_spooks),count,f):
	
	old_seqT, old_pebbles_used, old_spooks_used = gameSolver.calc_solution_info(states,n)
	seqT = 0
	pebbles_used = 0
	spooks_used = 0
	
	while(old_seqT != seqT or old_pebbles_used != pebbles_used or old_spooks_used != spooks_used):
		old_seqT = seqT
		old_pebbles_used = pebbles_used
		old_spooks_used = spooks_used
		
		(states,count) = par2seq(states,n,count,(max_pebbles,max_spooks))
		
		states = remove_useless_spookings(states,n,inv_edgelist,count)
		seqT, pebbles_used, spooks_used = gameSolver.calc_solution_info(states,n)
		f.write("(OPT2 "+str(seqT)+","+str(pebbles_used)+","+str(spooks_used)+")\n")
		
		states = delay_spook_placement(states,n,max_pebbles,count)
		seqT, pebbles_used, spooks_used = gameSolver.calc_solution_info(states,n)
		f.write("(OPT2 "+str(seqT)+","+str(pebbles_used)+","+str(spooks_used)+")\n")
		
		states = replace_spook_by_pebble_asap(states,n,inv_edgelist,max_pebbles,count)
		seqT, pebbles_used, spooks_used = gameSolver.calc_solution_info(states,n)
		f.write("(OPT2 "+str(seqT)+","+str(pebbles_used)+","+str(spooks_used)+")\n")
			
		states = remove_useless_pebbling(states,n,edgelist,count)
		seqT, pebbles_used, spooks_used = gameSolver.calc_solution_info(states,n)
		f.write("(OPT2 "+str(seqT)+","+str(pebbles_used)+","+str(spooks_used)+")\n")
		
		states = delay_pebble_placement(states,n,(edgelist,inv_edgelist),count)  
		seqT, pebbles_used, spooks_used = gameSolver.calc_solution_info(states,n)
		f.write("(OPT2 "+str(seqT)+","+str(pebbles_used)+","+str(spooks_used)+")\n")
		
		states = expedite_unpebbling(states,n,(edgelist,inv_edgelist),count)
		seqT, pebbles_used, spooks_used = gameSolver.calc_solution_info(states,n)
		f.write("(OPT2 "+str(seqT)+","+str(pebbles_used)+","+str(spooks_used)+")\n")
		
	return
	
def randomOptimizer(states,n,(edgelist,inv_edgelist),(max_pebbles,max_spooks),count,f,i):
	
	old_seqT, old_pebbles_used, old_spooks_used = gameSolver.calc_solution_info(states,n)
	seqT = 0
	pebbles_used = 0
	spooks_used = 0
	
	np.random.seed(i)
	
	while(old_seqT != seqT or old_pebbles_used != pebbles_used or old_spooks_used != spooks_used):
		old_seqT = seqT
		old_pebbles_used = pebbles_used
		old_spooks_used = spooks_used
		
		(states,count) = par2seq(states,n,count,(max_pebbles,max_spooks))
		for j in range(6):
			random = np.random.randint(6)
			if random == 0:
				states = remove_useless_spookings(states,n,inv_edgelist,count)
			elif random == 1:
				states = remove_useless_pebbling(states,n,edgelist,count)
			elif random == 2:		
				states = delay_pebble_placement(states,n,(edgelist,inv_edgelist),count)  
			elif random == 3:			 
				states = expedite_unpebbling(states,n,(edgelist,inv_edgelist),count)
			elif random == 4:
				states = delay_spook_placement(states,n,max_pebbles,count)
			elif random == 5:				
				states = replace_spook_by_pebble_asap(states,n,inv_edgelist,max_pebbles,count)
			seqT, pebbles_used, spooks_used = gameSolver.calc_solution_info(states,n)
			f.write("(OPT_RND "+str(seqT)+","+str(pebbles_used)+","+str(spooks_used)+")\n")
			
	return



# setup timeout behaviour
class TimeoutException2(Exception):
	pass

def timeout_handler(signum, frame):
	raise TimeoutException2

signal.signal(signal.SIGALRM, timeout_handler)



Nseeds = 3  # number of seeds to run


#============================================
#
#	SHORTRUN BENCHMARKS
#
#============================================

#shortrun_benchmarknames = ["c17","c432","c499","c880","c1355","c1908","c2670"]
shortrun_benchmarknames = ["c499","c880","c1355","c1908","c2670"]

#nodes = [7,172,177,276,177,193,401]
nodes = [177,276,177,193,401]

Twait = 15  # maximal runtime per bmc iteration
Tmax = 60*2 # maximal runtime of SAT solver

for i,benchmarkname in enumerate(shortrun_benchmarknames):
	print(benchmarkname)
	
	# open file to write solution
	f = open("final_results/"+benchmarkname+"_results", "a")
	
	# import DAG
	DAG = bench2DAG.dag("benchmarks/ISCAS85XMG/"+benchmarkname+".bench")
	
	# start run with spook constraint
	for max_spooks in [np.inf,int(np.ceil(nodes[i]/5)),int(np.ceil(nodes[i]/10)),int(np.ceil(nodes[i]/20)),0]:
		max_pebbles = np.inf #nodes[i]
		SAT_solution_found = True
		while(SAT_solution_found and max_pebbles > 0):
			new_max_pebbles = max_pebbles
			SAT_solution_found = False  # solution found with this max pebble constraint
			for seed in range(Nseeds):
				# set alarm for Tmax sec
				signal.alarm(Tmax)
				try:
					# try to find solution for given parameters
					print("[Pareto Front Search] Running SAT solver", max_pebbles, max_spooks)
					(states, n, count, edges),SATruntime = gameSolver.spooky_solver(DAG,benchmarkname,max_pebbles,max_spooks,Twait,9**seed,return_states = True)
					if (n==0):
						continue
				except:
					continue
				else:
					# reset alarm
					signal.alarm(0)
					SAT_solution_found = True
					
					seqT, pebbles_used, spooks_used = gameSolver.calc_solution_info(states,n)
					new_max_pebbles = min(new_max_pebbles,pebbles_used)
					
					print("[Pareto Front Search] SOLUTION FOUND",seqT, pebbles_used, spooks_used, max_pebbles, max_spooks)
					
					f.write("(SAT "+str(pebbles_used)+","+str(spooks_used)+","+str(count)+",("+str(max_pebbles)+","+str(max_spooks)+"),"+str(SATruntime)+"),\n")

					optimizeSolution(states,n,count,edges,(max_pebbles,max_spooks),f)
			
			
			max_pebbles = new_max_pebbles - 5 # decrease number of pebbles to be used with 5

	
	f.close()  # close file with solutions
	
#============================================
#
#	LONGRUN BENCHMARKS
#
#============================================

longrun_benchmarknames = ["c3540","c5315","c6288","c7552"]

nodes = [830,1089,979,988]

Twait = 60  # maximal runtime per bmc iteration
Tmax = 60*8 # maximal runtime of SAT solver


for i,benchmarkname in enumerate(longrun_benchmarknames):
	print(benchmarkname)
	
	# open file to write solution
	f = open("final_results/"+benchmarkname+"_results", "a")
	
	# import DAG
	DAG = bench2DAG.dag("benchmarks/ISCAS85XMG/"+benchmarkname+".bench")
	
	# start run with spook constraint
	for max_spooks in [np.inf,int(np.ceil(nodes[i]/5)),int(np.ceil(nodes[i]/10)),int(np.ceil(nodes[i]/20)),0]:
		max_pebbles = np.inf #nodes[i]
		SAT_solution_found = True
		while(SAT_solution_found and max_pebbles > 0):
			new_max_pebbles = max_pebbles
			SAT_solution_found = False  # solution found with this max pebble constraint
			for seed in range(Nseeds):
				# set alarm for Tmax sec
				signal.alarm(Tmax)
				try:
					# try to find solution for given parameters
					print("[Pareto Front Search] Running SAT solver", max_pebbles, max_spooks)
					(states, n, count, edges),SATruntime = gameSolver.spooky_solver(DAG,benchmarkname,max_pebbles,max_spooks,Twait,9**seed,return_states = True)
					if (n==0):
						continue
				except:
					continue
				else:
					# reset alarm
					signal.alarm(0)
					SAT_solution_found = True
					
					seqT, pebbles_used, spooks_used = gameSolver.calc_solution_info(states,n)
					new_max_pebbles = min(new_max_pebbles,pebbles_used)
					
					print("[Pareto Front Search] SOLUTION FOUND",seqT, pebbles_used, spooks_used, max_pebbles, max_spooks)
					
					f.write("(SAT "+str(pebbles_used)+","+str(spooks_used)+","+str(count)+",("+str(max_pebbles)+","+str(max_spooks)+"),"+str(SATruntime)+"),\n")

					optimizeSolution(states,n,count,edges,(max_pebbles,max_spooks),f)
			
			
			max_pebbles = new_max_pebbles - 5 # decrease number of pebbles to be used with 5

	
	f.close()  # close file with solutions
