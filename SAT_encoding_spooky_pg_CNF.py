from z3 import *
from Convert_bench_file_to_DAG import *
import time
import numpy as np


# ===================
#
# parameters
#
# ===================

T = 50 # maximal time (minus 1)
#n = 4 # number of vertices in DAG

<<<<<<< HEAD
max_pebbles = 100 # maximal number of pebbles allowed
=======
max_pebbles = 60 # maximal number of pebbles allowed
>>>>>>> 17e99f2ab0da2de72b6947a4bf3d957b66f3f267
max_spooks  = np.inf # maximal number of spooks allowed

""" Example DAG 0
n = 5
output_vertices = [3]
edges = [(0,1),(1,2),(2,3),(4,3)]
"""

""" Example DAG 1
n = 10
output_vertices = [1,5,6] # list of output vertices of DAG
edges = [(0,1),(2,1),(2,3),(3,4),(4,5),(4,6),(7,6),(8,5),(9,3)] # list of edges of DAG
# (i,j) means: i is a predecessor of j, i.o.w. i is a child of j -> 7-12-2022 reversed due to imported DAG format
"""

""" Example DAG 2
n = 9
output_vertices = [7]
edges = [(0,8),(1,8),(8,3),(2,3),(3,7),(6,7),(4,6),(5,6)]
"""

""" Example DAG 3
# create random DAG
n = 150
p = 0.1
output_vertices = [n-1]
np.random.seed(0)
random_matrix = np.random.choice(a=[False, True], size=(n,n), p=[1-p, p])
edges = []
input_vertices = np.arange(n)
output_vertices = np.arange(n)
for i in range(n):
	for j in range(i):
		if random_matrix[i][j] == True:
			edges.append((i,j))
			input_vertices = input_vertices[input_vertices != i]
			output_vertices = output_vertices[output_vertices != j]
output_vertices = output_vertices.tolist()
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
	max_spooks: maximal number of spooks allowed. Infinity is denoted as np.inf
	"""

	if max_spooks == 0:
		print("Better call the NoSpooks version...")

	# ===================
	#
	# initialisation
	#
	# ===================
	print("Program started",time.time()) 

	X,Y = np.meshgrid(np.arange(T), np.arange(n))
	p_s = np.full((n,T), "p")
	s_s = np.full((n,T), "s")
	bar_s = np.full((n,T), "_")

	X = np.char.array(X)
	Y = np.char.array(Y)


	P = np.char.add(bar_s,X)
	P = np.char.add(P,bar_s)
	P = np.char.add(P,Y)

	S = np.char.add(s_s,P)
	P = np.char.add(p_s,P)
	#print(P)
	#print(S)
	#print(S.reshape([n*T]).tolist())

	listP = P.reshape([n*T]).tolist()
	listS = S.reshape([n*T]).tolist()


	listP = Bools(listP)
	listS = Bools(listS)

	S = np.array(listS).reshape(n,T)
	P = np.array(listP).reshape(n,T)


	print("Variables initiated",time.time())

	# ===================
	#
	# define formula to be solved
	#
	# ===================

	#s = SolverFor("HORN")
	s = Solver()


	# initial clauses
	for i in range(n):
		s.add(Not(P[i][0]),Not(S[i][0]))
	

	# final clauses
	for i in range(n):
		s.add(Not(S[i][T-1]))
		if (i in output_vertices):
			s.add(P[i][T-1])
		else:
			s.add(Not(P[i][T-1]))

	"""
	# initial clauses
	s.add(Not(Or(P[:,0].tolist())))
	s.add(Not(Or(S[:,0].tolist())))
	
	# final clauses
	s.add(np.take(P[:,T-1],output_vertices).tolist())
	
	non_output_vertices = np.delete(np.arange(n),output_vertices)
	s.add(Not(Or(np.take(P[:,T-1],non_output_vertices).tolist())))

	s.add(Not(Or(S[:,T-1].tolist())))
	"""

	print("Initial/final clauses defined",time.time())

	# move clauses
	for t in range(T-1):

		for father, child in edges:
			# remove pebble condition
			"""s.add(Implies(And(P[father][t], Not(P[father][t+1])), 
				Or(S[father][t+1], And(P[child][t], P[child][t+1]) )))"""
			s.add(Or(Not(P[father][t]),P[father][t+1],S[father][t+1],P[child][t]))
			s.add(Or(Not(P[father][t]),P[father][t+1],S[father][t+1],P[child][t+1]))
			
			# remove spook condition
			"""s.add(Implies(And(S[father][t], Not(S[father][t+1])), 
				And(P[father][t+1], And(P[child][t], P[child][t+1]) )))"""
			s.add(Or(Not(S[father][t]),S[father][t+1],P[father][t+1]))
			s.add(Or(Not(S[father][t]),S[father][t+1],P[child][t]))
			s.add(Or(Not(S[father][t]),S[father][t+1],P[child][t+1]))

			# add pebble condition
			"""s.add(Implies(And(Not(P[father][t]),P[father][t+1]), 
				And(P[child][t], P[child][t+1])  ))"""
			s.add(Or(P[father][t],Not(P[father][t+1]),P[child][t]))
			s.add(Or(P[father][t],Not(P[father][t+1]),P[child][t+1]))
	
	if onePebblePerT:
		# max one pebble or spook changes per timestep
		for t in range(T-1):

			lst = []
			for i in range(n):
				lst.append((Xor(P[i][t],P[i][t+1]), 1))
				lst.append((Xor(S[i][t],S[i][t+1]), 1))
			s.add(PbLe(lst,1))

	print("Move clauses defined",time.time())

	# regularity clauses (no spook and pebble on any vertex at same time)
	# not necessarily needed -> omitted

	# cardinality clauses  
	# -> klein beetje trager dan for-loop variant, later versnellen met numba
	#s.set('cardinality.encoding','circuit')
	for t in range(T):
		p_t = P[:,t].tolist()
		p_t.append(max_pebbles)
		s.add(AtMost(p_t))
		
		if max_spooks != np.inf:
			s_t = S[:,t].tolist()
			s_t.append(max_spooks)
			s.add(AtMost(s_t))

	print("Cardinality clauses defined",time.time())
	#print(s)

	# ===================
	#
	# solve the formula
	#
	# ===================

	#print(s)
	#s.check()
	#s.model()
	
	return s


print(time.time())
<<<<<<< HEAD
benchmarkname = "ISCAS85/c1908"
=======
benchmarkname = "ISCAS85/c432"
>>>>>>> 17e99f2ab0da2de72b6947a4bf3d957b66f3f267
n, output_vertices, edges = benchToDAG("benchmarks/"+benchmarkname+".bench")
#print("Vertices",n)
#print("Edges",len(edges))
#print("Output vertices", len(output_vertices))
print(time.time())
s = gameFormula(T, n, output_vertices, edges, max_pebbles, max_spooks, False)
print("Solving formula",time.time())
res = s.check()
print("Formula solved",time.time())

"""
for encoding in ['grouped','bimander','ordered','unate','circuit']:
	starttime = time.time()
	s.set('cardinality.encoding',encoding)
	res = s.check()
	endtime = time.time()
	print(endtime-starttime," seconds for ",encoding)
"""

print("Time = ",T)
print("max pebbles = ",max_pebbles)
print("max spooks = ",max_spooks)
print("Benchmark = ",benchmarkname)
print(res)

if res == sat:
	go = raw_input("Print and save solution? y/n \n")

	if (go == "y"):
		solution = s.model()
		#print(solution)
		with open('output.txt', 'w+') as f:
			for d in solution.decls():
    				f.write("%s = %s \n" % (d.name(), solution[d]))

