## @package GeoJSON
#  @brief This class is used for storing geometry releated results, like Polygons and LineStrings and for exporting them into a .json file
# 
#  @author Dr. Milto Miltiadou
#  @date 3rd of Nov, 2017
#  @version 1.0

#

import sys

class GeoJSON:
    ## The constructor
    # @param[in] the type of features to be saved, "LineString" or "Polygon"
    def __init__(self,i_type):
        if((i_type!="Polygon") & (i_type!="LineString")):
            print "ERROR: i_type must either be \"Polygon\" or \"LineString\""
            sys.exit(1)
        ## the type of the saved features ("LineString" or "Polygon")
        self.type = i_type
        ## a list containing a list for each feature with its coordinates
        self.coordinates = []
        ## a list containing a list for each feature with its properties
        self.properties = []
        ## the coordinate system of the features
        self.coordinateSystem = ""
        ## the index of the current features, where new values will be added to
        self.current = -1
        
    ## method that moves the pointer to the next\new feature
    def nextFeature(self):
        self.current+=1
        self.coordinates += [[]]
        self.properties +=[[]]
    
    ## method that adds the given coordinates to the list of 
    # coordinates of the current feature
    # @param[in] i_x the x coordinate of the point to be added
    # @param[in] i_y the y coordinate of the point to be added
    def addCoordinates(self, i_x, i_y):
        self.coordinates[self.current] += [[i_x,i_y]]
        
        
    ## method that adds a propery to the current feature
    # @param i_name[in] the name of the property to be added
    # @param i_value[in] the value of the property to be added
    def addProperty(self, i_name, i_value):
        self.properties[self.current] += [i_name,i_value]
        
    
    ## method that sets the coordinate system
    # @param[in] i_coordinateSytem the coordinate system in a string
    def setCoordinateSystem(self, i_coordinateSystem):
        self.coordinateSystem = i_coordinateSystem
        
    ## method that export the export the stored features in a .json file
    # @param[in] i_filename the name of the the .json file to be exported
    def export(self, i_filename):
        print i_filename
        file = open(i_filename,"w") 
        file.write("{\"type\": \"FeatureCollection\",\n") 
        if (self.coordinateSystem == "") :
            print "Warning: Coordinate System is missing"
        else :
            file.write(" \"crs\": {\n     \"type\": \"name\",\n     \"properties\": {\n         \"name\":\"")
            file.write(self.coordinateSystem)
            file.write("\"\n     }\n }")
            if(len(self.coordinates)!=0):
                file.write("\n ,")
        if(len(self.coordinates)!=0):
            file.write("\n \"features\": [\n")
            for x in range(0, len(self.properties)):
                file.write(" { \"type\": \"Feature\",\n")
                file.write("       \"geometry\": {\n")
                file.write("         \"type\": \"")
                file.write(self.type)
                file.write("\",\n")
                file.write("         \"coordinates\": [")
                if (self.type == "Polygon"):
                    file.write("[")
                for c in range (0, len(self.coordinates[x])):
                    strTmp = "\n           [" + str(self.coordinates[x][c][0])+"," + str(self.coordinates[x][c][1]) + "]"
                    if (c<len(self.coordinates[x])-1):
                        strTmp+=","
                    file.write(strTmp)
                #file.write(self.features[x])
                if (self.type == "Polygon"):
                    file.write("\n         ]]\n       }")
                else : 
                    file.write("\n         ]\n       }")
                if(len(self.properties)!=0):
                    file.write(",\n       \"properties\": {\n")
                    for p in range(0,len(self.properties[x])/2):
                        strTmp = "         \"" + str(self.properties[x][2*p]) + "\":\"" + str(self.properties[x][2*p+1]) + "\""
                        if (p<len(self.properties[x])/2-1):
                            strTmp+=","
                        strTmp +="\n"
                        file.write(strTmp)
                    file.write("       }")
                file.write("\n }")
                if (x<len(self.properties)-1):
                    file.write("\n ,\n")
            file.write("\n ]")
        file.write("\n}")
        file.close() 
        
    ## Method that prints all the parameters, used for debugging
    def debugPrint(self):
        print "Type             : ", self.type
        print "Properties       : ", self.properties
        print "Coordinate System: ", self.coordinateSystem
        print "Coordinates      : ", self.coordinates
        print "Current          : ", self.current
        
    