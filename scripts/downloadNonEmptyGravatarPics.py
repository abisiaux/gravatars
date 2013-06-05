import csv							# Read from and write to CSV files
import os							# Path manipulations (e.g., os.path.abspath)
import sys
import time
import urllib2				# Open URLs

from unicodeMagic import UnicodeReader, UnicodeWriter

from downloader import Downloader	# Downloader module (for the mailing list archive files)

from Queue import Queue				# Multi-threading support for Downloader

def isDefaultPic(url):
	try:
		response = urllib2.urlopen("%s?d=404" % (url)) # throw an exception in case of default gravatar picture
		return False
	except Exception:
		return True
		
	
dataPath = os.path.abspath("C:/Users/Alexandre/Git/gravatars/resources")

# Set up downloader

queue = Queue()
threads = []

# Use multiple threads for download

for i in xrange(10):
	threads.append(Downloader(queue))
	threads[-1].start()

fd = open(os.path.join(dataPath, 'SOusers-Mar13.csv'), 'rb')
reader = UnicodeReader(fd)

idx = 0
SOhashes = {}
picsPath = os.path.abspath("C:/Users/Alexandre/Git/gravatars/resources/pictures/")

for row in reader:

	# row = [uid, name, hash, rep]
	if idx < 500:
		so_uid = row[0]			
		so_hash = row[2]
		if(not (SOhashes.has_key(so_hash)): # if it doesn't be ever downloaded
			SOhashes[so_hash] = so_uid
			url = 'http://www.gravatar.com/avatar/%s' % so_hash
			if(not isDefaultPic(url)):
				filepath = os.path.join(picsPath,'%d.jpg' % int(so_uid))
				queue.put((url, filepath))
			else:
				print("%s is default picture" % (so_uid))
	idx += 1
	time.sleep(0.5)

# If here, download finished. Stop threads
for i in xrange(10):
	queue.put((None, None))
	
os.system("pause")

