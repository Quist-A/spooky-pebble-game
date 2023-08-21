from z3 import *

from Convert_bench_file_to_DAG import *
import time

def final_clauses((P0,S0,P1,S1),n, output_vertices):
	clauses = []
	for i in range(n):
		clauses.append(Not(S0[i]))
		if (i in output_vertices):
			clauses.append(P0[i])
		else:
			clauses.append(Not(P0[i]))
	return And(clauses)
	

def transition((P0,S0,P1,S1),max_pebbles,max_spooks,edges,n):
	"""
	Define transition relation for spooky pebble game
	"""
	# cardinality conditions
	card_pebbles = AtMost(P0+[max_pebbles])
	if max_spooks != np.inf:
		card_spooks = AtMost(S0+[max_spooks])
	else: 
		card_spooks = And()
	
	# game move conditions
	game_move_conditions = move_conditions((P0,S0,P1,S1),edges,n)

	# one step per timestep
	unit_timestep = timestep_condition((P0,S0,P1,S1),n)
	
	return And(card_pebbles,card_spooks,game_move_conditions)#,unit_timestep) #


def timestep_condition((P0,S0,P1,S1),n):
	"""
	Define clauses to make sure that at most one pebble is moved per timestep

	For all vertices the new pebble value is XORed with the old pebble value. 
	Then we check that no pair of vertices has both XOR value 1. This formula 
	is worked out as CNF to simplify calculation for the SAT solver.
	"""
	"""clauses = []
	for i in range (n):
		for j in range(i):
			clauses.append(Or(P0[i],Not(P1[i]),P0[j],Not(P1[j])))
			clauses.append(Or(Not(P0[i]),P1[i],P0[j],Not(P1[j])))
			clauses.append(Or(P0[i],Not(P1[i]),Not(P0[j]),P1[j]))
			clauses.append(Or(Not(P0[i]),P1[i],Not(P0[j]),P1[j]))
	return And(clauses)
	"""
	clauses = []
	for p0,p1 in zip(P0,P1):
		clauses.append(Xor(p0,p1))
	return AtMost(clauses+[1])


def move_conditions((P0,S0,P1,S1),edges,n):
	add_pebble = 	[ And(
				Or(P0[father],Not(P1[father]),P0[child]),
				Or(P0[father],Not(P1[father]),P1[child])	) 
			for (father,child) in edges]+[ 	
				Or(P0[i],Not(P1[i]),Not(S1[i]))
			for i in range(n)]
	

	remove_pebble = [ And(
				Or(Not(P0[father]),P1[father],S1[father],P0[child]),
				Or(Not(P0[father]),P1[father],S1[father],P1[child])	) 
			for (father,child) in edges]

	add_spook = 	[ And(
				Or(Not(S1[i]),S0[i],P0[i]),
				Or(Not(S1[i]),S0[i],Not(P1[i]))	) 
			for i in range(n)]

	remove_spook = 	[ And(
				Or(Not(S0[father]),S1[father],P1[father]),
				Or(Not(S0[father]),S1[father],P0[child]),
				Or(Not(S0[father]),S1[father],P1[child])	) 
			for (father,child) in edges]

	return And(add_pebble + remove_pebble + add_spook + remove_spook)


def transitionIrreversible((P0,P1),max_pebbles,edges,n):
	"""
	Define transition relation for irreversible black pebble game
	"""
	# cardinality conditions
	card_pebbles = AtMost(P0+[max_pebbles])
	
	# game move conditions
	add_pebble = 	[ And(
				Or(P0[father],Not(P1[father]),P0[child]),
				Or(P0[father],Not(P1[father]),P1[child])	) 
			for (father,child) in edges]
	return And(card_pebbles,And(add_pebble))

def setup_bmc_formulae(DAG,max_pebbles,max_spooks):
	"""
	Setup SAT formula in Z3 expression as input for a Z3 bounded model checker (SAT solver). 
	
	Output:
	Every output is in the form of Z3 SAT solver expression.
	init: initial condition for pebble game, in terms of vars0
	trans: transition relation between timesteps of pebble game, in terms of vars0 to vars1
	final: final condition for pebble game, in terms of vars0
	vars0: initial variables of bmc
	vars1: output variables of transition relation
	"""

	n = DAG.n
	output_vertices = DAG.output_vertices
	edges = DAG.edges

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

	# define initial and final clauses
	init = And( [ Not(var0) for var0 in vars0 ] )
	final = final_clauses((P0,S0,P1,S1),n, output_vertices)

	#trans = transitionIrreversible((P0,P1),max_pebbles,edges,n)  # transition relation for black (irreversible) pebble game
	trans = transition((P0,S0,P1,S1),max_pebbles,max_spooks,edges,n)  # transition relation for spooky pebble game
	
	return init,trans,final,vars0,vars1
