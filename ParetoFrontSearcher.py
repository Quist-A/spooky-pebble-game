import gameSolver
import numpy as np
import signal

from bmcFormula import *



# setup timeout behaviour
class TimeoutException2(Exception):
	pass

def timeout_handler(signum, frame):
	raise TimeoutException2

signal.signal(signal.SIGALRM, timeout_handler)



Nseeds = 5  # number of seeds to run


#============================================
#
#	SHORTRUN BENCHMARKS
#
#============================================

shortrun_benchmarknames = ["c17","c432","c499","c880","c1355","c1908","c2670"]

nodes = [7,172,177,276,177,193,401]

Twait = 15  # maximal runtime per bmc iteration
Tmax = 60*2 # maximal runtime of SAT solver


for i,benchmarkname in enumerate(shortrun_benchmarknames):
	print(benchmarkname)
	
	# open file to write solution
	f = open("final_results/"+benchmarkname+"_results_new_Tmax=2m_Twait=15s", "a")
	
	# import DAG
	DAG = dag("benchmarks/ISCAS85XMG/"+benchmarkname+".bench")
	
	# start run with spook constraint
	for max_spooks in [np.inf,int(np.ceil(nodes[i]/5)),int(np.ceil(nodes[i]/10)),int(np.ceil(nodes[i]/20)),0]:
		max_pebbles = nodes[i]

		# search for first solution
		optimal_pebbles = np.inf
		for seed in np.arange(Nseeds):
			(pebbles_used,spooks_used,count,seqT),(opt_pebbles_used,opt_spooks_used,opt_count,opt_seqT),runtime = gameSolver.spooky_solver(DAG,benchmarkname,max_pebbles,max_spooks,Twait,9**seed)

			print((max_pebbles,max_spooks),(pebbles_used,spooks_used,count,seqT),(opt_pebbles_used,opt_spooks_used,opt_count,opt_seqT),runtime)

			f.write("(("+str(max_pebbles)+","+str(max_spooks)+"),("+str(pebbles_used)+","+str(spooks_used)+","+str(count)+","+str(seqT)+"),("+str(opt_pebbles_used)+","+str(opt_spooks_used)+","+str(opt_count)+","+str(opt_seqT)+"),"+str(runtime)+"),\n")

			if opt_pebbles_used < optimal_pebbles:
				optimal_pebbles = opt_pebbles_used
		
		# search for solutions with decreasing amount of pebbles
		for max_pebbles in np.arange(optimal_pebbles,0,-5):
			solution_found = False  # solution found with this max pebble constraint
			for seed in range(Nseeds):
				# set alarm for Tmax sec
				signal.alarm(Tmax)
				try:
					# try to find solution for given parameters
					(pebbles_used,spooks_used,count,seqT),(opt_pebbles_used,opt_spooks_used,opt_count,opt_seqT),runtime = gameSolver.spooky_solver(DAG,benchmarkname,max_pebbles,max_spooks,Twait,9**seed)
				except:
					continue
				else:
					# reset alarm
					signal.alarm(0)
					solution_found = True
					print((max_pebbles,max_spooks),(pebbles_used,spooks_used,count,seqT),	(opt_pebbles_used,opt_spooks_used,opt_count,opt_seqT),runtime)

					f.write("(("+str(max_pebbles)+","+str(max_spooks)+"),("+str(pebbles_used)+","+str(spooks_used)+","+str(count)+","+str(seqT)+"),("+str(opt_pebbles_used)+","+str(opt_spooks_used)+","+str(opt_count)+","+str(opt_seqT)+"),"+str(runtime)+"),\n")
	
			if not(solution_found):  # no solution found with this number of pebbles
				break  # go to next spook constraint
	
	f.close()  # close file with solutions






#============================================
#
#	LONGRUN BENCHMARKS
#
#============================================

longrun_benchmarknames = ["c3540","5315","c6288","c7552"]

nodes = [830,1089,979,988]

Twait = 60  # maximal runtime per bmc iteration
Tmax = 60*8 # maximal runtime of SAT solver


for i,benchmarkname in enumerate(longrun_benchmarknames):
	print(benchmarkname)

	# open file to write solution
	f = open("final_results/"+benchmarkname+"_results_new_Tmax=8m_Twait=60s", "a")
	
	# import DAG
	DAG = dag("benchmarks/ISCAS85XMG/"+benchmarkname+".bench")
	
	# start run with spook constraint
	for max_spooks in [np.inf,int(np.ceil(nodes[i]/5)),int(np.ceil(nodes[i]/10)),int(np.ceil(nodes[i]/20)),0]:
		max_pebbles = nodes[i]

		# search for first solution
		optimal_pebbles = np.inf
		for seed in np.arange(Nseeds):
			(pebbles_used,spooks_used,count,seqT),(opt_pebbles_used,opt_spooks_used,opt_count,opt_seqT),runtime = gameSolver.spooky_solver(DAG,benchmarkname,max_pebbles,max_spooks,Twait,9**seed)

			print((max_pebbles,max_spooks),(pebbles_used,spooks_used,count,seqT),(opt_pebbles_used,opt_spooks_used,opt_count,opt_seqT),runtime)

			f.write("(("+str(max_pebbles)+","+str(max_spooks)+"),("+str(pebbles_used)+","+str(spooks_used)+","+str(count)+","+str(seqT)+"),("+str(opt_pebbles_used)+","+str(opt_spooks_used)+","+str(opt_count)+","+str(opt_seqT)+"),"+str(runtime)+"),\n")

			if opt_pebbles_used < optimal_pebbles:
				optimal_pebbles = opt_pebbles_used
		
		# search for solutions with decreasing amount of pebbles
		for max_pebbles in np.arange(optimal_pebbles,0,-5):
			solution_found = False  # solution found with this max pebble constraint
			for seed in range(Nseeds):
				# set alarm for Tmax sec
				signal.alarm(Tmax)
				try:
					# try to find solution for given parameters
					(pebbles_used,spooks_used,count,seqT),(opt_pebbles_used,opt_spooks_used,opt_count,opt_seqT),runtime = gameSolver.spooky_solver(DAG,benchmarkname,max_pebbles,max_spooks,Twait,9**seed)
				except:
					continue
				else:
					# reset alarm
					signal.alarm(0)
					solution_found = True
					print((max_pebbles,max_spooks),(pebbles_used,spooks_used,count,seqT),	(opt_pebbles_used,opt_spooks_used,opt_count,opt_seqT),runtime)

					f.write("(("+str(max_pebbles)+","+str(max_spooks)+"),("+str(pebbles_used)+","+str(spooks_used)+","+str(count)+","+str(seqT)+"),("+str(opt_pebbles_used)+","+str(opt_spooks_used)+","+str(opt_count)+","+str(opt_seqT)+"),"+str(runtime)+"),\n")
	
			if not(solution_found):  # no solution found with this number of pebbles
				break  # go to next spook constraint
	
	f.close()  # close file with solutions
