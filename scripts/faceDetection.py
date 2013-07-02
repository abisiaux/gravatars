"""
@summary: Face detection with opencv using Haar detectors
@author: Alexandre Bisiaux
"""

import cv2

"""
@summary: Face detection with opencv using Haar detectors
"""
class FaceDetector():
    def __init__(self):
        self.front=cv2.cv.Load('../resources/haarcascade_frontalface_default.xml')
        self.profile=cv2.cv.Load('../resources/haarcascade_profileface.xml')
    
    """
    Detect front face
    @param img: Picture
    @return: True if a front face is detected, False otherwise
    """
    def isFrontFace(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.cv.HaarDetectObjects(cv2.cv.fromarray(img), self.front, cv2.cv.CreateMemStorage(), 1.3, 2,cv2.cv.CV_HAAR_DO_CANNY_PRUNING, (10,10))
    
    """
    Detect profile face
    @param img: Picture
    @return: True if a profile face is detected, False otherwise
    """
    def isProfileFace(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.cv.HaarDetectObjects(cv2.cv.fromarray(img), self.profile, cv2.cv.CreateMemStorage(), 1.3, 2,cv2.cv.CV_HAAR_DO_CANNY_PRUNING, (10,10))