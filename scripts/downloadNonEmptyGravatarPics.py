import csv							# Read from and write to CSV files
import os							# Path manipulations (e.g., os.path.abspath)
import sys
import urllib.request				# Open URLs

#from folderUtils import *			# Utilities to work with folders
from unicodeMagic import UnicodeReader, UnicodeWriter

from downloader import Downloader	# Downloader module (for the mailing list archive files)

from Queue import Queue				# Multi-threading support for Downloader


def exist(path):
	return (os.path.exists(path))
	

def isDefaultPic(url):
	try:
		response = urllib.request.urlopen("%s?d=404" % (url)) # throw an exception in case of default gravatar picture
		return False
	except Exception:
		return True
		
	
dataPath = os.path.abspath("C:/Users/Alexandre/Git/gravatars/resources/")

fd = open(os.path.join(dataPath, 'SOusers-Mar13.csv'), 'rb')
reader = UnicodeReader(fd)

# Set up downloader

queue = Queue()
threads = []

# Use multiple threads for download

for i in xrange(10):
	threads.append(Downloader(queue))
	threads[-1].start()

fd = open(os.path.join(dataPath, 'SOusers.csv'), 'rb')
reader = UnicodeReader(fd)

SOusers = []
idx = 0

picsPath = os.path.abspath("C:/Users/Alexandre/Git/gravatars/resources/pictures/")

for row in reader:

	# row = [uid, name, hash, rep]
	if idx >= 0 and idx < 100: # normally not needed. I downloaded some things previously so I skip them now
		so_uid = row[0]			
		so_hash = row[2]
		if(not exist('%s%d.jpg' % (picsPath,int(so_uid)))):
			url = 'http://www.gravatar.com/avatar/%s' % so_hash
			if(not isDefault(url)):
				prefix = os.path.join(picsPath, 'so_pics')
				filepath = os.path.join(prefix, '%d.jpg' % int(so_uid))
				queue.put((url, filepath))
	idx += 1

# If here, download finished. Stop threads
for i in xrange(10):
	queue.put((None, None))

	

