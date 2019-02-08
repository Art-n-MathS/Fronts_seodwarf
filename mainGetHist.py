## package main
#  @ brief this file is used for creating and saving the histogram of an imported tif image. 
#
#  @details How to run the program: 
#  @details python main.py -in <inputDirName> -out <outDirName>
#
#  @details Example:
#
# @details python C:/Users/milto/Documents/TEPAK/RISE/SEO_DWARF_algorithms/Fronts/mainGetHist.py -in "C:\Users\milto\Downloads\cyprus2\Filters\0sea_surface_temperature.tif" -out "C:\Users\milto\Downloads\cyprus2\Filters\0sea_surface_temperatureHist.png"

#  @author Dr. Milto Miltiadou
#  @date 2nd of May 2018
#  @version 1.0

import numpy as np
import argparse
import sys
import GeoImage


# parsing command line inputs
parser = argparse.ArgumentParser()
parser.add_argument("-in",
     required=True,
     help="path to folder containing SL_WST product of Sentinel 3",
     metavar='<string>')
parser.add_argument("-out",
     required=True,
     help="path to folder where results will be stored",
     metavar='<string>')

params = vars(parser.parse_args())
inImg = params['in']
outImg = params['out']

img = GeoImage.GeoImage(inImg)
img.getHist(outImg)


