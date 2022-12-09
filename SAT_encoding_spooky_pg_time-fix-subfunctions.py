from z3 import *
from Convert_bench_file_to_DAG import *
import time
#import numpy as np


# ===================
#
# parameters
#
# ===================

T = 5 # maximal time (minus 1)
#n = 4 # number of vertices in DAG

max_pebbles = 500 # maximal number of pebbles allowed
max_spooks  = 100 # maximal number of spooks allowed

""" Example DAG 0
n = 5
output_vertices = [3]
edges = [(0,1),(1,2),(2,3),(4,3)]
"""

""" Example DAG 1
n = 10
output_vertices = [1,5,6] # list of output vertices of DAG
edges = [(0,1),(2,1),(2,3),(3,4),(4,5),(4,6),(7,6),(8,5),(9,3)] # list of edges of DAG
# (i,j) means: i is a predecessor of j, i.o.w. i is a child of j
"""

""" Example DAG 2
n = 9
output_vertices = [7]
edges = [(0,8),(1,8),(8,3),(2,3),(3,7),(6,7),(4,6),(5,6)]
"""







def gameFormula(T, n, output_vertices, edges, max_pebbles, max_spooks, onePebblePerT = True):
	"""
	Create boolean formula to check whether game is solvable under 
	given constraints.
	
	Parameters:
	T: maximal time (minus 1)
	n: number of vertices in DAG
	output_vertices: list of output vertices
	edges: list of input edges
	max_pebbles: maximal number of pebbles allowed
	max_spooks: maximal number of spooks allowed
	"""
	# ===================
	#
	# initialisation
	#
	# ===================
	print(time.time())
	# matrix of pebbles
	P = [ [ Bool("p_%s_%s" % (i, j)) for j in range(T) ] 
	      for i in range(n) ]

	# matrix of spooks
	S = [ [ Bool("s_%s_%s" % (i, j)) for j in range(T) ] 
	      for i in range(n) ]
	print(time.time())
	#print("print matrix:")
	#pp(S)

	#print([P[i][0] for i in range(n)])


	# ===================
	#
	# define formula to be solved
	#
	# ===================

	s = Solver()

	# initial clauses
	#for i in range(n):
	#	s.add(Not(P[i][0]),Not(S[i][0]))
	initial_cl = initial_clauses(P, S, n)
	s.add(initial_cl)

	# final clauses
	#for i in range(n):
	#	s.add(Not(S[i][T-1]))
	#	if (i in output_vertices):
	#		s.add(P[i][T-1])
	#	else:
	#		s.add(Not(P[i][T-1]))
	final_cl = final_clauses(P, S, n, T)
	s.add(final_cl)

	print(time.time())

	# move clauses
	"""
	for t in range(T-1):

		for father, child in edges:
			# remove pebble condition
			s.add(Implies(And(P[father][t], Not(P[father][t+1])), 
				Or(S[father][t+1], And(P[child][t], P[child][t+1]) )))
			
			# remove spook condition
			s.add(Implies(And(S[father][t], Not(S[father][t+1])), 
				And(P[father][t+1], And(P[child][t], P[child][t+1]) )))

			# add pebble condition
			s.add(Implies(And(Not(P[father][t]),P[father][t+1]), 
				And(P[child][t], P[child][t+1])  ))
	"""
	move_cl = move_clauses(P, S, edges, 0, T)
	s.add(move_cl)

	if onePebblePerT:
		# max one pebble or spook changes per timestep
		"""for t in range(T-1):

			lst = []
			for i in range(n):
				lst.append((Xor(P[i][t],P[i][t+1]), 1))
				lst.append((Xor(S[i][t],S[i][t+1]), 1))
			s.add(PbLe(lst,1))
		"""
		onePebbPerT_cl = onePebbPerT_clauses(P, S, 0, T)
		s.add(onePebbPerT_cl)

	print(time.time())


	# regularity clauses
	# not necessarily needed -> omitted

	# cardinality clauses
	for t in range(T):
		
		#s.set("sat.cardinality.solver", True)
		# Some things might be updated to improve speed of PbLe function,
		# see the stanford documentation of Z3.
		s.add(PbLe([(P[i][t], 1) for i in range(n)], max_pebbles))
		s.add(PbLe([(S[i][t], 1) for i in range(n)], max_spooks))

	print(time.time())

	# ===================
	#
	# solve the formula
	#
	# ===================

	#print(s)
	#s.check()
	#s.model()
	
	return s

def initial_clauses(P, S, n):
	clauses = []
	for i in range(n):
		clauses.append(Not(P[i][0]))
		clauses.append(Not(S[i][0]))
	return clauses

def final_clauses(P, S, n, T):
	clauses = []
	for i in range(n):
		clauses.append(Not(S[i][T-1]))
		if (i in output_vertices):
			clauses.append(P[i][T-1])
		else:
			clauses.append(Not(P[i][T-1]))
	return clauses

def move_clauses(P, S, edges, startt, endt = None):
	if (endt == None):
		endt = startt+2

	clauses = []
	for t in np.arange(startt, endt-1):
		for father, child in edges:
			# remove pebble condition
			clauses.append(Implies(And(P[father][t], Not(P[father][t+1])), 
				Or(S[father][t+1], And(P[child][t], P[child][t+1]) )))
				
			# remove spook condition
			clauses.append(Implies(And(S[father][t], Not(S[father][t+1])), 
				And(P[father][t+1], And(P[child][t], P[child][t+1]) )))

			# add pebble condition
			clauses.append(Implies(And(Not(P[father][t]),P[father][t+1]), 
				And(P[child][t], P[child][t+1])  ))
	return clauses
	
def onePebbPerT_clauses(P, S, startt, endt = None):
	if (endt == None):
		endt = startt+2

	clauses = []
	for t in np.arange(startt, endt-1):
		lst = []
		for i in range(n):
			lst.append((Xor(P[i][t],P[i][t+1]), 1))
			lst.append((Xor(S[i][t],S[i][t+1]), 1))
		clauses.append(PbLe(lst,1))
	return clauses

print(time.time())
benchmarkname = "ISCAS85/c17"
n, output_vertices, edges = benchToDAG("benchmarks/"+benchmarkname+".bench")
print(n)
print(time.time())
s = gameFormula(T, n, output_vertices, edges, max_pebbles, max_spooks, True)
print(s)
print(time.time())
res = s.check()
print(time.time())

print(res)


if res == sat:
	go = raw_input("Print and save solution? y/n \n")

	if (go == "y"):
		solution = s.model()
		#print(solution)
		with open('output.txt', 'w+') as f:
			for d in solution.decls():
    				f.write("%s = %s \n" % (d.name(), solution[d]))


