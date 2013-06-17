import cv2
import numpy as np

class PictureUtils():
    def __init__(self, path):
        self.img = cv2.imread(path)
        
    def colorHistogram(self, picture):
        h = np.zeros((300,256,3))
        bins = np.arange(256).reshape(256,1)
        color = [ (255,0,0),(0,255,0),(0,0,255) ]
        
        for ch, col in enumerate(color):
            hist_item = cv2.calcHist([self.img],[ch],None,[256],[0,255])
            cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
            hist=np.int32(np.around(hist_item))
            pts = np.column_stack((bins,hist))
            cv2.polylines(h,[pts],False,col)
            
        h=np.flipud(h)
        return h

    #===========================================================================
    # Get the average saturation and the percentage of pixel
    # having brigthness above a certain threshold
    #===========================================================================
    def computeAvgSatThrBrightness(self, thresholdBright):
        im = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        hue, sat, val = cv2.split(im)
        size = np.size(val)
        VcountTr = 0
        val = val/float(255)
        # Go over each pixel's brightness value
        for l in val:
            for p in l:
                if p >= thresholdBright:
                    VcountTr += 1
        percentBr = VcountTr / float(size)
        avgSat = np.mean(sat)
        return percentBr, avgSat
    
    #===========================================================================
    # Quantify a picture with only k colors
    #===========================================================================
    def colorQuantization(self, k):
        z = self.img.reshape((-1,3))
        
        # convert to np.float32
        z = np.float32(z)
        
        # define criteria, number of clusters and apply kmeans
        crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        ret, label, center = cv2.kmeans(z, k, crit, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        # Now convert back into uint8, and make original image
        center = np.uint8(center)
        res = center[label.flatten()]
        res2 = res.reshape((self.img.shape))
        return res2
    
    #===========================================================================
    # Compute the histogram of values
    #===========================================================================
    def hist_lines(self, values):
        h = np.zeros((300,256,3))
        hist_item = cv2.calcHist([values],[0],None,[256],[0,256])
        cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
        hist=np.int32(np.around(hist_item))
        for x,y in enumerate(hist):
            cv2.line(h,(x,0),(x,y),(255,255,255))
        y = np.flipud(h)
        return y
        
    def edgeDetector(self):
        imgg = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        h = cv2.Sobel(imgg, -1, 1, 0)
        v = cv2.Sobel(imgg, -1, 0, 1)
        print h
        return h,v
picUtils = PictureUtils("../resources/cartoon2.jpg")
#picUtils = PictureUtils("../resources/SOpictures/194.jpg")
print picUtils.computeAvgSatThrBrightness(0.2)
img = cv2.cvtColor(picUtils.img, cv2.COLOR_BGR2HSV)
hue, sat, val = cv2.split(img)
hist = picUtils.hist_lines(sat)
#pic = picUtils.colorQuantization(3)
h, v = picUtils.edgeDetector()
cv2.imshow("h", h + v)
cv2.imshow("v", v)
cv2.waitKey(0)
cv2.destroyAllWindows()