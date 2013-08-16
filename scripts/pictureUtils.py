"""
@summary: Functions for visual features extraction
@author: Alexandre Bisiaux
"""

import cv2
import numpy as np

"""
Load a picture using OpenCv
@param path: Path to the picture
@return: The picture loaded
"""
def loadPicture(path):
    return cv2.imread(path)

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
Get the distance between two colors
@param c1, c2: Colors in rgb space
@return: The distance between c1 and c2 : d = |r1-r2| + |g1-g2| + |b1-b2|
"""
def colorDist(c1, c2):
    return abs(c2[0] - c1[0]) + abs(c2[1] - c1[1]) + abs(c2[2] - c1[2])

"""
Get the percentage of pixel having brigthness above a certain threshold
@param img: Image in bgr space
@param thresholdBriht: Threshold for brightness
@return: The % of pixel having a brightness greater than a certain threshold
"""
def threBrightness(img, threshold):
    im = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # convert image to hsv space
    _, _, val = cv2.split(im)
    size = np.size(val)
    VcountTr = 0
    val = val/float(255)
    # Go over each pixel's brightness value
    for l in val:
        for p in l:
            if p >= threshold:
                VcountTr += 1
    return VcountTr / float(size)

"""
Compute the average pixel saturation in the image
@param img: Image in bgr space
@return: The average saturation
"""
def avgSaturation(img):
    im = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # convert image to hsv space
    _, sat, _ = cv2.split(im)
    return np.mean(sat)

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
        frac1 = v1 / float((h*w))
        values.remove(max(values))
        keys.remove(c1)
        if len(keys) > 0:
            v2 = max(values)
            c2 = keys[values.index(v2)]
            frac2 = v2 / float((h*w))
            return c1, frac1, c2, frac2
        else:
            return c1, frac1, None, 0
    return None, 0, None, 0
    
"""
Get the fraction of pixels where the maximum color distance between it and its neighboor is greater than P
@param img: Image to analyze
@param P: Threshold for distance
@return: The fraction of pixels corresponding to this criteria
""" 
def farthestNeighborMetric(img, P): # P between 0 and 765
    score = 0
    h,w,_ = img.shape
    for i in range(1, h-1): # For each pixel except outer pixels
        for j in range(1, w-1):
            p1 = tuple(img[i,j,:])
            left = tuple(img[i-1,j,:])
            right = tuple(img[i+1,j,:])
            up = tuple(img[i,j-1,:])
            down = tuple(img[i,j+1,:])
            transitionVal = max(colorDist(p1, left), colorDist(p1, right), colorDist(p1, up), colorDist(p1, down))
            if transitionVal >= P:
                score += 1
    return score / float(h*w)