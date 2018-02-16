## @package GeoJSONexample
#  @brief Example of how to use the GeoJSON class
#  @details How to run the program: 
#  @details python GEOJSONexample.py -outJson <outFolder>
#  @details Example:
#  @details python C:/Users/milto/Documents/TEPAK/RISE/SEO_DWARF_algorithms/Fronts/GEOJSONexample.py -outFolder "C:\Users\milto\Documents\TEPAK\RISE\SEO_DWARF_algorithms\TestResults"
#  @author: Dr. Milto Miltiadou
#  @date 7th of Nov 2017
#  @version 1.0



import numpy as np
import argparse
import sys
import GeoJSON

# parsing command line inputs
parser = argparse.ArgumentParser()
parser.add_argument("-outFolder",
     required=True,
     help="path to folder where results will be stored",
     metavar='<string>')

params = vars(parser.parse_args())
outFolder = params['outFolder']


# example script for using the GeoJSON class for generating LineStrings
json = GeoJSON.GeoJSON("LineString")
json.setCoordinateSystem("+proj=utm +zone=33 +datum=WGS84 +units=m +no_defs")
json.nextFeature()
json.addCoordinates(600170,4600247)
json.addCoordinates(608254,4599055)
json.addCoordinates(609997,4593754)
json.addCoordinates(603997,4593754)
json.addProperty("phenomenon", "TEST")
json.addProperty("class", "low")
json.nextFeature()
json.addCoordinates(621903,4576792)
json.addCoordinates(603997,4593754)
json.addCoordinates(614747,4578514)
json.addProperty("phenomenon", "TEST")
json.addProperty("class", "high")
json.export(outFolder + "/LineString.json")
json.debugPrint()


# example script for using the GeoJSON class for generating Polygons
json = GeoJSON.GeoJSON("Polygon")
json.setCoordinateSystem("+proj=utm +zone=33 +datum=WGS84 +units=m +no_defs")
json.nextFeature()
json.addCoordinates(600170,4600247)
json.addCoordinates(608254,4599055)
json.addCoordinates(609997,4593754)
json.addCoordinates(603997,4593754)
json.addCoordinates(600170,4600247)
json.addProperty("phenomenon", "TEST")
json.addProperty("class", "low")
json.nextFeature()
json.addCoordinates(621903,4576792)
json.addCoordinates(603997,4593754)
json.addCoordinates(614747,4578514)
json.addCoordinates(621903,4576792)
json.addProperty("phenomenon", "TEST")
json.addProperty("class", "high")
json.export(outFolder + "/Polygon.json")
json.debugPrint()
