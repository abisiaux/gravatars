## Upload an image on google reverse search engine

import mimetypes
from cStringIO import StringIO
import urllib
import urllib2

from MultiPartForm import MultiPartForm

def upload(picPath):
    # Create the form
    form = MultiPartForm()
    
    # Add the image and required fields
    mimeType = mimetypes.guess_type(picPath)[0]
    form.add_file('encoded_image', picPath, StringIO(''), mimeType)
    form.add_field('image_content', '')

    # Build the request
    request = urllib2.Request('http://www.google.fr/searchbyimage/upload')
    body = str(form)
    request.add_header('Content-type', '%s;boundary=----WebKitFormBoundaryB6DC4larUvuT5gBS' % (form.get_content_type()))
    request.add_header('Content-length', len(body))
    request.add_header('User-Agent', 'User-Agent: Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36')
    request.add_data(body)

    print
    print 'REQUEST:'
    print request.get_data()

    print
    print 'SERVER RESPONSE:'
    #print urllib2.urlopen(request).read()
    print urllib2.urlopen(request).info()
	
upload("661.jpg")

# Trying with GET request and url from gravatar

# print urllib2.urlopen('http://www.google.com/searchbyimage?image_url=http%3A%2F%2Fgravatar.com%2Favatar%2Fa007be5a61f6aa8f3e85ae2fc18dd66e&image_content=').info()
