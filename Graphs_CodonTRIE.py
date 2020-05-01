#Use Beautiful Soup to grab the DNA signatures
from bs4 import BeautifulSoup
import requests
import textwrap

class Parser:
    def __init__(self):
        self.url = 'https://www2.palomar.edu/users/warmstrong/codons.htm'
        self.req = requests.get(self.url)
        self.soup = BeautifulSoup(self.req.text, 'html.parser')
        self.names = []
        #Call parsing functions
        self.data = self.parse_data()
        self.final_parse()
        self.codon_string = ""
        self.make_string()

    #Function to parse the soup data. Returns a list containing lists of string data.
    def parse_data(self):
        _data = []#throw away
        #First find all the div tags and then find the div tags that contain a bold bracket
        #Remove the html tags from those lines and append the text to a list for further parsing
        for row in self.soup.findAll('div'):
            col = row.findAll('b')
            col = [ ele.text.strip() for ele in col ]
            _data.append(col)
        #Further prep the lines for trie insertion
        data = []
        for line in _data:
            _line = ",".join(line)
            line = _line.split(", ")
            data.append(line)
        #Remove the labels ( i saved them in names array for formatting later)
        skip = 0
        _filtered = []
        for index, line in enumerate(data[4:-1]):
            if index == skip:
                skip+=4
                self.names.append(line)
            else:
                _filtered.append(line)
        return _filtered

    #This function will simultaneously empty the old data list and replace it with only the relevant RNA codons (the center table on the provided link)
    #It functions by breaking the original array in to groups of 3 and popping each element only preserving those we need while preserving the order.
    def final_parse(self):
        for i in range(21):
            for i in range(3):
                _temp = self.data.pop(0)
                if i == 1:
                    self.data.append(_temp)

    #This function will return a string  composed of the final_parsed codons stored in the data array
    # The formatting on the website was sub optimal im sure there is a better way to do this with a single loop 
    def make_string(self):
        _str = ""
        for arr in self.data:
            for ele in arr:
                _str+=ele
        for char in _str:
            if char != ' ':
                self.codon_string+=char

class Node:
    def __init__(self, _char, end=False):
        self.char = _char
        self.children = {}
        self.is_word = end
    
    def add_child(self, _node):
        _key = _node.char
        if _key not in self.children.keys():
            self.children.update({ _key:_node })

class Trie:
    def __init__(self, _str):
        self.nodes = {}
        self.codon_string = _str

    def add_nodes(self):
        #GCU GCC GCA GCG CGU CGC CGA CGG AGA AGG AAU AAC GAU GAC UGU UGC GAA
        triplets = textwrap.wrap(self.codon_string, 3)
        for trio in triplets:
            #If the string is not in the trie already then we add it with its children nodes
            if trio[0] in self.nodes:
                _root = self.nodes.get(trio[0])
                if trio[1] in _root.children:
                    _root = _root.children.get(trio[1])
                    _root.add_child(Node(trio[2],end=True))
            else:
                _node = Node(trio[0])
                _node.add_child(Node(trio[1]))
                _node.add_child(Node(trio[2],end=True))
                self.nodes.update({ trio[0] :_node})


#Create parser object to prep the data for our Trie
parser = Parser()
#Create a Trie object
codon_trie = Trie(parser.codon_string)
codon_trie.add_nodes()

for key, value in codon_trie.nodes.items():
    print(key, value.children)
    for child in value.children.values():
        print(child.children)