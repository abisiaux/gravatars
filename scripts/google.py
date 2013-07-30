"""
@summary: Some tools to do research on Google images and Google search engine
@author: Alexandre Bisiaux
"""
import requests, re, urllib2 
#, nltk.chunk
from htmlParser import MyParser, get_text_recursive
#from wikipedia import Wikipedia
from htmlentitydefs import name2codepoint


headersDic = {'Content-Type' : 'application/octet-stream',
           'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'} # Headers

"""
Filter the description given by Google
@param sentence: Sentence to filter
@return: A set of revelants words 
"""
def filterDescription(sentence):
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    chunked = nltk.chunk.ne_chunk(tagged)
    #print chunked
    def extract(t):
        names = []
        if hasattr(t, 'node') and t.node:
            if t.node == 'PERSON' or t.node == "GPE" or t.node == "ORGANIZATION":
                names.append(' '.join([child[0] for child in t]))
            else:   
                for child in t:
                    names.extend(extract(child))
        return names
    def tokenize(list):
        l = []
        for w in list:
            tokens = re.findall(r'\w+', w,flags = re.UNICODE | re.LOCALE)
            l.extend(tokens)
        return l
    names = []
    for tree in chunked:
        names.extend(extract(tree))
    return set(tokenize(names))

"""
Check if an url comes from Google or not
@param url: url to check
@return: True if the url comes from Google, False otherwise
"""
def isGoogleURL(url):
    if url == "#" or re.search("^/", url) or re.search(".*google.com.*", url) or re.search(".*http://webcache.*", url) or re.search("javascript.*", url):
        return False
    return True

"""
Escape html characters
@param str: String
@return: The string without html characters
"""
def html_unescape(str):
    def entity_replacer(m):
        entity = m.group(1)
        if entity in name2codepoint:
            return unichr(name2codepoint[entity])
        else:
            return m.group(0)

    def ascii_replacer(m):
        cp = int(m.group(1))
        if cp <= 255:
            return unichr(cp)
        else:
            return m.group(0)
        
    s = re.sub(r'&#(\d+);',  ascii_replacer, str, re.U)
    return re.sub(r'&([^;]+);', entity_replacer, s, re.U)

"""
@summary: Search by image on Google images
"""
class GoogleImage():
    
    """
    Do the search, parse the result page and store it in a tree
    @param picUrl: Url to the picture
    """
    def __init__(self, picUrl):
        # Get location of results page
        url = requests.get('https://www.google.com/searchbyimage?image_url=%s' % picUrl, headers=headersDic, allow_redirects=False).headers.get("Location")          
        # Get content of results page
        response = requests.get(url, headers=headersDic, allow_redirects=False)
        # Parse the html page and build an xml tree
        encoding = response.encoding
        response = (response.content).decode(encoding)
        parser = MyParser()
        parser.feed(response)
        self.tree = parser.close()
    
    """
    Get the best guess
    @return : The best guess if exists, None otherwise
    """
    def getBestGuess(self):
        try:
            bg = ((self.tree.find(".//div[@id='topstuff']").find(".//div")).find(".//div/a")).text
            return bg
        except:
            return None
    """
    Get the dictionary {name : link} of the result page
    @return : The dictionary {name : link}
    """
    def getLinks(self):
        links = {} # Dictionary of links { name : url }
        for link in self.tree.find(".//div[@id='ires']").findall(".//a[@href]"):
            url = link.get('href')
            if self.isGoogleURL(url):                
                links[self.get_text_recursive(link)] = url
        return links
    
"""
@summary: Search on Google
"""
class GoogleSearch():
    """
    @summary: Represent a search result e.g. (titre, url, description)
    """
    class SearchResult():
        def __init__(self, title, url, desc):
            self.title = title
            self.url = url
            self.desc = desc
    """
    Do the search for a specific query, parse the result page, store it in a tree and extract the results
    @param query: The words to search
    """     
    def __init__(self, query):
        # Get the results of the 1st page
        url = "http://www.google.com/search?hl=en&q=%s&btnG=Google+Search" % urllib2.quote(query)
        response = requests.get(url, headers=headersDic, allow_redirects=False)
        # Parse the html page and build an xml tree
        encoding = response.encoding
        response = (response.content).decode(encoding)
        parser = MyParser()
        parser.feed(response)
        self.tree = parser.close()
        self.results = self.extract_results()
    
    """
    Extract the results present in the tree in the form of a list of GoogleSearch objects
    @return: The list of GoogleSearch objects
    """  
    def extract_results(self):
        ret_res = []
        for res in self.tree.findall(".//li[@class='g']"):
            eres = self.extract_result(res)
            if eres:
                ret_res.append(eres)
        return ret_res
    
    """
    Extract the description
    @param result: One result of the results page
    @return: The description if exists, None otherwise
    """
    def extract_desc(self, result):
        _desc = result.find(".//span[@class='st']")
        if _desc:
            return html_unescape(get_text_recursive(_desc))
        else:
            return None
    
    """
    Extract the title and the url
    @param result: One result of the results page
    @return: The couple title, url if exist, None otherwise
    """
    def extract_title_url(self, result):
        _title = result.find(".//a")
        if _title:
            title = get_text_recursive(_title)
            title = html_unescape(title)
            url = _title.get("href")
            match = re.match(r'/url\?q=(http[^&]+)&', url)
            if match:
                url = urllib2.unquote(match.group(1))
            return title, url
        else:
            return None, None
    
    """
    Extract the content of one result
    @param result: The result where extract content
    @return: A new GoogleSearch object
    """
    def extract_result(self, result):
        title, url = self.extract_title_url(result)
        desc = self.extract_desc(result)
        if not title or not url or not desc:
            return None
        else:
            return self.SearchResult(title, url, desc)
    """
    Get the wikipedia title page if exists
    @return: The title of the wikipedia page if exists, None otherwise
    """         
    def getWikipediaTitlePage(self):
        for r in self.results:
            match = re.search('(?<=http://en.wikipedia.org/wiki/)\w+', r.url)
            if match:
                return r.url.split("http://en.wikipedia.org/wiki/")[1]
        return None
    
    """
    Get description of famous people on Google
    @return: Details and biography of the person
    """
    def getDescription(self):
        desc = self.tree.find(".//div[@class='kno-ec rhsvw vk_rhsc']")
        if desc:
            details = []
            bio = ""
            _details = desc.find(".//div[@class='kno-ecr-ts']")
            if _details:
                for n in _details.findall(".//div"):
                    details.append(get_text_recursive(n).encode("utf8"))
            _bio = desc.find(".//div[@class='kno-fb-ctx kno-desc']")
            if _bio:
                bio = get_text_recursive(_bio).encode("utf8")
            return details, bio
        else:
            return None, None