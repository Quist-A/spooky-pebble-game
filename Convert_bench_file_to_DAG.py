import numpy as np



class dag:
    def __init__(self,filename=None):
        self.n = 0  # number of vertices
        self.output_vertices = []
        self.edges = []
	if filename != None:  
		self.filename = filename
		self.benchmarkname = filename.split("/")[-1][:-6]
        	self.importBench(filename)
        
    def importBench(self,filename):
        """
        Convert circuit in .bench file to a directed acyclic graph (DAG) representation.
	The inputs of the .bench file are not included in the grpah.
        
        Input:
        filename (str): filename of .bench file to be converted
                
        Output:
        n (int): number of vertices of DAG
        output_vertices (numpy array): integer labels of output vertices of DAG
        edges (numpy array): pairs of integer labels of edges of DAG
        """

        # open file
        with open(filename, "r") as file:
            data = file.read().splitlines()
            
        linenr = 0

        # read lines with inputs
        input_vertices = []
        while (data[linenr][:5] == "INPUT"):
            input_vertex = data[linenr][7:-1]
            input_vertices.append(input_vertex)
            linenr += 1
        Ninputs = len(input_vertices)
        
        # read lines with outputs
        while (data[linenr][:6] == "OUTPUT"):
            # don't do anything...
            linenr += 1   

        # forget about the n0 = gnd line
        linenr += 1 

        # read lines with edges
        while (data[linenr][0] == "n"):
            split = data[linenr].split(" = ")

            start_vertex = int(split[0][1:])-Ninputs-1  # gate

            start = split[1].index("(")
            end = split[1].index(")")
            end_vertices = split[1][start+2:end].split(", n")  # inputs of gate

            for end_vertex in end_vertices:
                if (end_vertex != '0'):
                    if (end_vertex not in input_vertices):
                        self.edges.append((start_vertex,int(end_vertex)-Ninputs-1))
            linenr += 1
        
        self.edges = np.array(self.edges)
        self.n = np.max(self.edges)+1

        # read lines with outputs
        while (linenr < len(data) and data[linenr][:2] == "po"):
            start = data[linenr].index("(")
            end = data[linenr].index(")")
            output_vertex = data[linenr][start+2:-1]
            if (output_vertex not in input_vertices):
                self.output_vertices.append(int(output_vertex)-Ninputs-1)
            #else:
            #    self.output_vertices.append(self.n)
            #    self.n += 1
            linenr += 1  

        
        self.output_vertices = np.array(self.output_vertices)
        


# EXAMPLE to import .bench file
#
#filename = "benchmarks/ISCAS85XMG/c7552.bench"
#dag = dag(filename)










#==========================================================================================
#
#                              SECOND OPTION TO IMPORT .BENCH FILES    (by function)
#
#==========================================================================================

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
    vertices = []

    for linenr in range(len(data)):  # check input file line by line
        if (data[linenr][:5] == 'INPUT'):
            # line defines new input vertex
            input_vertex = data[linenr][6:-1]
            input_vertices.append(input_vertex)
            vertices.append(input_vertex)
        else:
            
            if (data[linenr][:1] == 'G' or data[linenr][:1] == 'I' or data[linenr][:1] == 'g'):  
                # line defines new edge/edges
                
                split = data[linenr].split(" = ")

                start_vertex = split[0]  # gate

                vertices.append(start_vertex)

                start = split[1].index("(")
                end = split[1].index(")")
                end_vertices = split[1][start+1:end].split(", ")  # inputs of gate

                for end_vertex in end_vertices:
                    edges.append((start_vertex,end_vertex))

                    vertices.append(end_vertex)

            else: 
                if (data[linenr][:6] == 'OUTPUT'):
                    # line defines new output vertex
                    output_vertex = data[linenr][7:-1]
                    output_vertices.append(data[linenr][7:-1])
                    vertices.append(output_vertex)
                else:
                    # if no regular input and no empty line nor comment line -> print error
                    if (data[linenr] != '' and data[linenr][0] != '#'): 
                        print("ERROR: Line ", linenr, "in file", filename,
                              " could not be handled and was not taken into account")
    if print_progress:
        print("Data successfully converted to DAG")


    

    # count total number of vertices
    vertices = np.unique(vertices, return_inverse=True)  # remove duplicate vertices
    n = len(vertices[0])  # total number of vertices
    



    # convert vertex numbers in edges from string labels to integer labels
    
    if (rename_vertices):
        
        if print_progress:
            print("Renaming vertices...")
            
        

        dictionary = vertices[0]  
        # dictionary of values from string to integer: 
        # string at second index -> replace by integer 1
        # string at 15th index   -> replace by integer 14
        # etc etc
        # NOTE: dictionary is of type list to guarantee preserved order in for-loops

        # convert vertex numbers in edges
        nr_of_edges = len(edges)
        edges = np.array(edges).reshape(2*nr_of_edges)
        for j,x in enumerate(dictionary):
                edges[edges == x] = j
        edges = np.array(edges, dtype=int).reshape([nr_of_edges,2]) # convert array type from strings to integers


        # convert vertex numbers of input vertices
        input_vertices = np.array(input_vertices)
        for j,x in enumerate(dictionary):
            input_vertices[input_vertices == x] = j
        input_vertices = np.array(input_vertices, dtype=int) # convert array type from strings to integers


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
#benchmarkname = "c432"
#print(benchToDAG("benchmarks/ISCAS85/"+benchmarkname+".bench",print_progress=True))
