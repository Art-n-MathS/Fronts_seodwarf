def getThresholds(i_centres):
        thres = [None] * (len(i_centres)-1)
        print i_centres
        for i in range (0, len(i_centres)-2):
            thres[i]=(i_centres[i]+i_centres[i+1])/2
        thres[len(thres)-1]=255
        print "System is returning the following thresholds:"
        print thres
        return thres