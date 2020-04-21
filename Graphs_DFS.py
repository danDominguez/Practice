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

if __name__ == '__main__':
    #Import the data and return an array containing each line.
    file = 'Flights.txt'
    data = import_data(file)
    #Part 1. Perform Breadth First Search on our Airport Node to fin0d flight path between two nodes based on layovers (Book a flight!)
    #This solution uses an adjaceny list
    ap_graph = Graph(data)
    ap_graph.add_nodes()
    count, path = ap_graph.BFS('ACY', 'BOS')
    print("Breadth First Search:\n Plane Count: {}\nFlight Path: {}".format(count,path))
