#Use Beautiful Soup to grab the DNA signatures
from bs4 import BeautifulSoup
import requests

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
    def __init__(self):
        self.char = ''
        self.children = []
        self.isWord = False

class Trie:
    def __init__(self, _str):
        self.nodes = []
        self._str = _str

    def add_nodes(self):
        pass
        #loop over the string and see if the node is known 

#Create parser object to prep the data for our Trie
parser = Parser()
print(parser.codon_string)
