#####################
# Face detection with opencv using Haar detectors
#####################

import cv2
import os
faces = []
for f in os.listdir('../resources/pictures/'):
    img = cv2.cv.LoadImage('../resources/pictures/%s' % f, 0)
    haar=cv2.cv.Load('../resources/haarcascade_frontalface_default.xml')
    detected = cv2.cv.HaarDetectObjects(img, haar, cv2.cv.CreateMemStorage(), 1.2, 2,cv2.cv.CV_HAAR_DO_CANNY_PRUNING, (10,10))
    if detected:
        faces.append(f)
        
# Sort the face by so_uid
print "Faces = %s " % sorted([int(i.split('.',1)[0]) for i in faces])