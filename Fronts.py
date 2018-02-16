## @package Fronts
#  @brief This class investigates different approaches for calculating the Fronts
#  @date 2nd Nov 2017
#  @version 1.0
#  @author Dr. Milto Miltiadou


import Sentinel3SST
import IMAlgorithms as ima
import numpy as np
import GeoImage
import os

class Fronts:
    ## the constructor
    def __init__ (self, i_inFolder, i_outFolder):
        ## the input .SEN3 folder that contains Sentinel 3 SLSTR product of level 2
        self.inFolder = i_inFolder
        ## the directory where the results will be stored
        self.outFolder = i_outFolder
        ## the sea surface temperature product of Sentinel 3
        SST = Sentinel3SST.Sentinel3SST(i_inFolder, i_outFolder)
        # Create a GeoTiff image of the SST product
        SST.generateTifGpt("sea_surface_temperature",self.inFolder+"/sea_surface_temperature.tif")
        self.geoImg = GeoImage.GeoImage(self.inFolder+"/sea_surface_temperature.tif")
        #os.remove(self.inFolder+"/sea_surface_temperature.tif")
            
        
    def kmeansApproach(self, i_k):
        print "Calculating Fronts using the Kmeans Approach"
        #self.geoImg.blurUsingGausian()
        #self.geoImg.exportImage(self.outFolder+"/blurred.tif")
        #self.geoImg.enchancementHistEqualisation()
        #self.geoImg.exportImage(self.outFolder+"/HistEq.tif")
        self.geoImg.applyfiler( [[0,-1,0], [-1,3,-1], [0,-1,0]])
        centres = np.array(self.geoImg.clusterWithKMeans(i_k,10,1)).astype(np.uint8)
        centres.sort()
        centres=np.append(centres,[255])
        print centres
        self.geoImg.SeparateLowMidHigh(centres,2)
        self.geoImg.medianFilter(9)
        self.geoImg.exportImage(self.outFolder + "/SSTKmeansClusteredfiltered.tif")
        self.geoImg.Laplacian()
        self.geoImg.exportImage(self.outFolder + "/SSTtestKmeansLaplacian.tif") 
        
        #ima.auto_canny (self.outFolder+"/SST.tif",self.outFolder+"/edgedF_H.tif")
        
    def meanShifClusteringApproach(self):
        print "Calculating Fronts using the mean shift clustering approach"
        self.geoImg.medianFilter(5)
        self.geoImg.averageBlur(5)
        self.geoImg.averageBlur(7)
        centres = np.array(self.geoImg.meanShiftClustering()).astype(np.uint8)
        centres.sort()
        centres=np.append(centres,[255])
        print centres
        self.geoImg.SeparateLowMidHigh(centres,2)
        self.geoImg.exportImage(self.outFolder + "/SSTMedianClusteringApproach.tif") 
        self.geoImg.medianFilter(9)
        self.geoImg.Laplacian()
        self.geoImg.exportImage(self.outFolder + "/SSTMedianClusteringLaplacian.tif") 
        
    def cannyEdgeApproach(self):
        self.geoImg.blurUsingGausian()
        self.geoImg.enchancementHistEqualisation()
        self.geoImg.medianFilter(5)
        self.geoImg.CannyEdge(0.3)
        self.geoImg.exportImage(self.outFolder + "/SSTCanyEdgeEnchancement.tif")
        
    def laplacianEdgeApproach(self):
        #self.geoImg.blurUsingGausian()
        #self.geoImg.enchancementHistEqualisation()
        self.geoImg.medianFilter(5)
        self.geoImg.Laplacian()
        self.geoImg.exportImage(self.outFolder + "/SSTLablacian.tif")
        