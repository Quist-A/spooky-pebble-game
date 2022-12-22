from z3 import *
import bmc

from Convert_bench_file_to_DAG import *
import time

def final_clauses(n, output_vertices):
	clauses = []
	for i in range(n):
		clauses.append(Not(S0[i]))
		if (i in output_vertices):
			clauses.append(P0[i])
		else:
			clauses.append(Not(P0[i]))
	return And(clauses)


def transition(max_pebbles,max_spooks,edges,n):
	# cardinality conditions
	card_pebbles = AtMost(P0+[max_pebbles])
	card_spooks = AtMost(S0+[max_spooks])
	
	# game move conditions
	game_move_conditions = move_conditions(edges,n)

	return And(card_pebbles,card_spooks,game_move_conditions)

def move_conditions(edges,n):
	add_pebble = 	[ And(
				Or(P0[father],Not(P1[father]),P0[child]),
				Or(P0[father],Not(P1[father]),P1[child])	) 
			for (father,child) in edges]

	remove_pebble = [ And(
				Or(Not(P0[father]),P1[father],S1[father],P0[child]),
				Or(Not(P0[father]),P1[father],S1[father],P1[child])	) 
			for (father,child) in edges]

	add_spook = 	[ And(
				Or(Not(S0[i]),S1[i],P0[i]),
				Or(Not(S0[i]),S1[i],Not(P1[i]))	) 
			for i in range(n)]

	remove_spook = 	[ And(
				Or(Not(S0[father]),S1[father],P1[father]),
				Or(Not(S0[father]),S1[father],P0[child]),
				Or(Not(S0[father]),S1[father],P1[child])	) 
			for (father,child) in edges]

	return And(add_pebble + remove_pebble + add_spook + remove_spook)

# Parameters
max_pebbles = 81
max_spooks = 20

benchmarkname = "c432"
n, output_vertices, edges = benchToDAG("benchmarks/ISCAS85/"+benchmarkname+".bench")



# list of pebbles
P0 = [ Bool("p0_%s" % (i)) for i in range(n) ]
# list of spooks
S0 = [ Bool("s0_%s" % (i)) for i in range(n) ]
vars0 = P0+S0

# list of pebbles
P1 = [ Bool("p1_%s" % (i)) for i in range(n) ]
# list of spooks
S1 = [ Bool("s1_%s" % (i)) for i in range(n) ]
vars1 = P1+S1
	

init = And( [ Not(var) for var in vars0 ] )
final = final_clauses(n, output_vertices)

trans = transition(max_pebbles,max_spooks,edges,n)


print("max pebbles",max_pebbles)
print("max spooks",max_spooks)
print("benchmarkname",benchmarkname)

bmc.bmc(init,trans,final,[],vars0,vars1)

print("max pebbles",max_pebbles)
print("max spooks",max_spooks)
print("benchmarkname",benchmarkname)
