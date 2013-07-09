"""
@summary: Tool to do research on Wikipedia
@author: Alexandre Bisiaux
"""

import requests, re
from htmlParser import MyParser
import networkx as nx
from matplotlib import pyplot as plt

"""
@summary: Tool to do research on Wikipedia
"""
class Wikipedia():
    
    """
    Search a specific page on Wikipedia, parse the page and store content in a tree
    @param searc: The title of the searched page
    """
    def __init__(self, search):
        self.headers = {'Content-Type' : 'application/octet-stream',
           'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
        #url = "http://en.wikipedia.org/w/api.php?action=parse&page=%s&format=xml" % search
        url = "http://en.wikipedia.org/wiki/%s" % search
        response = requests.get(url, headers=self.headers, allow_redirects=True)
        parser = MyParser()
        encoding = response.encoding
        response = (response.content).decode(encoding)
        parser.feed(response)
        self.tree = parser.close()

    """
    Check if a category is relevant
    @param catName: Name of the category to check
    @return: True if it is relevant, False otherwise
    """
    def relevantCategory(self, catName):
        unrelevant = ["wikipedia", "articles", "disambiguation", "contents", "^categories_by*", "parent_categories", "stub_categories"]
        for w in unrelevant:
            if re.search(w,catName.lower()):
                return False
        return True
    
    """
    Construct the graph of categories
    @param depth: The depth of the graph
    @return: The graph of categories
    """
    def getCategoryGraph(self):
        graph = nx.Graph()
        categories = self.getCategories()
        parents = []
        for c in categories:
            graph.add_node(c)
            for p in self.getMostRelevantParents(c):
                graph.add_edge(p, c)
                if not graph.has_node(p):
                    parents.append(p)
        categories = parents
        return graph 
    
    """
    Get the parents categories of a category
    @param catName: The name of the category
    @return: The list of its parents
    """
    def getParentsCategories(self, catName):
        wiki = Wikipedia("Category:%s" % catName)
        parents = wiki.getCategories()
        return parents
    
    """
    Get the most relevants parents
    @param catName: The name of the category
    @return: The list of its most relevants parents
    """
    def getMostRelevantParents(self, catName):
        wiki = Wikipedia("Category:%s" % catName)
        toReturn = []
        parents = wiki.getCategories()
        for p in parents:
            if len(toReturn) > 12:
                break
            if "by" in p:
                toReturn += self.getMostRelevantParents(p)
            else:
                toReturn.append(p)
        return toReturn
                
    
    """
    Get the categories present at the end of the page
    @return: A list of the categories
    """
    def getCategories(self):
        categories = []
        cats = self.tree.find(".//div[@id='mw-normal-catlinks']")
        if cats:
            for cat in cats.findall(".//li"):
                cat = cat.find(".//a")
                url = cat.get("href")
                match = re.search('(?<=/wiki/Category:)\w+', url)
                if match:
                    catName = match.group(0)
                    if self.relevantCategory(catName):
                        categories.append(catName.encode('utf8'))
        return categories
    
"""
Sort the nodes of a graph by degree
@param G: A graph
@return: The list of nodes sorted by degree
""" 
def sortGraphByDegree(G):
    nodes = sorted(G.degree(), key=G.degree().get)
    nodes.reverse()
    return nodes

#===============================================================================
# wiki = Wikipedia("Stack_Overflow")
# G = wiki.getCategoryGraph()
# print G.nodes()
# nx.draw(G)
# plt.show()
#===============================================================================
