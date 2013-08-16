"""
Build the sample set for train and test classifiers
@author: Alexandre Bisiaux
"""

from randomReader import RandomReader
from unicodeMagic import UnicodeWriter
import os, re, csv

"""
Convert a csv file into a tab file
@param file: path to the csv file
"""
class csvToTab:
    def __init__(self, file):
        with open(file,'rb') as fin:
            cr = csv.reader(fin, delimiter=';')
            filecontents = [line for line in cr]
        new = file.replace("csv", "tab")
        with open(new,'wb') as fou:
            cw = csv.writer(fou, delimiter='\t')
            cw.writerows(filecontents)

"""
Build the sample set
@param inputFile: path to the SO users data
@param sampleFile: path to the output file
"""			
def buildSampleSet(inputFile, sampleFile):
    
    
    f = open(os.path.join(inputFile), "rb")
    f1 = open(os.path.join(sampleFile), "wb")

    reader = RandomReader(f)
    writer = UnicodeWriter(f1)
    
    nbRows = 0
    categories = []
    countPages = []
    for row in reader:
        nbRows += 1
        for cat in row[15:25]:
            if cat != "?":
                if not cat in categories:
                    categories.append(cat)
                    countPages.append(0)    
    data = []
    
    for row in reader:
        line = []
        for d in row[0:15]:
            line.append(d)
        for ind, cat in enumerate(categories):
            if cat in row[15:25]:
                countPages[ind] += 1
                line.append(str(1))
            else:
                line.append(str('?'))
        data.append(line)
    
    i = 0
    filteredCategories = []
    for cat, cpt in zip(categories, countPages):
        if cpt < 6: # Filter categories and keep only those which have more than 6 subjects in it
            ind = 15 + i
            for d in data:
                d.pop(ind)
        else:
            filteredCategories.append(cat)
            i += 1        
            
    # Header
    header = ["uid", "cl1", "cl2", "cl3", "cl4", "cl5", "face",
              "fCols", "nbCols", "f1", "f2", "f3", "s",
              "b", "bestGuess"]
    domain = ["c", "d", "d", "d", "d", "d", "d", "c", "c", "c", "c", "c", "c", "c", "string"]
    attribut = ["m", "c", "m", "m", "m", "m"]
    
    for cat in filteredCategories:
        header.append(cat)
        domain.append("d")
        
    writer.writerow(header)
    writer.writerow(domain)
    writer.writerow(attribut)
    i = 0
    for row in data:
        writer.writerow(row)
        i += 1
    f.close()
    f1.close()

buildSampleSet("../resources/4.5k_sample.csv", "../resources/sampleSet.csv")
csvToTab("../resources/sampleSet.csv") 