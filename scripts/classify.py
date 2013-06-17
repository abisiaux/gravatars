import cv2, os
import numpy as np

simpsons = ["simpsons", "homer", "marge", "simpson", "bart", "lisa", "maggie"]

def hist_curve(img):
    im = cv2.imread(img)
    im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    bins = np.arange(256).reshape(256,1)
    h = np.zeros((300,256,3))
    if len(im.shape) == 2:
        color = [(255,255,255)]
    elif im.shape[2] == 3:
        color = [ (255,0,0),(0,255,0),(0,0,255) ]
    for ch, col in enumerate(color):
        hist_item = cv2.calcHist([im],[ch],None,[256],[0,256])
        cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
        hist=np.int32(np.around(hist_item))
        pts = np.int32(np.column_stack((bins,hist)))
        cv2.polylines(h,[pts],False,col)
    y=np.flipud(h)
    return y


    
def getNbOfColors(img):
    im = cv2.imread(img)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    colorsDic = {}
    h,w,d = im.shape
    for i in range(0, h):
        for j in range(0, w):
            rgb = tuple(im[i,j,:])
            #print rgb
            if not colorsDic.has_key(rgb):
                colorsDic[rgb] = 1
            else:
                colorsDic[rgb] += 1
    print colorsDic
    return len(colorsDic)



# Try to cartonify the picture and compare it to the original
def isCartoonPicture(picture):
    orig = cv2.imread(picture)
    orig = cv2.cvtColor(orig, cv2.COLOR_BGR2HSV)
    img = cv2.bilateralFilter(orig, 3, 200, 200)
    img = colorQuantization(img, 5)
    return np.mean(orig - img)

#===============================================================================
# for f in os.listdir("../resources/SOpictures"):
#     print "%s -> %f " % (f, isCartoonPicture("../resources/SOpictures/%s" % f))
#===============================================================================
hist = hist_curve("../resources/SOpictures/170.jpg")
cv2.imshow('histogram',hist)
cv2.waitKey(0)
cv2.destroyAllWindows()