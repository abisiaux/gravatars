#===============================================================================
# Search engine : grab information on the internet about images,...
#===============================================================================

import requests, urllib2, re
from HTMLParser import HTMLParser
from xml.etree import cElementTree as etree
    
class SearchEngine():
    
    class MyParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.links = []
            self.bestGuess = ""
            self.tb = etree.TreeBuilder()
            
        def handle_data(self, data):
            self.tb.data(data)
           
        def handle_starttag(self, tag, attrs):
            self.tb.start(tag, dict(attrs))
            
        def handle_endtag(self, tag):
            self.tb.end(tag)
            
        def close(self):
            HTMLParser.close(self)
            return self.tb.close()
        
    def __init__(self):
        self.headers = {'Content-Type' : 'application/octet-stream',
           'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}

    def searchByImage(self,picURL):
        # Get location of results page
        url = requests.get('https://www.google.com/searchbyimage?image_url=%s' % picURL, headers=self.headers, allow_redirects=False).headers.get("Location")          
        # Get content of results page
        response = requests.get(url, headers=self.headers, allow_redirects=False).content
        # Parse the html page and build an xml tree
        parser = self.MyParser()
        parser.feed(response)
        self.tree = parser.close()
        # Get the best guess
        try:
            bestGuess = ((self.tree.find(".//div[@id='topstuff']").find(".//div")).find(".//div/a")).text
            if(bestGuess == None):
                bestGuess = ""
        except:
            bestGuess = ""
        # Get links with their title
        links = {}
        for link in self.tree.find(".//div[@id='ires']").findall(".//a[@href]"):
            url = link.get('href')
            if self.isGoogleURL(url):                
                links[self.get_text_recursive(link)] = url
        
        return bestGuess, links
            
    def isGoogleURL(self, url):
            if url == "#" or re.search("^/", url) or re.search(".*google.com.*", url) or re.search(".*http://webcache.*", url) or re.search("javascript.*", url):
                return False
            return True
        
    def get_text_recursive(self, node):
        return (node.text or '') + ''.join(map(self.get_text_recursive, node)) + (node.tail or '')
    
    def isDefaultGravatarPic(self, url):
        try:
            urllib2.urlopen("%s?d=404" % (url)) # throw an exception in case of default gravatar picture
            return False
        except Exception:
            return True
