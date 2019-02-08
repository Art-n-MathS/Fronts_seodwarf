
## @package GeoImage2
#  This class contains an image and can apply various functions to it 
#  (for example canny edge).
#  @author Dr. Milto Miltiadou
#  @date Oct 2017
#  @version 1.0


import numpy as np
import cv2
from osgeo import gdal
from gdalconst import *
import math
from matplotlib import pyplot as plt
import copy
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets.samples_generator import make_blobs


## 
class GeoImage:
   
    ## method that transform an image to uint8 
    def display(self, image): 
        print " *** ", type(image), " *** "
        imgTemp = image.flatten()
        print len(imgTemp)
        imgTemp = [x for x in imgTemp if (not math.isnan(x) and x>0.000001 and x is not self.noValue )]
        print len(imgTemp)
        print type(imgTemp[0])
        median = np.median(imgTemp)
        std = np.std(imgTemp)
        minV = np.int16(round(max(median-2.0*std,np.amin(imgTemp))))
        maxV = np.int16(round(min(np.amax(imgTemp),median+2.0*std)))
        print median, minV, maxV, std
        for i in range(0,len(image)):
            image[i] = [0.0 if (math.isnan(x) or x<0.000001) else ((x-minV)*254/(maxV-minV)+1.0) for x in image[i]]
        print np.amin(image), np.amax(image)
        image[image<0.0] = 0.0
        image[image>255.0] = 255.0
        self.noValue = 0
        return image.astype(np.uint8)

    ## The constructor
    #  @param i_inputTif the input image in tif format
    def __init__(self, i_inputTif):
        inp_raster = gdal.Open(i_inputTif)
        ## the value that represents null within the image
        self.noValue = inp_raster.GetRasterBand(1).GetNoDataValue()
        print self.noValue, "***************************"
        imArr = np.array(inp_raster.ReadAsArray())
        [self.cols, self.rows] = imArr.shape
        ## the array containing the values of the image
        print "++++++++++++++++++++++++", imArr.dtype
        if (imArr.dtype != np.uint8):
            print "Converting image to numpy.unit8, required by OpenCV"
            self.image = self.display(imArr)
        else :
            self.image = imArr
        ## the geo transformation of the image
        self.geoTransform = inp_raster.GetGeoTransform()
        ## the projection of the image
        self.projection = inp_raster.GetProjection()
        
    ## method that applies a given filter kernel to the image
    #  @param[in] i_kernel the kernel to be applied
    def applyfiler(self, i_kernel):
        #  e.g. [[0,-1,0], [-1,3,-1], [0,-1,0]]
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        self.image= cv2.filter2D(self.image, -1, kernel)
        
    def blurUsingGausian(self):
        gaussian_1 = cv2.GaussianBlur(self.image, (9,9), 10.0)
        self.image = cv2.addWeighted(self.image, 1.5, gaussian_1, -0.5, 0, self.image)
    
    def enchancementHistEqualisation(self):
        gaussian_1 = cv2.GaussianBlur(self.image, (9,9), 10.0)
        self.image = cv2.addWeighted(self.image, 1.5, gaussian_1, -0.5, 0, self.image)
        self.image = cv2.equalizeHist(self.image)
        
    
    ## Method that applies a median filter for "salt & pepper" noise removal
    #  @param[in] i_size the size of the kernel to be applied. It must always be an odd number
    def medianFilter(self, i_size):
        self.image=cv2.medianBlur(self.image,i_size)
        print "Median Filter has been applied"

    
    ## method that blurs an image using an averaging filter
    #  @param[in] the size of the filter to be applied. It must be an odd number
    def averageBlur(self, i_size):
        self.image = cv2.blur(self.image,(i_size,i_size))
        print "Averaging Filter has been applied" 
        
 
    ## Method that clusters the image using the k-means algorithm
    #  @param[in] i_k the numbers of clusters to be created
    #  @param[in] i_maxIter number max iterations to be done
    #  @param[in] i_e the max error to terminate the iterations
    def clusterWithKMeans(self, i_k, i_maxIter, i_e):
        # Define criteria = ( type, max_iter = 10 , epsilon = 1.0 )
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, i_maxIter, i_e)
        
        # Set flags (Just to avoid line break in the code)
        flags = cv2.KMEANS_RANDOM_CENTERS
        # reshape img
        imgTemp = self.image.flatten()
        imgTemp = [x for x in imgTemp if not math.isnan(x)]    
        imgTemp = [x for x in imgTemp if x>0.0001]    
        imgTemp = np.asarray(imgTemp).astype(np.float32)
        # Apply KMeans
        print "Starting kmeans!!!"
        #plt.hist(imgTemp,256,[0,256]),plt.show()
        compactness,labels,centres = cv2.kmeans(imgTemp,i_k,criteria,i_maxIter,flags)
        print "\n\n", compactness,"\n\n",labels,"\n\n",centres, " ********************* "
        return centres.flatten()
    
    
        
    
    ## Method that thresholds and classifies the image
    # @param[in] i_weights an array indicating the weights of the classification e.g. [20,30,40] 
    # @param[in] i_thresType 1 for percentage of pixels
    # 2 when the imported weights are the actual thresholds as defined during 
    # calibration
    def SeparateLowMidHigh(self,i_weights, i_thresType):
        print i_weights
        assert(len(i_weights)>0), "The imported weights array should contain at least one value"
        lenWeights = len(i_weights)
        totalWeight = np.float32(np.sum(i_weights))
        imgTemp = self.image.flatten()
        imgTemp = [x for x in imgTemp if (x is not self.noValue )]
        imgTemp = [x for x in imgTemp if (x>0.000001)]
        noOfPixels = len(imgTemp)
        thresholds = copy.deepcopy(i_weights)
        print "weights      : " , i_weights
        print "total Weight : " , totalWeight
        
        print "---------- THRESHOLDS -----------"
        if (i_thresType==0):
            for i in range (0, len(i_weights)):
                thresholds[i] = np.float32(i_weights[i])/totalWeight*255.0  
            for i in range (1, len(i_weights)):
                i_weights[i]+=i_weights[i-1]
            thresholds+=[255]
            print thresholds , " thresholds"
            print i_weights , " weights"
            
        elif (i_thresType == 1) :
            imgTemp.sort()
            pixelsNo = len(imgTemp)
            print "++ " , pixelsNo
            for i in range (0, len(i_weights)):
                if (i!=0):
                    i_weights[i]=i_weights[i]+i_weights[i-1]
                print i, "     - ", i_weights[i]
                print i_weights 
                index= (np.float64(i_weights[i]))/totalWeight*np.float64(pixelsNo)-1.0
                print index, " * ", i ,":", thresholds[i], " = "
                print np.float32(i_weights[i]), " / ", totalWeight, " * ", np.float32(pixelsNo)
                print "\n"
                thresholds[i] = imgTemp[int(index)]

                
            for i in range (1, len(i_weights)):
                i_weights[i]+=i_weights[i-1]
        print thresholds
        
        print "-----------------------------------"
        
        newImg = copy.deepcopy(self.image)
        for i in reversed(range(0,len(thresholds))):
            print "*** " , i , " " , len(thresholds), " ", thresholds[i]
            newImg[self.image<= thresholds[i]+0.000001]=i+1
        newImg[self.image<= 0.000001]=0
        self.image = copy.deepcopy(newImg)
        print "Separate Low Min High"
        
    def meanShiftClustering(self):
        X =np.array([self.image.flatten()]).reshape(-1,1)
        print X.shape
        # The following bandwidth can be automatically detected using
        bandwidth = estimate_bandwidth(X, quantile=0.2, n_samples=500)
        print "bandwidth = " , bandwidth

        ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
        print "Start fitting"
        ms.fit(X)
        labels = ms.labels_
        cluster_centers = ms.cluster_centers_
        print cluster_centers

        labels_unique = np.unique(labels)
        n_clusters_ = len(labels_unique)
        
        print("number of estimated clusters : %d" % n_clusters_)
        return cluster_centers.flatten()
        
    
    ## Method that creates and stores the histogram of an image
    #  @param[in] i_name the name of the image to be stored
    def getHist(self, i_name):
        #hist = cv2.calcHist([self.image],[0],None,[256],[0,256])
        hist,bins = np.histogram(self.image,256,[1,256])
        plt.hist(hist.ravel(),120,[1,256])
        plt.savefig(i_name)
    
    ## Method that applies the Canny Edge algorithm to the image
    #  @param[in] i_sigma    
    def CannyEdge(self,i_sigma):   
        val = self.image[self.image>0]
        v=np.median(val)     
        lower=int(max(np.amin(val),(1.0 - i_sigma)*v)) 
        upper=int(min(np.amax(val),(1.0 + i_sigma)*v))
        self.image=cv2.Canny(self.image, lower, upper)
        
    def Laplacian(self):
        self.image = cv2.Laplacian(self.image,cv2.CV_64F)
        #sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
        #sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)

    ## Method that exports the current stage of the image as 
    #  a GeoTiff image
    #  @param[in] i_output the name of the file to be exported    
    def exportImage(self, i_output):
        print "Exporting image : " , i_output
        driver = gdal.GetDriverByName("GTiff")
        outdata = driver.Create(i_output, self.rows, self.cols, 1, gdal.GDT_UInt16)
        # sets same geotransform as input
        outdata.SetGeoTransform(self.geoTransform)
        # sets same projection as input
        outdata.SetProjection(self.projection)
        outdata.GetRasterBand(1).WriteArray(self.image)
        # sets no value 
        outdata.GetRasterBand(1).SetNoDataValue(self.noValue)
        outdata.FlushCache()