import cv2
import numpy as np
import os

def detectCircle(image):
    # Convert it into gray scale
    gray_img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # Apply a gaussian blur to avoid noize
    gray_img = cv2.GaussianBlur(gray_img,(5,5), 2)
    # Apply Hough Circle Transform
    circles = cv2.HoughCircles(gray_img, cv2.cv.CV_HOUGH_GRADIENT, 1.5, 10)
    if circles == None:
        return False
    else:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            cv2.circle(image,(i[0],i[1]),i[2],(0,255,0),1)  # draw the outer circle
        
        cv2.imshow('detected circles',image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return True
    
def isGeometricShape(picture):
    # Load the picture
    img = cv2.imread(picture)
        
    if detectCircle(img):
        print "%s contains circles" % picture
    #===========================================================================
    # cv2.imshow('gray image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #===========================================================================

    
for f in os.listdir('../resources/pictures/'):
    isGeometricShape('../resources/pictures/%s' % f)