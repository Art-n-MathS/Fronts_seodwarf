## @package Sentinel3OLCI
#  @brief This class takes as input data acquired by the OLCI instrument and performs various functions 
#  @details For example it extracts the clouds and resize them to match the SLSTR instrument
#  (UNDER DEVELOPMENT)
#  @author Dr. Milto Miltiadou
#  @date 10th of Nov 2017
#  @version 1.0




import netCDF4
import sys
import cv2
import numpy as np
import scipy.misc

class Sentinel3OLCI:
    
    
    # default constructor
    def __init__ (self, i_inFolder):
        # the input .SEN3 folder containing the OL_2_WFR product
        self.inFolder = i_inFolder
        print "Sentinel 3 OLCI created \n"
    
    ## method that finds the clouds from the OL_2_WFR product of Sentinel 3 and exports them into a jpg image. For now the coordinate system is not preserved 
    def extractClouds(self):
        print "Start extracting clouds"
        nc  = netCDF4.Dataset(self.inFolder + "\wqsf.nc")
        ncv = nc.variables
        key = ncv.keys()[0]
        
        flag_meanings = nc[key].flag_meanings.split()
        flag_masks = nc[key].flag_masks
                        
        for x in range (0,len(flag_meanings)):
            if (flag_meanings[x]=="CLOUD"):
                cloud = flag_masks[x]
            elif (flag_meanings[x]=="CLOUD_AMBIGUOUS"):
                cloud_ambiguous = flag_masks[x]
            elif (flag_meanings[x]=="CLOUD_MARGIN"):
                cloud_margin = flag_masks[x]
        lenX = len(nc[key]) 
        if lenX<1 :
            print "ERROR: length of masks with the netCDF file should be greater than 0"
            sys.exit(1)
        lenY = len(nc[key][0])
        
        nArray = np.zeros((lenX, lenY), np.uint8) 
        for x in range (0,lenX):
            print x
            tmpArr = nc[key][x]
            for y in range (0,lenY):
                if (tmpArr[y]==cloud):
                    nArray[x][y] = 255
                elif (tmpArr[y]==cloud_ambiguous):
                    nArray[x][y] = 176
                elif (tmpArr[y]==cloud_margin):
                    nArray[x][y] = 100
        scipy.misc.imsave('C:\Users\milto\Downloads\cyprus/outfile.jpg', nArray)
        
        print nc
        print "====================="
        print ncv
        print "====================="
        print key
        print "====================="
        print flag_meanings, len(flag_meanings)
        print "====================="
        print flag_masks, len (flag_masks)
        print "====================="
        print  cloud, cloud_ambiguous, cloud_margin
    