## package main
#  @ brief this file is used for testing the classes and libraries created
#
#  @details How to run the program: 
#  @details python main.py -inFolder <inputFolder> -outFolder <outFolder>
#
#  @details Example:
#
#  @details ##### Cyprus example SLSTR ####
#
#  @details cd C:/Users/milto/Documents/TEPAK/RISE/SEO_DWARF_algorithms/Fronts/
# @details python main.py -inFolder "C:/Users/milto/Downloads/cyprus/S3A_SL_2_WST____20171014T080458_20171014T080758_20171014T101117_0179_023_192_2339_MAR_O_NR_002.SEN3" -outFolder "C:\Users\milto\Documents\TEPAK\RISE\SEO_DWARF_algorithms\TestResults"
#
#
#  @details #####   Cyprus 2 example OLCI 2 WFR   ####
#
#  @details python C:/Users/milto/Documents/TEPAK/RISE/SEO_DWARF_algorithms/Fronts/main.py -inFolder "C:\Users\milto\Downloads\cyprus2\S3A_OL_2_WFR____20170909T081227_20170909T081527_20170910T153111_0180_022_078_2339_MAR_O_NT_002.SEN3" -outFolder "C:\Users\milto\Documents\TEPAK\RISE\SEO_DWARF_algorithms\TestResults"
#
#  @details python C:/Users/milto/Documents/TEPAK/RISE/SEO_DWARF_algorithms/Fronts/main.py -inFolder "C:\Users\milto\Downloads\cyprus2\S3A_OL_2_WFR____20170909T081227_20170909T081527_20170910T153111_0180_022_078_2339_MAR_O_NT_002.SEN3" -outFolder "C:\Users\milto\Documents\TEPAK\RISE\SEO_DWARF_algorithms\TestResults\TurbFilterTests"
#
#  @author Dr. Milto Miltiadou
#  @date 31st of Oct 2017
#  @version 1.0

import numpy as np
import argparse
import sys
import Sentinel3SST
import Fronts 
import GeoJSON
import GeoImage
import Sentinel3OLCI


# parsing command line inputs
parser = argparse.ArgumentParser()
parser.add_argument("-inFolder",
     required=True,
     help="path to folder containing SL_WST product of Sentinel 3",
     metavar='<string>')
parser.add_argument("-outFolder",
     required=True,
     help="path to folder where results will be stored",
     metavar='<string>')

params = vars(parser.parse_args())
inFolder = params['inFolder']
outFolder = params['outFolder']

"""
frontsImg = Fronts.Fronts(inFolder,outFolder)
#frontsImg.kmeansApproach(6)
#frontsImg.meanShifClusteringApproach()
#frontsImg.cannyEdgeApproach()
frontsImg.laplacianEdgeApproach()
sys.exit(0)
"""




turbImg = GeoImage.GeoImage("C:\Users\milto\Downloads\cyprus\S3A_SL_2_WST____20171014T080458_20171014T080758_20171014T101117_0179_023_192_2339_MAR_O_NR_002.SEN3\sea_surface_temperature.tif")
turbImg.medianFilter(9)
turbImg.SeparateLowMidHigh([20,30,40],0)
turbImg.exportImage(outFolder + "/turbThres.tif")


"""
SS3Img = GeoImage.GeoImage("C:\Users\milto\Documents\TEPAK\RISE\SEO_DWARF_algorithms\TestResults\SST.tif")
SS3Img.exportImage("C:\Users\milto\Documents\TEPAK\RISE\SEO_DWARF_algorithms\TestResults\SSTcopy.tif")
"""




#s3img = Sentinel3OLCI.Sentinel3OLCI(inFolder)
#s3img.extractClouds()

