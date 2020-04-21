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
        while(len(no_zeroes)!=0):
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
    #Part 2. Perform Dijkstras Algorithm to find the least amount of time required based on distance using adjaceny matrix
    #This solution uses an adjaceny matrix
    ap_matrix = Matrix(data)
    ap_matrix.add_edges()
    duration, path = ap_matrix.dijkstras('ACY','BOS')
    print("Dijkstras:\nFlight Duration: {}\nFlight Path: {}".format(duration, path))