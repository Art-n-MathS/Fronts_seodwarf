## package main
#  @ brief this file is used for testing the classes and libraries created
#
#  @details How to run the program: 
# 
#  @details format: python main.py -inImg <inputImg> -outImg <outImg> -type <kmeans, thresholds or percentage> -thres <[low, med, high]> -geojson <output_name>
#  @details -inImg : followed by the name and directory of the input image
#  @details -outImg : followed by the name and directory of the clustered image to be exported
#  @details -type : type of clustering to be performed. You may choose between kmeans, thresholds and percentage
#  @details -thres : if a type threshold is chosen, then you should also include a list of three numbers containing the predefined thresholds
# @details -geojson : the name of the file, where the vector with the clustered image will be inluded, containing tags of low med high turb. 
#
#  @details Example: 
#  @details python C:\Users\milto\Documents\TEPAK\RISE\SEO_DWARF_algorithms\Fronts\mainTurbCalibration.py -in "C:\Users\milto\Documents\TEPAK\RISE\SEO_DWARF_algorithms\TestResults\S2A_2017-08-13_T33TXF_resultsPresentedInBari5Oct17\TURB\S2A_2017-08-13_T33TXF_TURB_DOGLIOTTI2015.tif" -out "C:\Users\milto\Documents\TEPAK\RISE\SEO_DWARF_algorithms\TestResults\S2A_2017-08-13_T33TXF_resultsPresentedInBari5Oct17\TURB\S2A_2017-08-13_T33TXF_TURB_DOGLIOTTI2015_clustered.tif" -type kmeans -geojson "C:\Users\milto\Documents\TEPAK\RISE\SEO_DWARF_algorithms\TestResults\S2A_2017-08-13_T33TXF_resultsPresentedInBari5Oct17\TURB\S2A_2017-08-13_T33TXF_TURB_DOGLIOTTI2015.json"
#
#  @author Dr. Milto Miltiadou
#  @date 17th Apr 2018
#  @version 1.0

import numpy as np
import argparse
import sys
import GeoImage
import re
import subprocess
import gdal
from gdalconst import *


# parsing command line inputs
parser = argparse.ArgumentParser()
parser.add_argument("-inFolder",
     required=True,
     help="path to folder containing S2 data (first folder, neither IMG_DATA nor TURB product)",
     metavar='<string>')
parser.add_argument("-outFolder",
     required=True,
     help="path to folder where results are stored",
     metavar='<string>')

parser.add_argument("-type",
     required=True,
     help="type of clustering to be performed. You may choose between \"kmeans\", \"thresholds\" and \"percentage\"",
     metavar='<string>')
parser.add_argument("-thres", nargs='+', type=int,
     required=False,
     help="if a type threshold is chosen, then you should also include a list of two numbers defining the thresholds. The numbers should be within the range of [0,255]. The values of an image are automatically scaled using a min-max scale to lie within that range. For example, if the thresholds 20 50 are given, then the range  [0-19] will indicate low turbidity, the range [20-49] will indicate medium Turbidity and the range [50-255] will indicate high turbidity."
     )
parser.add_argument("-pers", nargs='+', type=int,
     required=False,
     help="if a type percentage is chosen, then you should also include a list of three numbers defining the perecntages of the corresponding low, med and high Turbidity. For example, if the number 2 5 3 are given, then 20% will be low turbidity, 50% will be medium turbidity and 30% high turbidity. The numbers do not need to sum up to something (e.g. 1 or 100). The program automatically adjust the percentages as shown in the example."
     )
parser.add_argument("-nameAddition",
     required=True,
     help="Give a string that will be added to the name of the outputed img",
     metavar='<string>')
     


params  = vars(parser.parse_args())
inFolder  = params['inFolder']
outFolder = params['outFolder']
typeC   = params['type'] 
thres   = params['thres'] 
pers    = params['pers']
nameAddition    = params['nameAddition']


# reading metadata and searching tile name in input folder
MTD_MSIL1C = inFolder + 'MTD_MSIL1C.xml'

match = re.search('([A-Z][1-9][1-9][A-Z][A-Z][A-Z])', inFolder)
tile = match.group(0)
EPSG_code = 'EPSG_326' + tile[1:3]

dataset = gdal.Open('SENTINEL2_L1C:%s:10m:%s' % (MTD_MSIL1C, EPSG_code), GA_ReadOnly)
					
if dataset is None:
	print ('Failed to Read Metadata: Exiting')
	sys.exit(0)

MTD = dataset.GetMetadata()

DATE = MTD['GENERATION_TIME'][0:10]
HOUR = MTD['GENERATION_TIME'][11:16]

if MTD['DATATAKE_1_SPACECRAFT_NAME'] == 'Sentinel-2A':
	sensor = 'S2A'
elif MTD['DATATAKE_1_SPACECRAFT_NAME'] == 'Sentinel-2B':
	sensor = 'S2B'
	
# --- Check if Output Folder has been created - if not then exit ---
print('Checking if TURB product exist')

inImg = outFolder + sensor + '_' + DATE + '_' + tile +"/TURB/" +sensor + '_' + DATE + '_' + tile + "_TURB_DOGLIOTTI2015.tif"

outImg =  outFolder + sensor + '_' + DATE + '_' + tile +"/TURB/" +sensor + '_' + DATE + '_' + tile + "_TURB_DOGLIOTTI2015_classified_" + nameAddition + ".tif"

geojson = outFolder + sensor + '_' + DATE + '_' + tile +"/TURB/" +sensor + '_' + DATE + '_' + tile + "_TURB_DOGLIOTTI2015.json"


img = GeoImage.GeoImage(inImg)

print "\n"

if(typeC=="kmeans"):
    print "Low-Mid-High classes are caclulated using the k-means algorithms"
    centres = np.array(img.clusterWithKMeans(3,10,1)).astype(np.uint8)
    centres.sort()
    centres=np.append(centres,[255])
    print centres
    img.SeparateLowMidHigh(centres,2)
elif (typeC=="thresholds"):
    print "Low-Mid-High classes are cacluated using pre-defined thresholds"
    if (thres == None or len(thres)!=2):
        print "ERROR: Thresholds has not been defined or the number of provided thresholds not equal to 2"
        exit(1)
    elif (thres[0]<0 or thres[1]<0 or thres[0]>255 or thres[1]>255):
        print "ERROR: The thresholds should be within the range [0,255]"
        exit(1)
    thres = np.append(thres,[255])
    img.SeparateLowMidHigh(thres,2)
elif (typeC=="percentage"):
    print "Low-Mid-High classes are calculated using pre-defined percentages"
    img.SeparateLowMidHigh(pers,1)
else :
    print "ERROR: Type not recognised\n"
    exit(1)
    
img.medianFilter(15)
img.medianFilter(11)
img.medianFilter(9)
img.exportImage(outImg)


# TO DO: Test the following command and make gdal_polygonise run automatically from Anaconda Prompt
"""
cmd= "gdal_polygonize.bat " + outImg+ " -f GeoJSON " + geojson
print cmd
subprocess.call(cmd, shell=True)
"""

