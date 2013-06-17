#===============================================================================
# Download gravatar SO user's pictures and grab information about them on google images
# Alexandre Bisiaux
# 05-13
#===============================================================================
from searchEngine import SearchEngine
from downloader import Downloader # Downloader module (for the mailing list archive files)
from Queue import Queue # Multi-threading support for Downloader
from unicodeMagic import UnicodeReader, UnicodeWriter
from faceDetection import FaceDetector
import time, os, sys, csv, cv2
from pictureUtils import PictureUtils

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg
        
def main():
    
    data = "../resources/SOusers-Mar13.csv"
    results = "../resources/SOusers-googleSearch.csv"
    picPath = "../resources/SOpictures/"
    
    fr = open(os.path.join(data), 'rb')
    fw = open(os.path.join(results), 'w')
              
    reader = UnicodeReader(fr)
    writer = csv.writer(fw)
    
    # Set up job queue and search
    queue = Queue()
    threads = []
    searchEngine = SearchEngine()
    faceDetector = FaceDetector()
    
    # Use multiple threads to download and get information
    for i in xrange(10):
        threads.append(Downloader(queue))
        threads[-1].start()
    
    SOhashes = {} # Dictionary of user's hashes
    idx = 0
    for row in reader:
        if idx < 200: # To not dowload all the pictures
            so_uid = row[0]            
            so_hash = row[2]
            if(not (SOhashes.has_key(so_hash))): # if it is not already downloaded
                SOhashes[so_hash] = so_uid
                url = 'http://www.gravatar.com/avatar/%s' % so_hash
                if(not searchEngine.isDefaultGravatarPic(url)):
                    # Download picture
                    filepath = os.path.join('%s%d.jpg' % (picPath,int(so_uid)))
                    queue.put((url, filepath))
                    # Get information about picture
                    bestGuess, links = searchEngine.searchByImage(url)
                    
                    # Get Average saturation and threshold brightness
                    picUtils = PictureUtils(filepath)
                    avgSat, threBright = picUtils.computeAvgSatThrBrightness(0.2)
                    
                    # Convert dictionary to string
                    #strLinks = ''.join('{}{}'.format(key, val) for key, val in links.items())
                    # Write information in csv file
                    nbOfLink = 0
                    data = [so_uid, bestGuess, avgSat, threBright]
                    if bestGuess == "":
                        for name, url in links.iteritems():
                            if nbOfLink < 2:
                                data.append(name)
                                data.append(url)
                            else:
                                break
                        # Detect face
                        if faceDetector.isFrontFace(picUtils.img):
                            data.append("Front face")
                        if faceDetector.isProfileFace(picUtils.img):
                            data.append("Profile face")
                    print data
                    writer.writerow(data)
        idx += 1
        time.sleep(0.1)
        
    fr.close()
    fw.close()
    
    # If here, download finished. Stop threads
    for i in xrange(10):
        queue.put((None, None))

if __name__ == "__main__":
    sys.exit(main())
    
    


