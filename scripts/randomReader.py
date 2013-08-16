"""
@summary: Read a csv file, build a dictionary of lines content and randomize it
@author: Alexandre Bisiaux
"""

from unicodeMagic import UnicodeReader
import random

"""
@summary: Read a csv file, construct a dictionary of lines content and randomize it
"""
class RandomReader:
    """
    Construct a dictionary of contents and randomize its key set
    """
    def __init__(self, f):
        reader = UnicodeReader(f)
        self.content = {}
        i = 0
        for row in reader:
            line = []
            for r in row:
                line.append(r)
            self.content[i] = line
            i += 1

        self.randomKeys = self.content.keys()
        random.shuffle(self.randomKeys)
    
    """
    Iterate over random lines
    @return: self
    """
    def __iter__(self):
        self.iterator = self.randomKeys.__iter__()
        return self
    
    """
    Get the next line according to the randomize key
    @return: A random line
    """
    def next(self):
        k = self.iterator.next()
        return self.content[k]