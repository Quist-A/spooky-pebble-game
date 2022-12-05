import numpy as np

def benchToDAG(filename, rename_vertices = True, print_progress = False):
    """
    Convert circuit in .bench file to a directed acyclic graph (DAG) representation.
    
    Input:
    filename (str): filename of .bench file to be converted
    rename_vertices (bool): convert vertex labels of DAG from strings to integers
    print_progress (bool): print progress during run of program
    
    Output:
    n (int): number of vertices of DAG
    output_vertices (list / numpy array): string resp. integer labels of output vertices of DAG
    edges (list / numpy array): pairs of string resp. integer labels of edges of DAG
    """
    # import file
    if print_progress:
        print("Reading input file...")
        
    with open(filename, "r") as file:
        data = file.read().splitlines()


    # convert .bench file to DAG
    if print_progress:
        print("Converting input file to DAG...")
    input_vertices = [] # not necessarily needed for spooky pebble game solver
    output_vertices = []
    edges = []
    #vertices = []

    for linenr in range(len(data)):  # check input file line by line
        if (data[linenr][:5] == 'INPUT'):
            # line defines new input vertex
            input_vertices.append(linenr)
        else:
            
            if (data[linenr][:1] == 'G' or data[linenr][:1] == 'I' or data[linenr][:1] == 'g'):  
                # line defines new edge/edges
                
                split = data[linenr].split(" = ")

                start_vertex = split[0]  # gate

                #vertices.append(start_vertex)

                start = split[1].index("(")
                end = split[1].index(")")
                end_vertices = split[1][start+1:end].split(", ")  # inputs of gate

                for end_vertex in end_vertices:
                    edges.append((start_vertex,end_vertex))

                    #vertices.append(end_vertex)

            else: 
                if (data[linenr][:6] == 'OUTPUT'):
                    # line defines new output vertex
                    output_vertices.append(data[linenr][7:-1])
                else:
                    # if no regular input and no empty line nor comment line -> print error
                    if (data[linenr] != '' and data[linenr][0] != '#'): 
                        print("ERROR: Line ", linenr, "in file", filename,
                              " could not be handled and was not taken into account")
    if print_progress:
        print("Data successfully converted to DAG")


    

    # count total number of vertices
    vertices = np.unique(edges, return_inverse=True)  # remove duplicate vertices
    n = len(vertices[0])  # total number of vertices
    

    
    # convert vertex numbers in edges from string labels to integer labels
    
    if (rename_vertices):
        
        if print_progress:
            print("Renaming vertices...")
            
        # convert vertex numbers in edges
        edges = vertices[1].reshape([len(edges),2])

        dictionary = vertices[0]  
        # dictionary of values from string to integer: 
        # string at second index -> replace by integer 1
        # string at 15th index   -> replace by integer 14
        # etc etc


        # convert vertex numbers of output vertices
        output_vertices = np.array(output_vertices)
        for j,x in enumerate(dictionary):
            output_vertices[output_vertices == x] = j
            """ other option:
            for i in range(len(output_vertices)):
                if (output_vertices[i] == x):
                    output_vertices[i] = j"""
        output_vertices = np.array(output_vertices, dtype=int) # convert array type from strings to integers
    
    
    # input_vertices can also be returned (if vertex numbers are converted)
    return n, output_vertices, edges


# EXAMPLE to run program
#
#filename = "s38584.bench"
#benchToDAG(filename)
