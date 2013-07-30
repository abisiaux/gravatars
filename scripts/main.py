"""
Main Program
Download gravatar SO user's pictures
Grab information about them on google and wikipedia
Compute some visual features
Store these information in a csv file
@author: Alexandre Bisiaux
"""
from google import GoogleSearch, GoogleImage, html_unescape
from wikipedia import Wikipedia
from downloader import Downloader # Downloader module (for the mailing list archive files)
from Queue import Queue # Multi-threading support for Downloader
from unicodeMagic import UnicodeReader, UnicodeWriter
from randomReader import RandomReader
from faceDetection import FaceDetector
import pictureUtils as picUtils
import time, os, sys


"""
Features
"""
_VISUAL_FEATURES = True
_FACE = True
_MOST_COMMON_COLORS = True
_CIRCLES = True
_NBCOLORS = True
_FARTHEST_NEIGHBOR = True
_NEAREST_NEIGHBOR = True
_AVERAGE_SATURATION = True
_THRESHOLD_BRIGHTNESS = True
_GOOGLE = False
_WIKIPEDIA = False


"""
Main Program
"""
def main():
    
    data = "../resources/SOusers-Mar13.csv" # File containing SO user dump
    results = "../resources/features.csv" # File where features will be stored
    picPath = "../resources/SOpictures/" # Directory where pictures will be downloaded
    
    fr = open(os.path.join(data), 'rb')
    fw = open(os.path.join(results), 'wb')
              
    reader = RandomReader(fr)
    writer = UnicodeWriter(fw)
    
    queue = Queue()
    if _FACE:
        faceDetector = FaceDetector()
    
    threads = []
    SOhashes = {} # Dictionary of user's hashes
        
    # Use multiple threads to download and get information
    for i in xrange(10):
        threads.append(Downloader(queue))
        threads[-1].start()
    idx = 0
    
    for row in reader:
        if idx < 10000:
            so_uid = row[0]            
            so_hash = row[1]
            if(not (SOhashes.has_key(so_hash))):
                SOhashes[so_hash] = so_uid
                if(not picUtils.isDefaultGravatarPic(so_hash)):
                    data = [so_uid]
                    if _VISUAL_FEATURES:
                        # Download picture
                        filepath = os.path.join('%s%d.jpg' % (picPath,int(so_uid)))
                        if not os.path.isfile(filepath):
                            queue.put(('http://www.gravatar.com/avatar/%s' % so_hash, filepath))
                            time.sleep(2)
                        # Load picture
                        pic = picUtils.loadPicture(filepath)
                    
                        if _FACE:
                            if faceDetector.isFrontFace(pic) or faceDetector.isProfileFace(pic):
                                data.append(str(True))
                            else:
                                data.append(str(False))
                        
                        if _MOST_COMMON_COLORS:
                            c1, f1, c2, f2 = picUtils.mostCommonColor(pic)
                            #data.append(str(c1))
                            #data.append(str(c2))
                            data.append(str(f1))
                            data.append(str(f2))
                            
                        if _CIRCLES:
                            data.append(str(picUtils.detectCircle(pic)))
                            
                        if _NBCOLORS:
                            data.append(str(picUtils.getNbOfColors(pic)))
                            
                        if _FARTHEST_NEIGHBOR:
                            data.append(str(picUtils.farthestNeighborMetric(pic, 5, 1)))
                            
                        if _NEAREST_NEIGHBOR:
                            data.append(str(picUtils.nearestNeighborMetric(pic, 5, 1)))
                        
                        if _AVERAGE_SATURATION:
                            data.append(str(picUtils.avgSaturation(pic)))
                        
                        if _THRESHOLD_BRIGHTNESS:
                            data.append(str(picUtils.threBrightness(pic, 0.4)))
                            data.append(str(picUtils.threBrightness(pic, 0.2)))
                        
                    if _GOOGLE:
                        gi = GoogleImage('http://www.gravatar.com/avatar/%s' % so_hash)
                        bestGuess = gi.getBestGuess()
                        if bestGuess:
                            bestGuess = bestGuess.encode('utf8')
                            data.append(bestGuess)
                            if _WIKIPEDIA:
                                gs = GoogleSearch("%s site:en.wikipedia.org" % bestGuess)
                                wikiTitlePage = gs.getWikipediaTitlePage()
                                if wikiTitlePage:
                                    wiki = Wikipedia(wikiTitlePage)
                                    wiki.categoryGraph(2)
                                    nbCats = 5
                                    i = 0
                                    cats = wiki.sortGraphByDegree()
                                    while i<nbCats and i < len(cats):
                                        data.append(str(cats[i]))
                                        i += 1
                   
                    
                    # Write all information collected in the csv file
                    try:
                        idx += 1
                        print data
                        writer.writerow(data)
                    except:
                        print "Error with data"
                    time.sleep(0.05)
        else:
            break
    fr.close()
    fw.close()
    
    # If here, download finished. Stop threads
    for i in xrange(10):
        queue.put((None, None))

if __name__ == "__main__":
    t = time.time()
    sys.exit(main())
    elapsed = time.time() - t
    print "Time elapsed = %s" % elapsed
    
    


