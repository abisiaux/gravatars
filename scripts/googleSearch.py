#===============================================================================
# Upload an image on google reverse search engine
#===============================================================================

import requests

headers = {'Content-Type' : 'application/octet-stream',
           'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}

def searchByUrl(picURL):
    return requests.get('https://www.google.com/searchbyimage?image_url=%s' % picURL, headers=headers, allow_redirects=False)              

def searchByImage(picPath, picName):
    data = {'image_content' : open(picPath, 'rb').read(), 'encoded_image' : {'filename' : picName}}
    return requests.post('https://www.google.com/searchbyimage/upload', data=data, headers=headers, allow_redirects=False)

print searchByUrl('http://gravatar.com/avatar/a007be5a61f6aa8f3e85ae2fc18dd66e').headers.get('Location')
print searchByImage('../resources/pictures/0.jpg', '0.jpg').headers.get('Location')