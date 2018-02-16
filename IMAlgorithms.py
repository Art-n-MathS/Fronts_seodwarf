## @package IMAlgorithms
#  @brief This is a class for processing GeoTiff Images using well-known Image Processing techniques 
#  @details The GeoImage class is an update of this one
#  @details The cunny edge detection member started from Anastasia Sarelli
#  @author: Dr. Milto Miltiadou
#  @date: 
#  @version 1.0


import numpy as np
import cv2
from osgeo import gdal
import os
from matplotlib import pyplot as plt

# Function modified by Milto from :
# https://stackoverflow.com/questions/14464449/using-numpy-to-efficiently-convert-16-bit-image-data-to-8-bit-for-display-with
def display(image): 
    image[image<0.0001] = 0.0
    imgTemp = image[image>0.0001]
    median = np.median(imgTemp)
    std = np.std(imgTemp)
    minV = np.int16(round(max(median-2.0*std,np.amin(imgTemp))))
    maxV = np.int16(round(min(np.amax(imgTemp),median+2.0*std)))
    image[image<minV] = minV
    image[image>maxV] = maxV
    
    image = np.array(image, copy=True)
    image.clip(minV, maxV, out=image)
    image -= minV
    np.floor_divide(image, (maxV - minV + 1) / 256,
                    out=image, casting='unsafe')
    image[image<0.0001] = 0
    return image.astype(np.uint8)

def auto_canny (imageFile,Output) :
    inp_raster = gdal.Open(imageFile)
    imArr = np.array(inp_raster.ReadAsArray())

    # Adjust image to be UINT8 so that it can be an input to canny edge function
    image2 = display(imArr)
    
    gaussian_1 = cv2.GaussianBlur(image2, (9,9), 10.0)
    unsharp_image = cv2.addWeighted(image2, 1.5, gaussian_1, -0.5, 0, image2)
    
    #apply filter to find stamp pieces, histogram equalization on greyscale
    image = cv2.equalizeHist(unsharp_image)
    image = cv2.equalizeHist(image)
    
    # apply sharpening kernel
    # kernel = np.array([[0,-1,0], [-1,3,-1], [0,-1,0]])
    # image= cv2.filter2D(image, -1, kernel)
    
    # Apply canny edge detection algorithm
    edged=cv2.Canny(image, 100, 200)
        
    # Export image
    driver = gdal.GetDriverByName("GTiff")
    [cols, rows] = imArr.shape
    print cols, rows
    outdata = driver.Create(Output, rows, cols, 1, gdal.GDT_UInt16)
    outdata.SetGeoTransform(inp_raster.GetGeoTransform())##sets same geotransform as input
    outdata.SetProjection(inp_raster.GetProjection())##sets same projection as input
    outdata.GetRasterBand(1).WriteArray(edged)
    outdata.GetRasterBand(1).SetNoDataValue(0)##if you want these values transparent
    outdata.FlushCache() ##saves to disk!!

#os.chdir('/home/anastasia/Desktop/eo_psarakia/')
#auto_canny('C:/Users/milto/Downloads/cyprus/S3A_SL_2_WST____20171014T080458_20171014T080758_20171014T101117_0179_023_192_2339_MAR_O_NR_002.SEN3/allbands.tif','C:/Users/milto/Downloads/cyprus/S3A_SL_2_WST____20171014T080458_20171014T080758_20171014T101117_0179_023_192_2339_MAR_O_NR_002.SEN3/allbands_CANNY_EDGE_afterDoubleEqualisation100_200.tif')

