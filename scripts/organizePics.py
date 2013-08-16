"""
Organize pictures in directories according to their labels stored in a csv file
@author: Alexandre Bisiaux
"""

from unicodeMagic import UnicodeReader
import os

picPath = '../resources/SOpictures/'
organizePath = '../resources/SOpictures/organizedPics/'
labels = '../resources/4.5k_sample.csv'

f = open(os.path.join(labels), "rb")
reader = UnicodeReader(f)

cpt = 0

for row in reader:
    uid = row[0]
    cl1 = row[1]
    cl2 = row[2]
    cl3 = row[3]

    newPath = organizePath + cl1 + "/" + cl2 + "/" + cl3 + "/"
    if not os.path.exists(newPath): os.makedirs(newPath)
    os.rename(picPath + uid + ".jpg", newPath + uid + ".jpg")
    cpt += 1

print "%s files organized" % cpt
