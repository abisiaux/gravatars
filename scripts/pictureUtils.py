"""
@summary: Some tools to analyze images and collect some visual features
@author: Alexandre Bisiaux
"""

import cv2, urllib2
import numpy as np

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
Load a picture using OpenCv
@param path: Path to the picture
@return: The picture loaded
"""
def loadPicture(path):
    return cv2.imread(path)

"""
Convert a image in bgr space into grey scale
@param img : Image to convert
@return: The image in grey scale
"""
def bgrToGray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

"""
Compute the color histogram of a picture
@param img: Image
@return: The color histogram
"""
def colorHistogram(img):
    h = np.zeros((300,256,3))
    bins = np.arange(256).reshape(256,1)
    color = [ (255,0,0),(0,255,0),(0,0,255) ]
    
    for ch, col in enumerate(color):
        hist_item = cv2.calcHist([img],[ch],None,[256],[0,255])
        cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
        hist=np.int32(np.around(hist_item))
        pts = np.column_stack((bins,hist))
        cv2.polylines(h,[pts],False,col)
        
    h=np.flipud(h)
    return h

"""
Get the number of colors in an image
@param img: Image in bgr space
@return:The number of colors
"""
def getNbOfColors(img):
    colorsDic = {}
    h,w,_ = img.shape
    for i in range(0, h):
        for j in range(0, w):
            col = tuple(img[i,j,:])
            if colorsDic.has_key(col):
                colorsDic[col] += 1
            else:
                colorsDic[col] = 1
    return len(colorsDic)
"""
Convert a bgr color in hsv
@param c: Color in bgr to convert
@return: The color in hsv space
""" 
def bgr2hsv(c):
    b = c[0] / float(255)
    g = c[1] / float(255)
    r = c[2] / float(255)
    cmax = max(b,g,r)
    cmin = min(b,g,r)
    delta = cmax - cmin
    
    v = cmax
    
    if cmax != 0:
        s = delta / float(cmax)
    else:
        s = 0
        h = 0
        return (h,s,v)
    
    if cmax == r: h = 60 * (b - g)
    elif cmax == g: h = 60 * (2 + r - b)
    else: h = 60 * (4 + g - r)
    if h > 360: h -= 360
    if h < 0: h += 360
    
    return (h,s,v)

"""
Get the distance between two colors
@param c1, c2: Colors in bgr space
@param d: Distance to calculate
    d1 = |r1-r2| + |g1-g2| + |b1-b2|
    d2 = |h1-h2| + |s1-s2| + |v1-v2|
    d3 = |h1-h2| + |s1-s2|
    d4 = |h1-h2|
@return: The distance between c1 and c2
"""
def colorDist(c1, c2, d):
    s = 0
    if d == 1 or d==2:
        if d == 2:
            c1 = bgr2hsv(c1)
            c2 = bgr2hsv(c2)
        for i in range(len(c1)):
            s += abs(c2[i] - c1[i])
    elif d==3 or d==4:
        c1 = bgr2hsv(c1)
        c2 = bgr2hsv(c2)
        if d==3:
            s += abs(c2[0] - c1[0])
            s += abs(c2[1] - c1[1])
        else:   
            s = abs(c2[0] - c1[0]) 
    return s

"""
Get the average saturation and the percentage of pixel having brigthness above a certain threshold
@param img: Image in bgr space
@param thresholdBriht: Threshold for brightness
@return: The average saturation in img and % of pixel having a brightness >= thresholdBright
"""
def computeAvgSatThrBrightness(img, thresholdBright):
    im = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # convert image to hsv space
    _, sat, val = cv2.split(im)
    size = np.size(val)
    VcountTr = 0
    val = val/float(255)
    # Go over each pixel's brightness value
    for l in val:
        for p in l:
            if p >= thresholdBright:
                VcountTr += 1
    percentBr = (VcountTr / float(size))*100
    avgSat = np.mean(sat)
    return avgSat, percentBr
    
"""
Quantify a picture with only k colors
Use k-means
@param img: Image to quantify
@param k: Number of colors to use
@return: The image with a number of colors reduces to k 
"""
def colorQuantization(img, k):
    z = img.reshape((-1,3))
    # convert to np.float32
    z = np.float32(z)
    # define criteria, number of clusters and apply kmeans
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, label, center = cv2.kmeans(z, k, crit, 10, cv2.KMEANS_RANDOM_CENTERS)
    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((img.shape))
    return res2
    
"""
Compute the histogram of values
@param values: Values
@return: The histogram of these values
"""
def hist_lines(values):
    h = np.zeros((300,256,3))
    hist_item = cv2.calcHist([values],[0],None,[256],[0,256])
    cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
    hist=np.int32(np.around(hist_item))
    for x,y in enumerate(hist):
        cv2.line(h,(x,0),(x,y),(255,255,255))
    y = np.flipud(h)
    return y

"""
Get the 2 most common colors and for each the fraction of pixels which have one these two colors
@param img: Image to analyze
@return: The 2 most common colors and the fraction of pixels for each
"""
def mostCommonColor(img):
    colorsDic = {}
    h,w,_ = img.shape
    for i in range(0, h):
        for j in range(0, w):
            bgr = tuple(img[i,j,:])
            if not colorsDic.has_key(bgr):
                colorsDic[bgr] = 1
            else:
                colorsDic[bgr] += 1
    values = list(colorsDic.values())
    keys = list(colorsDic.keys())
    if keys:
        v1 = max(values)
        c1 = keys[values.index(v1)]
        frac1 = v1 / (float((h*w))) * 100
        values.remove(max(values))
        keys.remove(c1)
        if len(keys) > 0:
            v2 = max(values)
            c2 = keys[values.index(v2)]
            frac2 = v2 / (float((h*w))) * 100
            return c1, frac1, c2, frac2
        else:
            return c1, frac1, None, None
    return None, None, None, None

"""
Detect circle in an image
@param image: Image to analyze
@return: The number of circles present in the picture
"""
def detectCircle(image):
    # Convert it into gray scale
    gray_img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # Apply a gaussian blur to avoid noize
    gray_img = cv2.GaussianBlur(gray_img,(5,5), 2)
    # Apply Hough Circle Transform
    circles = cv2.HoughCircles(gray_img, cv2.cv.CV_HOUGH_GRADIENT, 1.5, 10)
    if circles == None:
        return 0
    else:
        return len(circles)

"""
Detect corners in an image using Harris detector
@param image: Image to analyze
@return: The number of corners in the picture
"""
def detectCorners(image):
    # Convert it into gray scale
    gray_img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # Apply a gaussian blur to avoid noize
    gray_img = cv2.GaussianBlur(gray_img,(5,5), 2)
    # Detect corners
    corners = cv2.cornerHarris(gray_img, 20, 4, 0.04)
    if corners == None: return 0
    else: return len(corners)
    
"""
Get the fraction of pixels where the maximum color distance between it and its neighboor is greater than P
@param img: Image to analyze
@param P: Threshold for distance
@param d: Type of distance to use (d={1,2,3,4}) @see: colorDistance
@return: The fraction of pixels corresponding to this criteria
""" 
def farthestNeighborMetric(img, P, d): # P between 0 and 765
    score = 0
    h,w,d = img.shape
    for i in range(1, h-1): # For each pixel except outer pixels
        for j in range(1, w-1):
            p1 = tuple(img[i,j,:])
            left = tuple(img[i-1,j,:])
            right = tuple(img[i+1,j,:])
            up = tuple(img[i,j-1,:])
            down = tuple(img[i,j+1,:])
            transitionVal = max(colorDist(p1, left, d), colorDist(p1, right, d), colorDist(p1, up, d), colorDist(p1, down, d))
            if transitionVal >= P:
                score += 1
    return score / float(h*w)


"""
Get the fraction of pixels where the maximum color distance between it and its neighboor is lower than P
@param img: Image to analyze
@param P: Threshold for distance
@param d: Type of distance to use (d={1,2,3,4}) @see: colorDistance
@return: The fraction of pixels corresponding to this criteria
""" 
def nearestNeighborMetric(img, P, d): # P between 0 and 765
    score = 0
    h,w,d = img.shape
    for i in range(1, h-1): # For each pixel except outer pixels
        for j in range(1, w-1):
            p1 = tuple(img[i,j,:])
            left = tuple(img[i-1,j,:])
            right = tuple(img[i+1,j,:])
            up = tuple(img[i,j-1,:])
            down = tuple(img[i,j+1,:])
            transitionVal = min(colorDist(p1, left, d), colorDist(p1, right, d), colorDist(p1, up, d), colorDist(p1, down, d))
            if transitionVal >= P:
                score += 1
    return score / float(h*w)