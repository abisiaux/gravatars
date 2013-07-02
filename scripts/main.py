"""
Main Program
Download gravatar SO user's pictures
Grab information about them on google and wikipedia
Compute some visual features
Store these information in a csv file
@author: Alexandre Bisiaux
"""
from google import GoogleSearch, GoogleImage, html_unescape
from wikipedia import Wikipedia, sortGraphByDegree
from downloader import Downloader # Downloader module (for the mailing list archive files)
from Queue import Queue # Multi-threading support for Downloader
from unicodeMagic import UnicodeReader, UnicodeWriter
from faceDetection import FaceDetector
import pictureUtils as picUtils
import time, os, sys, urllib2        
    
"""
Check if a so_hash correspond to a default gravatar picture
@param so_hash: Mail hash of the SO user
@return: True if it links to the default gravatar picture, False otherwise
"""
def isDefaultGravatarPic(so_hash):
    url = 'http://www.gravatar.com/avatar/%s' % so_hash
    try:
        urllib2.urlopen("%s?d=404" % (url)) # throw an exception in case of default gravatar picture
        return False
    except Exception:
        return True

"""
Main Program
"""
def main():
    
    data = "../resources/SOusers-Mar13.csv" # File containing SO user dump
    results = "../resources/features.csv" # File where features will be stored
    picPath = "../resources/SOpictures/" # Directory where pictures will be downloaded
    
    fr = open(os.path.join(data), 'rb')
    fw = open(os.path.join(results), 'a+b')
              
    reader = UnicodeReader(fr)
    writer = UnicodeWriter(fw)
    
    queue = Queue()
    faceDetector = FaceDetector()
    
    threads = []
    SOhashes = {} # Dictionary of user's hashes
    idx = 1
        
    # Use multiple threads to download and get information
    #===========================================================================
    # for i in xrange(10):
    #     threads.append(Downloader(queue))
    #     threads[-1].start()
    #===========================================================================
    
    nbDefault = 0
    cpt = 0
    for row in reader:
        if cpt >= 4443 and cpt < 4444:
            time.sleep(0.05)
            if idx < 4500: # To not download all the pictures
                so_uid = row[0]            
                so_hash = row[2]
                if(not (SOhashes.has_key(so_hash))): # if it is not already downloaded
                    SOhashes[so_hash] = so_uid
                    if(not isDefaultGravatarPic(so_hash)):
                        # Download picture
                        filepath = os.path.join('%s%d.jpg' % (picPath,int(so_uid)))
                        #if not os.path.isfile(filepath):
                            #queue.put(('http://www.gravatar.com/avatar/%s' % so_hash, filepath))
                        data = [so_uid]
                         
                        #===========================================================
                        # Visual information
                        #===========================================================
                         
                        # Load picture
                        pic = picUtils.loadPicture(filepath)
                         
                        # Detect face
                        if faceDetector.isFrontFace(pic) or faceDetector.isProfileFace(pic):
                            data.append("True")
                        else:
                            data.append("False")
                         
                        # 2 most common colors
                        c1, f1, c2, f2 = picUtils.mostCommonColor(pic)
                        data.append(str(c1))
                        data.append(str(c2))
                        data.append(str(f1))
                        data.append(str(f2))
                         
                        # Number of circles
                        data.append(str(picUtils.detectCircle(pic)))
                         
                        # Number of colors
                        data.append(str(picUtils.getNbOfColors(pic)))
                         
                        # Farthest neighbor score with d1 metric
                        data.append(str(picUtils.farthestNeighborMetric(pic, 5, 1)))
                         
                        # Nearest neighbor score with d1 metric
                        data.append(str(picUtils.nearestNeighborMetric(pic, 5, 1)))
                         
                        #===========================================================
                        # # Farthest neighbor score with d2 metric
                        # data.append(str(picUtils.farthestNeighborMetric(pic, 5, 2)))
                        # 
                        # # Nearest neighbor score with d2 metric
                        # data.append(str(picUtils.nearestNeighborMetric(pic, 5, 2)))
                        # 
                        # # Farthest neighbor score with d3 metric
                        # data.append(str(picUtils.farthestNeighborMetric(pic, 5, 3)))
                        # 
                        # # Nearest neighbor score with d3 metric
                        # data.append(str(picUtils.nearestNeighborMetric(pic, 5, 3)))
                        # 
                        # # Farthest neighbor score with d4 metric
                        # data.append(str(picUtils.farthestNeighborMetric(pic, 5, 4)))
                        # 
                        # # Nearest neighbor score with d4 metric
                        # data.append(str(picUtils.nearestNeighborMetric(pic, 5, 4)))
                        #===========================================================
                         
                        # Average saturation and threshold brightness
                        #=======================================================
                        avgSat, threBright = picUtils.computeAvgSatThrBrightness(pic, 0.4)
                        data.append(str(avgSat))
                        data.append(str(threBright))
                        _, threBright = picUtils.computeAvgSatThrBrightness(pic, 0.2)
                        data.append(str(threBright))
                        #=======================================================
                         
                        # Information about picture on google and wikipedia
                        gi = GoogleImage('http://www.gravatar.com/avatar/%s' % so_hash)
                        bestGuess = gi.getBestGuess()
                        if bestGuess:
                            bestGuess = bestGuess.encode('utf8')
                            data.append(bestGuess)
                            gs = GoogleSearch(bestGuess)
                            wikiTitlePage = gs.getWikipediaTitlePage()
                            details, _ = gs.getDescription()
                            if details:
                                for d in details:
                                    data.append(d)
                            if wikiTitlePage:
                                print wikiTitlePage
                                G = Wikipedia(wikiTitlePage).getCategoryGraph()
                                G = sortGraphByDegree(G)
                                for cat in G:
                                    data.append(cat)
                        # Check with NER
                         
                         
                        # Convert dictionary to string
                        #strLinks = ''.join('{}{}'.format(key, val) for key, val in links.items())
                        # Write information in csv file
                        #data.append(avgSat)
                        #data.append(threBright)
                     
                         
     
                        # Write all information collected in the csv file
                        try:
                            idx += 1
                            print so_uid
                            print data
                            writer.writerow(data)
                        except:
                            print "Error with data"
                    else:
                        nbDefault += 1
            else:
                break
        cpt+=1
        
    
    print nbDefault
    fr.close()
    fw.close()
    
    # If here, download finished. Stop threads
    #for i in xrange(10):
        #queue.put((None, None))

if __name__ == "__main__":
    t = time.time()
    sys.exit(main())
    elapsed = time.time() - t
    print "Time elapsed = %s" % elapsed
    
    


