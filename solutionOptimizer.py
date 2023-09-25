import numpy as np

def check_solution(states,edges,n,count):
    """    
    Check solution for errors
    """  
    childedgelist = []
    for i in range(n):
        childedgelist.append([])
    
    for child,father in edges:
        childedgelist[child].append(father)
        
    
    # check validity of solution
    for time in range(count):
        for vertex in range(n):
            if (states[time][vertex] == 0 and states[time+1][vertex] == 1) or (states[time][vertex] == 1 and states[time+1][vertex] == 0) or (states[time][vertex] == 2 and states[time+1][vertex] == 1): # vertex pebbled or unpebbled or unspooked
                for child in childedgelist[vertex]:
                    if states[time][child] != 1 or states[time+1][child] != 1:
                        print("ERROR: the optimized solution is not valid, child not pebbled", vertex,child,time)
                        print("Transition",states[time][vertex],states[time+1][vertex])
            if (states[time][vertex] == 2 and states[time+1][vertex] == 0):
                print("ERROR: the optimized solution is not valid, vertex unpebbled without spook",vertex,time)
            if (states[time][vertex] == 0 and states[time+1][vertex] == 2):
                print("WARNING: optimized solution has strange but valid behavior",vertex,time)
    return
    

def remove_useless_pebbling(states,n,edgelist,count):
    """
    Optimize the sequential pebbling time of solution. 
    Pebbles that are not used to (un)pebble or unspook a succesor are detected and removed.
    
    Output: optimized solution in the form of a state matrix
    """
    for time in range(count,0,-1):
        for vertex in range(n):
            if states[time][vertex] == 0 and states[time-1][vertex] == 1:
                father_pebbled = False
            
                t = time
                while not(father_pebbled):
                    
                    if states[t][vertex] == 2: # if pebble was placed to unspook
                        break
                    
                    if states[t][vertex] == 0 and time != t and not(father_pebbled): # at this timestep the vertex was pebbled
                    #print()
                        for i in range(t,time,1): # remove the pebbles at the timestep
                            states[i][vertex] = 0
                        break
                    
                    for father in edgelist[vertex]: #check if a father is pebbled/unpebbled or unspooked during pebbling of vertex
                        if (states[t][father] == 0 and states[t-1][father] == 1) or (states[t][father] == 1 and states[t-1][father] == 0) or (states[t][father] == 1 and states[t-1][father] == 2):
                            father_pebbled = True
                            break
                        #print(vertex)

                    t-=1 # go to previous timestep
                
    return states
    
def replace_spook_by_pebble_asap(states,n,inv_edgelist,max_pebbles,count):
    """
    Optimize the sequential pebbling time of solution. 
    Remove spooks as soon as their inputs are pebbled and there is a pebble available.
    
    Output: optimized solution in the form of a state matrix
    """
    pebbles_used = n-np.count_nonzero(states-1, axis = 1)
    
    for time in range(1,count+1,1):
        if pebbles_used[time] < max_pebbles: # maximal number of pebbles not reached
            for vertex in range(n):
                if states[time][vertex] == 1 and states[time-1][vertex] == 2:  # unspooking move
                    inputs = inv_edgelist[vertex]
                    
                    t = time-1
                    while(t>0 and states[t][vertex] == 2):
                        
                        # what if states[t][vertex] == 0
                        

                        if pebbles_used[t]>=max_pebbles:
                            break
                        
                        replace = True
                        for inpt in inputs:
                            if (states[t][inpt] != 1 or states[t-1][inpt] != 1): # input still pebbled
                                replace = False
                                break
                        

                                
                        if replace:
                            for x in range(t,time):
                                if (states[x][vertex] != 1):
                                    pebbles_used[x] += 1
                                    states[x][vertex] = 1
                                
                            #print("asap replaced",t,vertex)
                        t -= 1

    return states
    
def delay_spook_placement(states,n,max_pebbles,count):
    """
    Optimize the sequential pebbling time of solution. 
    Delay the spook placements if enough pebbles are available. 
    
    Output: optimized solution in the form of a state matrix
    """
    pebbles_used = n-np.count_nonzero(states-1, axis = 1)
    
    for time in range(1,count+1,1):
        if pebbles_used[time] < max_pebbles: # maximal number of pebbles not reached
            
            #delayable_vertixes = []
            for vertex in range(n):
                if states[time][vertex] == 2 and states[time-1][vertex] == 1:  # spooking move
                    #delayable_vertices.append(vertex)
                    #print("delayed at time",time)                    
                    states[time][vertex] = 1
                    pebbles_used[time] += 1
                    
                    
                    if pebbles_used[time] >= max_pebbles:
                        break
                    
            #for vertex in delayable_vertices:
            #    states[time][vertex] = 1
    return states
    
def expedite_unpebbling(states,n,(edgelist,inv_edgelist),count):
    """
    Optimize the sequential pebbling time and number of pebbles of solution. 
    Expedite pebble placements if enough inputs are already available and pebble is not used yet. 
    
    Output: optimized solution in the form of a state matrix
    """
    
    for time in range(1,count+1,1):
        for vertex in range(n):
            if states[time][vertex] == 0 and states[time-1][vertex] == 1:  # unpebbling move
                inputs = inv_edgelist[vertex]
                outputs = edgelist[vertex]
                
                t = time-1
                used_for_output = False
                while(t>0 and states[t][vertex] == 1 and not(used_for_output)):
                    
                    # what if states[t][vertex] == 2
                    
                    expedite = True
                    
                    for inpt in inputs:
                        if (states[t][inpt] != 1 or states[t-1][inpt] != 1): # input still pebbled
                            expedite = False
                            break
                    for outpt in outputs:
                        if ((states[t][outpt] != states[t+1][outpt] and not(states[t][outpt] == 1 and states[t+1][outpt] == 2)) or (states[t-1][outpt] != states[t][outpt] and not(states[t-1][outpt] == 1 and states[t][outpt] == 2))): #output (un)pebbled or unspooked
                            expedite = False
                            used_for_output = True
                            break
                            
                    if expedite and states[t-1][vertex] != 2:
                        for x in range(t,time):
                            states[x][vertex] = 0  #expedite pebbling
                        #print("expedited",t,vertex)
                    t -= 1
                
                #if (states[t][vertex] == 2):
                #    print(states[t-1][vertex],states[t][vertex],states[t+1][vertex])
                #    states[t+1][vertex] = 1
                    # it would be better to run remove_spook_asap instead on this vertex
                    
            #for vertex in delayable_vertices:
            #    states[time][vertex] = 1
    
    return states

def delay_pebble_placement(states,n,(edgelist,inv_edgelist),count):
    """
    Optimize the sequential pebbling time and number of pebbles of solution. 
    Delay the pebble placements if enough inputs are still available and pebble is not used already. 
    
    Output: optimized solution in the form of a state matrix
    """
    
    for time in range(count,0,-1):
        for vertex in range(n):
            if states[time][vertex] == 1 and states[time-1][vertex] == 0:  # pebbling move
                inputs = inv_edgelist[vertex]
                outputs = edgelist[vertex]
                
                t = time
                used_for_output = False
                while(t<count and states[t][vertex] == 1 and not(used_for_output)):
                    
                    # what if states[t][vertex] == 2  ==>  we can remove the spook
                    
                    delay = True
                    
                    for inpt in inputs:
                        if (states[t][inpt] != 1 or states[t-1][inpt] != 1): # input still pebbled
                            delay = False
                            break
                    for outpt in outputs:
                        if ((states[t][outpt] != states[t+1][outpt] and not(states[t][outpt] == 1 and states[t+1][outpt] == 2)) or (states[t-1][outpt] != states[t][outpt] and not(states[t-1][outpt] == 1 and states[t][outpt] == 2))): #output (un)pebbled or unspooked
                            delay = False
                            used_for_output = True
                            break
                            
                    if delay:
                        for x in range(time,t):
                            states[x][vertex] = 0  #delay pebbling
                        #print("delayed",t,vertex)
                    t += 1
                    
            #for vertex in delayable_vertices:
            #    states[time][vertex] = 1
    return states
    
    
def remove_useless_spookings(states,n,inv_edgelist,count):
    """
    Optimize the sequential pebbling time of solution. 
    Spookings moves with all inputs pebbled are changed into unpebbling moves. 
    
    Output: optimized solution in the form of a state matrix
    """
    for time in range(count,0,-1):
        for vertex in range(n):
            if states[time][vertex] == 2 and states[time-1][vertex] == 1:  # spooking move
            
                useless_spooking = True
                for child in inv_edgelist[vertex]: # check if inputs of vertex were pebbled at time
                    if not(states[time][child] == 1 and states[time-1][child] == 1):
                        useless_spooking = False
                        break
                
                if useless_spooking:
                    #print("unspooked")
                    # remove spook
                    t=time
                    while(states[t][vertex] == 2):
                        states[t][vertex] = 0
                        t += 1
                    
    return states

def par2seq(states,n,count,(max_pebbles,max_spooks)):
    """
    Convert parrallel solution to sequential pebbling solution.
    
    Output: sequential pebbling solution [np array] and number of sequential moves 
    """
    
    seqStates = []
    seqCount = count
    
    states = states.tolist()
    
    seqStates.append(states[0])
    
    for time in range(0,count):
        pebbling = []
        unpebbling = []
        spooking = []
        unspooking = []
        
        for vertex in range(n):
            if states[time][vertex] != states[time+1][vertex]:
                start = states[time][vertex]
                next = states[time+1][vertex]
                if start == 0 and next == 1:
                    pebbling.append(vertex)
                elif start == 1 and next == 0:
                    unpebbling.append(vertex)
                elif start == 1 and next == 2:
                    spooking.append(vertex)
                elif start == 2 and next == 1:
                    unspooking.append(vertex)
                    
        for vertex in unpebbling:
            newState = list(seqStates[-1])
            newState[vertex] = 0
            seqStates.append(newState)
        """
        for vertex in unspooking:
            newState = list(seqStates[-1])
            newState[vertex] = 1
            seqStates.append(newState)
            
        for vertex in spooking:
            newState = list(seqStates[-1])
            newState[vertex] = 2
            seqStates.append(newState)
        """
        pebbles_used = n-np.count_nonzero(np.array(seqStates[-1])-1)
        spooks_used = n-np.count_nonzero(np.array(seqStates[-1])-2)
        
        while(len(unspooking)>0 or len(spooking)>0):
            if (pebbles_used >= max_pebbles) and (spooks_used >= max_spooks): 
                # spook and unspook in one timestep
                newState = list(seqStates[-1])
                vertex = unspooking.pop(0)
                newState[vertex] = 1
                vertex = spooking.pop(0)
                newState[vertex] = 2
                seqStates.append(newState)
        
            if len(unspooking)>0 and (pebbles_used < max_pebbles):
                vertex = unspooking.pop(0)
                newState = list(seqStates[-1])
                newState[vertex] = 1
                seqStates.append(newState)
                
                pebbles_used += 1
                spooks_used -= 1
            
            if len(spooking)>0 and (spooks_used < max_spooks):
                vertex = spooking.pop(0)
                newState = list(seqStates[-1])
                newState[vertex] = 2
                seqStates.append(newState)
                
                pebbles_used -= 1
                spooks_used += 1
        
        for vertex in pebbling:
            newState = list(seqStates[-1])
            newState[vertex] = 1
            seqStates.append(newState)
    
    seqCount = len(seqStates)-1
    seqStates = np.array(seqStates)
    #print([Solution] seqStates)
    return (seqStates,seqCount)

def calc_solution_info_temp(states,n, verbose = True):
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
    
    #print("Pebbles:",(n-np.count_nonzero(states-1, axis = 1)))#.tolist())
    #print("Spooks: ",(n-np.count_nonzero(states-2, axis = 1)))#.tolist())
    
    if verbose:
        #print("Sequential time:",seqT)
        #print("Maximal operations per parallel timestep:",np.max(np.count_nonzero(sum, axis = 1)))
        #print("Parallel time:",parT)
        print("Number of pebbles used: ",pebbles_used)
        print("Number of spooks used: ",spooks_used)
    
    return seqT, pebbles_used, spooks_used 



def optimize_states(states,n,(edgelist,inv_edgelist),(max_pebbles,max_spooks),count):
    """
    Optimize the sequential pebbling time of solution. 
    Useless pebblings/unpebblings/spookings/unspookings are detected and removed.
    
    Output: optimized solution in the form of a state matrix
    """
    states = remove_useless_pebbling(states,n,edgelist,count)
    states = remove_useless_spookings(states,n,inv_edgelist,count)
    
    for x in range(10):

        (states,count) = par2seq(states,n,count,(max_pebbles,max_spooks))

        calc_solution_info_temp(states,n)
                
        states = delay_pebble_placement(states,n,(edgelist,inv_edgelist),count)           
        states = expedite_unpebbling(states,n,(edgelist,inv_edgelist),count)

        states = delay_spook_placement(states,n,max_pebbles,count)
        states = replace_spook_by_pebble_asap(states,n,inv_edgelist,max_pebbles,count)
        
        states = remove_useless_spookings(states,n,inv_edgelist,count)
        states = remove_useless_pebbling(states,n,edgelist,count)
    
    for x in range(10):
        print("x=",x)
        (states,count) = par2seq(states,n,count,(max_pebbles,max_spooks))
        print(count)
        calc_solution_info_temp(states,n)
        
        
        states = remove_useless_spookings(states,n,inv_edgelist,count)
        
        states = replace_spook_by_pebble_asap(states,n,inv_edgelist,max_pebbles,count)

        #calc_solution_info_temp(states,n)
        states = delay_pebble_placement(states,n,(edgelist,inv_edgelist),count)
        #calc_solution_info_temp(states,n)
        states = remove_useless_pebbling(states,n,edgelist,count)
        #calc_solution_info_temp(states,n)
        states = delay_spook_placement(states,n,max_pebbles,count)
        #calc_solution_info_temp(states,n)
        
        states = expedite_unpebbling(states,n,(edgelist,inv_edgelist),count)
        #calc_solution_info_temp(states,n)

        

    
    return (states, count)
