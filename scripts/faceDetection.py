#===============================================================================
# Face detection with opencv using Haar detectors
#===============================================================================

import cv2

class FaceDetector():
    def __init__(self):
        self.front=cv2.cv.Load('../resources/haarcascade_frontalface_default.xml')
        self.profile=cv2.cv.Load('../resources/haarcascade_profileface.xml')
        
    def isFrontFace(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.cv.HaarDetectObjects(cv2.cv.fromarray(img), self.front, cv2.cv.CreateMemStorage(), 1.3, 2,cv2.cv.CV_HAAR_DO_CANNY_PRUNING, (10,10))
    
    def isProfileFace(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.cv.HaarDetectObjects(cv2.cv.fromarray(img), self.profile, cv2.cv.CreateMemStorage(), 1.3, 2,cv2.cv.CV_HAAR_DO_CANNY_PRUNING, (10,10))