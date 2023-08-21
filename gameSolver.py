"""
Initially copied from Z3Prover/doc

Changed by Arend-Jan Quist

"""
import time
from z3 import *
from bmcFormula import *
from solutionOptimizer import optimize_states, check_solution 


index = 0  # index to enumerate fresh variables
def fresh(round, s):
    global index
    var = Const("!f%d_%d" % (round, index), s)
    index += 1
    return var
    
def freshq(round, s):
    global index
    var = Const("q%d_%d" % (round, index), s)
    index += 1
    return var

def zipp(xs, ys):
    return [p for p in zip(xs, ys)]
    
def edges2edgelist(n,edges):
    """
    Convert list of edges to adjacency list per vertex.
    """
    edgelist = []
    for i in range(n):
        edgelist.append([])
    
    for father,child in edges:
        edgelist[child].append(father)
    return edgelist

def bmc(init, trans, goal, xs, xns, n, edges, benchmarkname, max_pebbles, max_spooks, Twait = 7, seed = 0, verbose = True):
    """
    BMC solver for spooky pebble game.

    Inputs:
    

    Outputs:
    
    """
    s = Solver()
    timeout = Twait*1000  # timeout in ms
    s.set('timeout',timeout)
    #s.set('lemmas2console',True)
    #s.set('threads',8)   
    s.set('random_seed',seed) 

    s.add(init)
    count = 0 # round/iteration of bmc
    
    max_time = 300  # max number of bmc iterations
    check = [True]*max_time  # solve rounds
    
    variables = []  # list of pebble/spook variables
    variables.append(xs)
    variables.append(xns)
    
    #solutions = []
    

    edgelist = edges2edgelist(n,edges)
        
    
    while count < max_time:
        if verbose:
            print("iteration ", count)
        
        if check[count]:  # check whether this count must be searched
            q = freshq(count, BoolSort()) 
            s.add(Or(Not(q),goal))   # q implies goal
            
            res = solve(s,q,count,timeout,check)  # run SAT solver
            if verbose:
                print(res)
            
            if res == sat:  # if solution is found
                solution = s.model()  
                
                # calculate info of solution
                states = model2states(solution,n,count)
                seqT, pebbles_used, spooks_used = calc_solution_info(states,n)
                #print(states.tolist())  # for debugging
                
                if verbose:
                    print("solution: p ",pebbles_used,", s ",spooks_used, ", parT ",count,", seqT ", seqT)
                
                # optimize sequential pebbling time
                states = optimize_states(states,n,edgelist,count)
                
                # check solution for errors, for debugging
                #check_solution(states,edges,n,count)
                #print(states) # for debugging
                
                opt_seqT, opt_pebbles_used, opt_spooks_used = calc_solution_info(states,n)
                
                # output solution
                if verbose:
                    print("optimized solution: p ",opt_pebbles_used,", s ",opt_spooks_used, ", parT ",count,", seqT ", opt_seqT)
                    return
                else:
                    return (pebbles_used,spooks_used,count,seqT),(opt_pebbles_used,opt_spooks_used,count,opt_seqT)
        


        # add counter and set variable index to 0
        count += 1
        global index
        index = 0
        
        
        if (count > 1):
            # define new transition relation
            ys = [fresh(count, x.sort()) for x in xs]
            trans = substitute(trans, 
                               zipp(xns + xs, ys + xns))
            goal = substitute(goal, zipp(xns, ys))
            variables.append(ys)
            xs, xns = xns, ys 
        else:
            goal = substitute(goal, zipp(xs, xns))
        
        # update transition relation
        s.add(trans)
        
        
    
    
    #print(solutions)
    if verbose:
        print("BMC solver: no solution found in max_time")
        return
    else:
        return (0,0,0,0),(0,0,0,0)

def solve(s,q,count,timeout,check):
    """
    Solve solution of pebble game for given game s with goal q.
    """
    res = s.check(q)  # call SAT solver
    if unknown == res: # run out of time
        # disable check for next interations
        for i in range(5):
            try:
                check[count+i] = False
            except:
                return 0
    return res
    
def model2states(solution, n, parT):
    """
    Convert the Z3 model solution of spooky pebble game to accessible matrix form of states.
    
    Input: solution is of type Solver.model() for a game solution.
    
    Output: in the form of matrix of pebbles/spooks per time and vertex
    0 empty, 1 pebble, 2 spook
    """
    states = np.zeros(n*(parT+1),dtype=int).reshape(parT+1,n)     

    # read solution line by line
    for x in solution.decls():
        
        if solution[x]:
            x = x.name()
            if x[0] == '!':
                T, vertex = x[2:].split("_")
                T, vertex = int(T), int(vertex)
                if T > 1:
                    if vertex < n: # pebble variable
                        states[T][vertex] += 1
                    elif vertex < 2*n: # spook variable
                        vertex -= n
                        states[T][vertex] += 2
            elif x[0] == 'p':
                T, vertex = x[1:].split("_")
                T, vertex = int(T), int(vertex)
                states[T][vertex] += 1
            elif x[0] == 's':
                T, vertex = x[1:].split("_")
                T, vertex = int(T), int(vertex)
                states[T][vertex] += 2
    return states
    
    
def calc_solution_info(states,n, verbose = False):
    """
    Calculate sequential time, nr. of pebbles and spooks used for parallel solution.
    
    Input:
    'states': matrix of states of (parallel) spooky pebble game solution
    'n': number of vertices in DAG

    Output:
    sequential time, pebbles used in game, spooks used in game
    """
    
    sum = np.add(states[:-1],-states[1:])
    seqT = np.count_nonzero(sum)

    pebbles_used = n-np.min(np.count_nonzero(states-1, axis = 1))
    spooks_used = n-np.min(np.count_nonzero(states-2, axis = 1))
    
    #if verbose:
        #print("Sequential time:",seqT)
        #print("Maximal operations per parallel timestep:",np.max(np.count_nonzero(sum, axis = 1)))
        #print("Parallel time:",parT)
        #print("Number of pebbles used: ",pebbles_used)
        #print("Number of spooks used: ",spooks_used)
    
    return seqT, pebbles_used, spooks_used       
    
def spooky_solver(DAG,benchmarkname,max_pebbles,max_spooks,Twait = 15,seed = 0):
    """
    Setup and run solver for spooky pebble game
    """
    starttime = time.time()

    init,trans,final,vars0,vars1 = setup_bmc_formulae(DAG,max_pebbles,max_spooks)

    (pebbles_used,spooks_used,count,seqT),(opt_pebbles_used,opt_spooks_used,opt_count,opt_seqT) = bmc(init,trans,final,vars0,vars1,DAG.n,DAG.edges,benchmarkname,max_pebbles,max_spooks,Twait,seed,False)

    endtime = time.time()
    
    runtime = endtime-starttime
    
    return (pebbles_used,spooks_used,count,seqT),(opt_pebbles_used,opt_spooks_used,opt_count,opt_seqT),runtime



#=========================================================================================


# This function is mainly used for testing and debugging

def run_bmc_manually():  
    starttime = time.time()

    # Parameters
    max_pebbles = 70
    max_spooks = 20 #np.inf

    benchmarkname = "c499"
    #n, output_vertices, edges = benchToDAG("benchmarks/ISCAS85/"+benchmarkname+".bench")
    DAG = dag("benchmarks/ISCAS85XMG/"+benchmarkname+".bench")

    """
    #Example DAG
    benchmarkname = "linegraph5"
    DAG.n = 5
    DAG.output_vertices = [0]
    DAG.edges = [(0,1),(1,2),(2,3),(3,4)]
    DAG.benchmarkname = benchmarkname
    """
    """
    #Example DAG
    # create random DAG
    benchmarkname = "randomDAG"
    DAG.benchmarkname = benchmarkname
    DAG.n = 30
    n = DAG.n 
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
    DAG.output_vertices = output_vertices.tolist()

    DAG.edges = edges

    print("Number of edges:",len(edges))
    print("Number of input vertices:",len(input_vertices))
    print("Number of output vertices:",len(output_vertices))
    print("Input vertices:",input_vertices)
    print("Output vertices:",output_vertices)
    """
    """
    benchmarkname = "testDAG"
    DAG.n = 7
    DAG.output_vertices = [3,6]
    DAG.edges = [(3,2),(2,1),(1,0),(6,5),(5,4),(4,0)]
    DAG.benchmarkname = benchmarkname
    """

    init,trans,final,vars0,vars1 = setup_bmc_formulae(DAG,max_pebbles,max_spooks)

    print("max pebbles",max_pebbles)
    print("max spooks",max_spooks)
    print("benchmarkname",benchmarkname)

    bmc(init,trans,final,vars0,vars1,DAG.n,DAG.edges,benchmarkname,max_pebbles,max_spooks)

    endtime = time.time()
    print("Solution found in ", endtime-starttime," seconds")

    print("max pebbles",max_pebbles)
    print("max spooks",max_spooks)
    print("benchmarkname",benchmarkname)
    print("number of vertices",DAG.n)
    
    return


"""
run_bmc_manually()
"""
