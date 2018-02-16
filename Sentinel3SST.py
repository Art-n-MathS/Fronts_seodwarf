## @package Sentinel3SST
#  @brief a class the extracts products from sentinel and exports them into .tiff files
#  @author Dr. Milto Miltiadou
#  @date Nov 2017
#  @version 1.0

import GdalCommands
import os
import glob
import glob
import subprocess


class Sentinel3SST: 
    ## constructor
    def __init__(self,i_inFolder,i_outFolder):
        self.inFolder = i_inFolder
        self.outFolder = i_outFolder
        self.tempImgs = []
        print i_inFolder, self.outFolder
        
    ## method that extracts a band from the .nc file and exports it as .tif
    # @param[in] i_subdataset the name of the band to be extracted
    # @param[in] i_name the name of the .tif file to be exported  
    # @note This approach does not reproject image. No coordinate system\projection. Alternatively use generateTifGpt
    def generateTif(self, i_subdataset, i_name):
        print "WARNING: This approach does not reproject image. No coordinate system\\projection. Alternatively use generateTifGpt"
        workingDir = os.getcwd()
        os.chdir(self.inFolder)
        nc = glob.glob("2*nc")[0]
        os.chdir(workingDir)
        GdalCommands.translateNETCDFtoTIFF(self.inFolder+"/"+nc, i_subdataset, self.outFolder+"/"+i_name)
        
        
    ## method that extracts a band from the .nc file and exports it as .tif
    # @details It uses SNAP s function using gpt. It also geocorrects the image
    # @param[in] i_subdataset the name of the band to be extracted
    # @param[in] i_name the name of the .tif file to be exported  
    def generateTifGpt(self, i_subdataset,i_name):
        print "Extracting and geocorrecting ", i_subdataset, " band"
        nc = glob.glob(self.inFolder+"/*.nc")[0]
        cmd = "gpt \"gptCommands\ExtractReprojectBandfromS3_SLSTR.xml\" -Pin=" + nc + " -Pband=" + i_subdataset + " -Pout=\"" + i_name
        print cmd
        subprocess.call(cmd)

        
        
        
    