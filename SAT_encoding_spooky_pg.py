from z3 import *


# ===================
#
# parameters
#
# ===================

T = 15  # maximal time
n = 10 # number of vertices in DAG

max_pebbles = 6 # maximal number of pebbles allowed
max_spooks  = 10 # maximal number of spooks allowed

""" Example DAG 1
n = 10
output_vertices = [1,5,6] # list of output vertices of DAG
edges = [(0,1),(2,1),(2,3),(3,4),(4,5),(4,6),(7,6),(8,5),(9,3)] # list of edges of DAG
# (i,j) means: i is a predecessor of j, i.o.w. i is a child of j
"""

""" Example DAG 2"""
n = 9
output_vertices = [7]
edges = [(0,8),(1,8),(8,3),(2,3),(3,7),(6,7),(4,6),(5,6)]


# ===================
#
# initialisation
#
# ===================

# matrix of pebbles
P = [ [ Bool("p_%s_%s" % (i, j)) for j in range(T) ] 
      for i in range(n) ]

# matrix of spooks
S = [ [ Bool("s_%s_%s" % (i, j)) for j in range(T) ] 
      for i in range(n) ]

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
for i in range(n):
	s.add(Not(P[i][0]),Not(S[i][0]))

# final clauses
for i in range(n):
	s.add(Not(S[i][T-1]))
	if (i in output_vertices):
		s.add(P[i][T-1])
	else:
		s.add(Not(P[i][T-1]))






for t in range(T-1):

	# move clauses

	for child, father in edges:
		# remove pebble condition
		s.add(Implies(And(P[father][t], Not(P[father][t+1])), 
			Or(S[father][t+1], And(P[child][t], P[child][t+1]) )))
		
		# remove spook condition
		s.add(Implies(And(S[father][t], Not(S[father][t+1])), 
			And(P[father][t+1], And(P[child][t], P[child][t+1]) )))

		# add pebble condition
		s.add(Implies(And(Not(P[father][t]),P[father][t+1]), 
			And(P[child][t], P[child][t+1])  ))



# regularity clauses
# not necessarily needed


for t in range(T):

	# cardinality clauses

	#s.set("sat.cardinality.solver", True)
	# Some things might be updated to improve speed of PbLe function,
	# see the stanford documentation of Z3.
	s.add(PbLe([(P[i][t], 1) for i in range(n)], max_pebbles))
	s.add(PbLe([(S[i][t], 1) for i in range(n)], max_spooks))



# ===================
#
# solve the formula
#
# ===================

#print(s)
print(s.check())
print(s.model())

