## @package GdalCommands
# This library contains useful commands from Gdal For example extracting a band from a Sentinel product and exporting it into a .tif file
#  @notes The coordinate system is not preserved when the gdal_translate command is used
#  @author Dr. Milto Miltiadou
#  @date 31st of Oct 2017
#  @version 1.0


import os
import gdal
from gdalconst import *
import sys
import subprocess

## this function takes as input a .nc file and export a .tif
def translateNETCDFtoTIFF(i_input, i_subdataset, i_output,):
    # store current directory to string
    workingDir = os.getcwd()
    # go to i_input dir
    os.chdir(os.path.dirname(i_input))
    # create the script in a string
    cmd = "gdal_translate -of GTiff HDF5:\"" + i_input + "\"://" + i_subdataset + " " + i_output 
    # run the script from the terminal
    print cmd
    subprocess.call(cmd)
    # return to working directory
    os.chdir(workingDir)


    