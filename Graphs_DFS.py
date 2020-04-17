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
    
    #This is a function to return the nearest edge
    def min_edge(self):
        edge_keys = sorted(self.edges)
        return self.edges.get(edge_keys[0])

#Graph class to structure nodes
class Graph:
    def __init__(self, data):
        self.data = data
        self.nodes = {}

    #Functiont to add a node to the graph or edge to an existing edge
    def add_nodes(self):
        for line in self.data:
            _name = line[:3]
            _dest = line[4:7]
            _dist = int(line[-3:])
            _edge = { _dist : _dest }
            new_node = Node(_name)
            #If the node is not known we create it and add the first edge. If the node is known, we reference it and add the edge.
            #An edge is a dict where the key is the distance and the destination is the value 
            if _name not in self.nodes.keys():
                self.nodes.update( { _name : new_node} )
                self.nodes[_name].add_edge(_edge)
            else:
                self.nodes[_name].add_edge(_edge)

    def BFS(self, origin, dest):
            # Create a queue for BFS
            queue = []
            path = ""
            # Mark the source node as
            # visited and enqueue it
            queue.append(self.nodes[origin])
            self.nodes[origin].visited = True
            while queue:
                # Dequeue a node from
                # queue and print it
                origin = queue.pop(0)
                path += origin.name + "->"
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
            return path
                    
if __name__ == '__main__':

    file = 'Flights.txt'
    data = import_data(file)
    ap_graph = Graph( data )
    ap_graph.add_nodes()

    print(ap_graph.BFS('ACY', 'BDL'))
    
