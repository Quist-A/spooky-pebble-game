def check_solution(states,edges,n,count):
    # check solution for errors

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
                                    print(states[time][vertex],states[time+1][vertex])
                        if (states[time][vertex] == 2 and states[time+1][vertex] == 0):
                            print("ERROR: the optimized solution is not valid, vertex unpebbled without spook",vertex,time)
                        if (states[time][vertex] == 0 and states[time+1][vertex] == 2):
                            print("WARNING: optimized solution has strange but valid behavior",vertex,time)
                return
    

def optimize_states(states,n,edgelist,count):
    """
    Optimize the sequential pebbling time of solution. Useless pebblings/unpebblings are detected and removed.
    
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
