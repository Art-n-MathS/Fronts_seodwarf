## package main
#  @ brief this file is used for testing the classes and libraries created
#
#  @details How to run the program: 
#  @details cd <directory of code> 
#  @details python main.py -inFolder <inputFolder> -outFolder <outFolder> -alg <nameOfAlgorithm>
#
#  @details Example:
#
#  @details ##### Cyprus example SLSTR ####
#
#  @details cd C:/Users/milto/Documents/TEPAK/RISE/SEO_DWARF_algorithms/Fronts/
#  @details python main.py -inFolder "C:/Users/milto/Downloads/cyprus/S3A_SL_2_WST____20171014T080458_20171014T080758_20171014T101117_0179_023_192_2339_MAR_O_NR_002.SEN3" -outFolder "C:\Users\milto\Documents\TEPAK\RISE\SEO_DWARF_algorithms\TestResults\fronts" -alg kmeans

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
parser.add_argument("-alg",
     required=True,
     help="\"kmeans\" for the k-means algorithm or \"meanshift\" for the Mean Shift algorithm ",
     metavar='<string>')

params = vars(parser.parse_args())
inFolder = params['inFolder']
outFolder = params['outFolder']
alg = params['alg']


if alg == "kmeans":
    print "k-means Algorithm"
    frontsImg = Fronts.Fronts(inFolder,outFolder)
    frontsImg.kmeansApproach(6)
elif alg == "meanshift" :
    print "Mean Shift Algorithm"
    frontsImg = Fronts.Fronts(inFolder,outFolder)
    frontsImg.meanShifClusteringApproach()
else :
    print "ERROR: Algorithm requested not applicable"
    sys.exit(1)

