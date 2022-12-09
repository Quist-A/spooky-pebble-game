from z3 import *
import numpy as np  # wsch niet nodig om te importeren...
from Convert_bench_file_to_DAG import *
import time



B = BoolSort()


T = 10 # aantal tijdsstappen werkt nog niet...

max_pebbles = 150
max_spooks = 0



print(time.time(),"Program started")
benchmarkname = "ISCAS85/c432"
n, output_vertices, edges = benchToDAG("benchmarks/"+benchmarkname+".bench")

print(time.time(),"Data imported")

# function speed can be improved by numpy
def edges2edgelist(n,edges):
	edgelist = []
	for i in range(n):
		edgelist.append([])
	
	for father,child in edges:
		edgelist[father].append(child)
	return edgelist


edgelist = edges2edgelist(n,edges)

print(time.time(),"Converted to edgelist")


fp = Fixedpoint()

#print(fp.help())




fp.set('engine' , 'spacer')  #datalog/spacer zijn snel bij UNSAT, bmc is snel bij SAT


# print(fp.param_descrs())  # print parameter description set

#fp.set(timeout=3000)  # timeout in ms

fp.set('spacer.min_level', 200)

fp.set('spacer.max_level', 300)



fp.set('bmc.linear_unrolling_depth', 300)  # bound search depth of solver



P = [ Bool("p%s" % i) for i in range(n) ]
S = [ Bool("s%s" % i) for i in range(n) ]

# declare pebbles and spooks
for i in range(n):
	fp.declare_var(P[i])

for i in range(n):
	fp.declare_var(S[i])


#fp.fact()

f = Function('f', [B]*(2*n) + [B])

fp.register_relation(f)



# initial condition
fp.fact(f([False]*(2*n)))



# move conditions
for vertex, childlist in enumerate(edgelist):
	# add pebble
	new_state = P+S
	new_state[vertex] = True

	for child in childlist:
		new_state[child] = True 

	prev_state = list(new_state)
	prev_state[vertex] = False
	
	
	#print(prev_state, new_state)
	fp.rule(f(new_state), [AtMost(S+[max_spooks]), AtMost(new_state[:n]+[max_pebbles]), f(prev_state)],
				name = "add_pebble_vertex"+str(vertex))

	# remove pebble: 2 options
	#(1) all childs are pebbled
	new_state[vertex] = False
	prev_state[vertex] = True

	fp.rule(f(new_state), [AtMost(S+[max_spooks]), AtMost(prev_state[:n]+[max_pebbles]), f(prev_state)], 
				name = "(1)remove_pebble_vertex"+str(vertex))

	#(2) change pebble into spook
	new_state = P+S
	new_state[vertex] = False
	new_state[vertex+n] = True

	prev_state = P+S
	prev_state[vertex] = True
	fp.rule(f(new_state), [AtMost(S+[True]+[max_spooks]), AtMost(P+[max_pebbles]), f(prev_state)],
				name = "(2)remove_pebble_vertex"+str(vertex))


	# add spook
	#not needed to be added


	# remove spook
	new_state = P+S
	new_state[vertex+n] = False

	prev_state = P+S
	prev_state[vertex] = True

	fp.rule(f(new_state), [AtMost(S+[max_spooks]), AtMost(P+[True]+[max_pebbles]), f(prev_state)],
				name = "remove_spook_vertex"+str(vertex))
	
#print(fp)


final_clauses = [False]*(2*n)
for i in output_vertices:
	final_clauses[i] = True

#print(final_clauses)


print(time.time(),"Setted relations and rules")

print(time.time(),"Query starts...")

#fp.timeout(100000) #timeout in milliseconds

res = fp.query(f(final_clauses))
print(time.time(),"Query finished")
print(res)
if res == unknown:
	print(fp.reason_unknown())
#if res == sat:
	#ans = fp.get_answer()
	#print(ans)

