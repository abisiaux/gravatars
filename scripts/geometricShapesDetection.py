import cv2
import numpy as np
import os

def detectCircle(image):
    # Apply Hough Circle Transform
    circles = cv2.HoughCircles(image, cv2.cv.CV_HOUGH_GRADIENT, 1.5, 10)
    if circles == None:
        return 0
    else:
        return len(circles)

def isGeometricShape(picture):
    # Load the picture
    img = cv2.imread(picture)
    # Convert it in gray scale
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Apply a gaussian blur to avoid noize
    gray_img = cv2.GaussianBlur(gray_img,(5,5), 2)
    if detectCircle(gray_img) > 0:
        print "%s contains circles" % picture
    
    #===========================================================================
    # cv2.imshow('gray image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #===========================================================================

    
for f in os.listdir('../resources/pictures/'):
    isGeometricShape('../resources/pictures/%s' % f)