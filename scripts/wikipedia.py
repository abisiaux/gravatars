import re, htmlParser
import networkx as nx
import matplotlib.pyplot as plt # Only for display the graph

"""
Normalize a string for wikipedia search
@param str: String to normalize
@return: The normalized string
"""
def normalize(s):
    return s.replace(" ", "_")

class Category():
    
    def __init__(self, name):
        self.name = name
    
    """
    Get the categories of the page
    @return: The list of page categories
    """    
    def getCategories(self):
        url = "http://en.wikipedia.org/w/api.php/?action=query&titles=%s&prop=categories&clshow=!hidden&format=xml" % normalize(self.name)
        tree = htmlParser.parse(url)
        
        categories = []
        cats = tree.find(".//categories")
        if cats:
            for cat in cats.findall(".//cl"):
                title = cat.get("title")
                if self.relevantCategory(title):
                    categories.append(Category(title.encode('utf8')))
        return categories
    
    """
    String representation of a category
    @return: The string representation
    """
    def __str__(self):
        return self.name.replace("Category:","")
    
    """
    String representation of a category
    @return: The string representation
    """
    def __repr__(self):
        return self.__str__()
    
    """
    Get category information
    @param cat: Category name
    @return Category id, number of pages, number of subcats
    """
    def getInfo(self):
        url = "http://en.wikipedia.org/w/api.php/?action=query&titles=%s&prop=categoryinfo" % self.name
        tree = htmlParser.parse(url)
        
        _pageId = tree.find(".//page")
        _catInfo = tree.find(".//categoryinfo")
        if _pageId and _catInfo:
            pageId = _pageId.get("pageid")
            pages = _catInfo.get("pages")
            subcats = _catInfo.get("subcats")
            return {"pageId":pageId, "pages":pages, "subcats":subcats}
        else:
            return {}
        
    """
    Check if a category is relevant
    @param catName: Name of the category to check
    @return: True if it is relevant, False otherwise
    """
    def relevantCategory(self, catName):
        unrelevant = ["stubs", "categories", "wikipedia", "articles", "disambiguation", "contents", "^categories_by*", "parent_categories", "stub_categories"]
        for w in unrelevant:
            if re.search(w,catName.lower()):
                return False
        return True

        
"""
@summary: Tool to do research on Wikipedia
"""
class Wikipedia():
    
    """
    Search a specific page on Wikipedia
    @param searc: The title of the searched page
    """
    def __init__(self, pageName):
        self.root = Category(pageName)
    
    """
    Get the category graph until a specific depth
    @param depth: Depth of the graph
    @return: The category graph
    """
    def categoryGraph(self, depth):
        self.G = nx.DiGraph()
        pages =[self.root]
        for i in range(depth):
            allCategories = []
            for p in pages:
                categories = p.getCategories()
                self.G.add_node(p, {"depth" : i})
                for c in categories:
                    self.G.add_node(c, {"depth" : i+1})
                    self.G.add_edge(p,c)
                allCategories += categories
            pages = allCategories
        return self.G
    
    """
    Sort the nodes of a graph by degree
    @return: The list of nodes sorted by degree
    """ 
    def sortGraphByDegree(self):
        nodes = sorted(nx.degree(self.G))
        nodes.remove(self.root)
        return nodes
        
            