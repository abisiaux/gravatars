"""
@summary: Custom HTML parser using HTMLParser library, store the result in a tree
@author: Alexandre Bisiaux
"""

from HTMLParser import HTMLParser
from xml.etree import cElementTree as etree


"""
Get text of a tree node 
@param node: The tree node
@return: The text presents in the node Ex : <a> text </a> => return text
"""
def get_text_recursive(node):
    return (node.text or '') + ' '.join(map(get_text_recursive, node)) + (node.tail or '')

"""
@summary: Custom HTML parser using HTMLParser library, store the result in a tree
"""
class MyParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tb = etree.TreeBuilder()
    
    """
    Store the data between two tags in the tree
    @param img: data
    """
    def handle_data(self, data):
        self.tb.data(data)
    
    """
    Store a start tag with its attributes in the tree
    @param img: data
    """
    def handle_starttag(self, tag, attrs):
        self.tb.start(tag, dict(attrs))
    
    """
    Store a end tag in the tree
    @param img: data
    """
    def handle_endtag(self, tag):
        self.tb.end(tag)
    
    """
    Close the parser and return the tree builded
    @return: The tree
    """
    def close(self):
        HTMLParser.close(self)
        return self.tb.close()