import os
import sys
import urllib.request

def isDefaultPic(url):
	try:
		response = urllib.request.urlopen("%s?d=404" % (url)) # throw an exception in case of default gravatar picture
		return False
	except Exception:
		return True

print(isDefaultPic("http://gravatar.com/avatar/a007be5a61f6aa8f3e85ae2fc18dd66e"))

os.system("pause")
