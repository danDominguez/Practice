#Function to import the data from the text file
def import_data(f_name):
    try:
        with open(f_name, 'r') as fp:
            #Deal with all the empy lines -_-
            line = [line.rstrip() for line in fp]
            line = [line for line in line[1:] if line]
            return line
    except:
        print('Could not find file!')

#Node class for each airport
class Node:
    def __init__(self, name):
        self.name = name 
        self.dest = ""
        self.dist = 0
        self.edges = {}
        self.visited = False
    
    #Function to add an edge to a node
    #_edge is a dict where the { distance : destination }
    def add_edge(self, _edge):
        self.edges.update(_edge)
    
    #Return a list of the distances sorted 
    def min_edge(self):
        return sorted(self.edges)

#Graph class to structure nodes
class Graph:
    def __init__(self, data):
        self.nodes = {}

    #Function to add a node to the graph or edge to an existing edge
    def add_nodes(self):
        for line in data:
            line = line.split()
            _name = line[0]
            _dest = line[1]
            _dist = int(line[2])
            _edge = { _dist : _dest }
            new_node = Node(_name)
            #If the node is not known we create it and add the first edge. If the node is known, we reference it and add the edge.
            #An edge is a dict where the key is the distance and the destination is the value 
            if _name not in self.nodes.keys():
                self.nodes.update( { _name : new_node} )
                self.nodes[_name].add_edge(_edge)
            else:
                self.nodes[_name].add_edge(_edge)
    #Function to print the graph
    def print_graph(self):
        for node_name, node in self.nodes.items():
            print(node_name, node.edges)

    def BFS(self, origin, dest):
            # Create a queue for BFS
            queue = []
            path = ""
            count = 0
            # Mark the source node as
            # visited and enqueue it
            queue.append(self.nodes[origin])
            self.nodes[origin].visited = True
            while queue:
                # Dequeue a node from
                # queue and print it
                origin = queue.pop(0)
                path += origin.name + "->"
                count+=1
                # Get all adjacent nodes of the
                # dequeued node s. If a adjacent node
                # has not been visited, then mark it
                # visited and enqueue it
                edges = [ edge for edge in origin.edges.values() ]
                if dest in edges:
                    path += dest
                    break
                for edge in edges:
                    _curr_edge = self.nodes[edge]
                    if _curr_edge.visited == False:
                        _curr_edge.visited = True
                        queue.append(_curr_edge)
            return (count, path)

#Adjacenty Matrix to represent our data
class Matrix:
    def __init__(self, data):
        #Create a list of names for the nodes.
        self.uniques = []
        [self.uniques.append(line[:3]) for line in data if line[:3] not in self.uniques]
        self.num_nodes = len(self.uniques)
        #Create a matrix num_nodes x num_nodes in size.
        self._matrix = [[0 for node in range(self.num_nodes)] for node in range(self.num_nodes)]

    #This function will print the matrix. Accepts a range as an argument (58x58 was a bit much for my screens)
    def print_matrix(self, range = 10):
        print("i:node\t{}".format("\t".join(self.uniques[:range])))
        for index, row in enumerate(self._matrix[:range]):
           print("{}:{}\t{}".format(index,self.uniques[index], row[:range]))

    #This function will add the edge by first finding the coordinating index value
    def add_edge(self, origin, destination , distance):
        for index, name in enumerate(self.uniques):
            if name == origin:
                ori_index = index
            if name == destination:
                des_index = index
        self._matrix[ori_index][des_index] = int(distance)

    #Function to loop over the data list and create edges
    def add_edges(self):
        for line in data:
            line = line.split()
            ori = line[0]
            des = line[1]
            dis = line[2]
            self.add_edge(ori, des, dis)

    #This function will return the lowest value distance in the array and the index as a tuple (index, value)
    def get_min(self, row):
        no_zeroes = [ distance for distance in row if distance > 0]
        no_zeroes.sort()
        count = 0
        #Keep looping over the row to find an index that has not been used yet
        while(count<len(no_zeroes)):
            #pop the first node from the list to use as a search 
            curr_search = no_zeroes.pop(0)
            #Loop over the row and get the index for the matching distance
            for index, distance in enumerate(row):
                #If the index has not been visited yet then we use it
                if index not in self.visited:
                    if distance == curr_search:
                        return((index, distance))
            count +=1

    #This is my implementation if dijkstras shortest path algorithm
    #Returns a tuple where ((int)duration, (string)path)
    def dijkstras(self, origin, dest):
        dist = 0
        self.visited = []
        for index, name in enumerate(self.uniques):
            if name == origin:
                ori_index = index
            if name == dest:
                des_index = index        
        #Add the origin node to the visited list
        self.visited.append(ori_index)
        #This will stop looping when we have visited every node in the graph or the return is met 
        while(len(self.visited) < len(self.uniques)):
            #If there is a direct path from the origin node just return the distance we are done.
            v_base = self._matrix[ori_index][des_index]
            if v_base:
                dist+=v_base
                path = [self.uniques[_] for _ in self.visited]
                return (dist, "->".join(path))

            #Get the index and distance of the nearest adjacent node
            min_index, min_dist = self.get_min(self._matrix[ori_index])
            dist += min_dist
            ori_index = min_index
            self.visited.append(min_index)

if __name__ == '__main__':
    #Import the data and return an array containing each line.
    file = 'Flights.txt'
    data = import_data(file)
    #Part 1. Perform Breadth First Search on our Airport Node to fin0d flight path between two nodes based on layovers (Book a flight!)
    #This solution uses an adjaceny list
    ap_graph = Graph(data)
    ap_graph.add_nodes()
    count, path = ap_graph.BFS('ACY', 'BOS')
    print('\nBreadth First Search:')
    print("Plane Count: {}\nFlight Path: {}".format(count,path))

    #Part 2. Perform Dijkstras Algorithm to find the least amount of time required based on distance using adjaceny matrix
    #This solution uses an adjaceny matrix
    ap_matrix = Matrix(data)
    ap_matrix.add_edges()
    duration, path = ap_matrix.dijkstras('ACY','BOS')
    print('\nDijkstras:')
    print("Flight Duration: {}\nFlight Path: {}".format(duration, path))

