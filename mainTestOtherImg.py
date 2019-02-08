
import numpy as np
import argparse
import sys
import Sentinel3SST
import Fronts 
import GeoJSON
import GeoImage
import Sentinel3OLCI

import Sentinel3SST
import IMAlgorithms as ima
import numpy as np
import GeoImage
import os

def getThresholds(i_centres):
    thres = [None] * (len(i_centres)-1)
    print i_centres
    for i in range (0, len(i_centres)-2):
        thres[i]=(i_centres[i]+i_centres[i+1])/2
    thres[len(thres)-1]=255
    print "System is returning the following thresholds:"
    print thres
    return thres


i_k=5 

geoImg = GeoImage.GeoImage("C:/Users/milto/Downloads/Italy/projected_S3A_SL_2_WST____20180719T205531_20180719T205831_20180719T232148_0179_033_314_0540_MAR_O_NR_002.SEN3.tif")

print "Calculating Fronts using the Kmeans Approach"
geoImg.medianFilter(9)
geoImg.enchancementHistEqualisation()

geoImg.exportImage("C:/Users/milto/Downloads/Italy/SSTKmeansPreProcessed.tif")
centres = np.array(geoImg.clusterWithKMeans(i_k,10,1)).astype(np.uint8)
centres.sort()
centres=np.append(centres,[255])
print centres
geoImg.SeparateLowMidHigh(getThresholds(centres),2)
geoImg.exportImage("C:/Users/milto/Downloads/Italy/SSTKmeansClustered.tif")
        
geoImg.medianFilter(9)
geoImg.exportImage("C:/Users/milto/Downloads/Italy/SSTKmeansClusteredfilteredUTM22.tif")
geoImg.Laplacian()
geoImg.exportImage("C:/Users/milto/Downloads/Italy/SSTtestKmeansLaplacianUTM22.tif") 



geoImg = GeoImage.GeoImage("C:/Users/milto/Downloads/cyprus3/projected_201807~1.tif")

print "Calculating Fronts using the Kmeans Approach"
geoImg.medianFilter(9)
geoImg.enchancementHistEqualisation()
geoImg.exportImage("C:/Users/milto/Downloads/cyprus3/SSTKmeansPreProcessed.tif")
centres = np.array(geoImg.clusterWithKMeans(i_k,10,1)).astype(np.uint8)
centres.sort()
centres=np.append(centres,[255])
print centres
geoImg.SeparateLowMidHigh(getThresholds(centres),2)
geoImg.exportImage("C:/Users/milto/Downloads/cyprus3/SSTKmeansClustered.tif")
geoImg.medianFilter(9)
geoImg.exportImage("C:/Users/milto/Downloads/cyprus3/SSTKmeansClusteredfilteredUTM22.tif")
geoImg.Laplacian()
geoImg.exportImage("C:/Users/milto/Downloads/cyprus3/SSTtestKmeansLaplacianUTM22.tif") 