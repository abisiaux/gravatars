#===============================================================================
# Upload an image on google reverse search engine
#===============================================================================

import requests
from HTMLParser import HTMLParser
from xml.etree import cElementTree as etree
import re

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
                    
headers = {'Content-Type' : 'application/octet-stream',
           'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}

def searchByUrl(picURL):
    return requests.get('https://www.google.com/searchbyimage?image_url=%s' % picURL, headers=headers, allow_redirects=False)          

def searchByImage(picPath, picName):
    data = {'image_content' : open(picPath, 'rb').read(), 'encoded_image' : {'filename' : picName}}
    return requests.post('https://www.google.com/searchbyimage/upload', data=data, headers=headers, allow_redirects=False)

def getBestGuess(root):
    try:
        bestGuess = ((root.find(".//div[@id='topstuff']").find(".//div")).find(".//div/a")).text
    except:
        bestGuess = None
    return bestGuess

def checkURL(url):
        if url == "#" or re.search("^/", url) or re.search(".*google.com.*", url) or re.search(".*http://webcache.*", url) or re.search("javascript.*", url):
            return False
        return True
        
def getLinks(root):
    links = {}
    for link in root.find(".//div[@id='ires']").findall(".//a[@href]"):
        url = link.get('href')
        name = []
        if checkURL(url):
            if(link.text != None):
                name.append(link.text)
            try:
                for n in link.findall(".//em"):
                    name.append(n.text)
            except:
                name.append(link.text)
                
            links[', '.join(name)] = url
    return links

url = searchByUrl('http://gravatar.com/avatar/42893555ea66c988b51c9167a650d849').headers.get('Location')
#url = searchByUrl('http://gravatar.com/avatar/a007be5a61f6aa8f3e85ae2fc18dd66e').headers.get('Location')
response = requests.get(url, headers=headers, allow_redirects=False).content
parser = MyParser()
parser.feed(response)
root = parser.close()
print "Best guess = %s" % getBestGuess(root)
print getLinks(root)

#print searchByImage('../resources/pictures/0.jpg', '0.jpg').headers.get('Location')