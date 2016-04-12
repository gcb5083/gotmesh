#!/usr/bin/env python

import cv2

import numpy as np
import sys
import os
import string
import math
import time

path = sys.argv[1]

if path[len(path) - 1] != '//':
    path = path + '//'

heightcount = 1
valuecount = 1

pointcount = 0
linecount = 0
layercount = 0

t1 = 2000
t2 = 4000

def nothing(*arg):
    pass

cv2.namedWindow('Edge Preview')
cv2.createTrackbar('Threshold 1', 'Edge Preview', 2000, 10000, nothing)
cv2.createTrackbar('Threshold 2', 'Edge Preview', 2500, 10000, nothing)
cv2.createTrackbar('Start', 'Edge Preview', 0, 1, nothing)
cv2.createTrackbar('Save Settings', 'Edge Preview', 0, 1, nothing)

start = 0
save = 0

pointmesh = open(path[0:string.rfind(path, "//")] + '_output.xyz', 'w')

for imageslice in os.listdir(path):

    extension = imageslice[(len(imageslice) - 3):(len(imageslice))]

    if ((extension == "bmp" or
        extension == "dip" or
        extension == "peg" or
        extension == "jpg" or
        extension == "jpe" or
        extension == "bmp" or
        extension == "jp2" or
        extension == "png" or
        extension == "pbm" or
        extension == "pgm" or
        extension == "ppm" or
        extension == ".sr" or
        extension == "ras" or
        extension == "iff" or
        extension == "tif") and
        math.sqrt(heightcount) >= valuecount):

        RGBslice = cv2.imread(path + imageslice)
        grayslice = cv2.cvtColor(RGBslice, cv2.COLOR_BGR2GRAY)

        if save == 0:
            while start == 0:

                t1 = cv2.getTrackbarPos('Threshold 1', 'Edge Preview')
                t2 = cv2.getTrackbarPos('Threshold 2', 'Edge Preview')
                start = cv2.getTrackbarPos('Start', 'Edge Preview')
                save = cv2.getTrackbarPos('Save Settings', 'Edge Preview')

                edgeslice = cv2.Canny(grayslice, t1, t2, apertureSize=5)

                cv2.imshow('Edge Preview', edgeslice)
                cv2.waitKey(200)

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
    cv2.setTrackbarPos('Start', 'Edge Preview', 0)
    start = 0

pointmesh.close()
