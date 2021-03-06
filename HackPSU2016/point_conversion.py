#!/usr/bin/env python

import cv2
import numpy as np
import sys
import os
import string
import math
import time

path = sys.argv[1]
t1 = float(sys.argv[2])
t2 = float(sys.argv[3])

heightcount = 1
valuecount = 1

pointcount = 0
linecount = 0
layercount = 0

pointmesh = open(path[0:string.rfind(path, "\\")] + 'xyzmesh.xyz', 'w')

for imageslice in os.listdir(path):

    if math.sqrt(heightcount) >= valuecount:

        RGBslice = cv2.imread(path + imageslice)
        grayslice = cv2.cvtColor(RGBslice, cv2.COLOR_BGR2GRAY)
        edgeslice = cv2.Canny(grayslice, t1, t2, apertureSize=5)

        baseslice = RGBslice.copy()
        baseslice = np.uint8(baseslice/2.)
        baseslice[edgeslice != 0] = (0, 255, 0)

        for line in edgeslice:
            for point in line:

    	        if point > 0:
    	            pointmesh.write("%s\t%s\t%s\n" % (pointcount, linecount, layercount))
                pointcount += 1

            pointcount = 0
	    linecount += 1

        linecount = 0
        layercount += 1

        valuecount += 1
    heightcount += 1

pointmesh.close()
