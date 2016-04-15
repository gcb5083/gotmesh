#!/usr/bin/env python

import cv2
import sys # so we can quit cleanly
from os import listdir
import os.path

### User variables for locations etc
outputfile = 'output.xyz'
source_image_dir = "./input/"
# initial guesses for UI
threshold_1_guess = 2000
threshold_2_guess = 2500


### Globals
legal_extensions = ["bmp", "dip", "peg", "jpg", "jpe", "jp2", "png", "pbm",
                    "pgm", "ppm", "sr", "ras", "iff", "tif"]


class Image_slice(object):
    " Hold image array and threshhold values for each image slice "
    def __init__(self, path, fname):
        self.label = fname
        self.image = cv2.imread(os.path.join(path, fname))
        self.t1 = None # intial guess for useful values
        self.t2 = None
        self.edges = [] # holds edge detection results
    def __repr__(self):
        return "<image %s thresh=(%d,%d)>" %(self.label, self.t1 or 0, self.t2 or 0)


def load_images(image_dir):
    """ Load in all valid image in directory.
        Turn all into Image_slice class
        - assume can be sorted by alpha
        - ignore unknown image types
    """
    images = []
    filenames = sorted(listdir(image_dir))
    print "Found", len(filenames),"files"
    for name in filenames:
        print "  Loading -",name
        fname, ext = os.path.splitext(name)
        if ext[1:] in legal_extensions: # ignore leading "."
            image = Image_slice(image_dir, name)
            if image:
                images.append(image)
    #
    print "Gathered", len(images), "legal images."
    return images


def nothing(*arg):
    " placeholder for unused side effect in cv2 sliders "
    pass


def new_slice(value):
    " got a new value from the slider for image to look at "
    global current
    current = value


def detect_edges(grayscale, t1, t2):
    """ do edge detection here so doing smarter edge detection in future is in one place
        - canny two thresholds
    """
    return cv2.Canny(grayscale, t1, t2, apertureSize=5)



###
if __name__ == "__main__":
    # if no directory dropped then look for dir at head of this file
    if len(sys.argv) > 1:
        dirpath = os.path.abspath(sys.argv[1])
    else:
        dirpath = source_image_dir
    images = load_images(dirpath)
    #
    current = 0 # current index into images to show
    last = -1
    prev_t1 = -1
    prev_t2 = -1
    images[0].t1 = threshold_1_guess
    images[0].t2 = threshold_2_guess
    # use openCV GUI approach
    cv2.namedWindow('Edge Preview',cv2.WINDOW_AUTOSIZE)
    cv2.createTrackbar('Image', 'Edge Preview', 0, len(images)-1, new_slice)
    cv2.createTrackbar('Threshold 1', 'Edge Preview', threshold_1_guess, 10000, nothing)
    cv2.createTrackbar('Threshold 2', 'Edge Preview', threshold_2_guess, 10000, nothing)
    #
    while(1):
        # check for quit
        k = cv2.waitKey(1) & 0xFF
        if k < 255 : # can check for "q" == chr(k) etc here...
            break
        # normal operation
        im = images[current]
        if current != last:
            print " looking at", current, images[current]
            last = current
            RGBslice = im.image
            grayslice = cv2.cvtColor(RGBslice, cv2.COLOR_BGR2GRAY)
            if im.t1:
                cv2.setTrackbarPos('Threshold 1', 'Edge Preview',im.t1)
            if im.t2:
                cv2.setTrackbarPos('Threshold 2', 'Edge Preview',im.t2)
            t1 = cv2.getTrackbarPos('Threshold 1', 'Edge Preview')
            t2 = cv2.getTrackbarPos('Threshold 2', 'Edge Preview')
            edgeslice = cv2.Canny(grayslice, t1, t2, apertureSize=5)
            im.edges = edgeslice
            cv2.imshow('Edge Preview', edgeslice)
        #
        t1 = cv2.getTrackbarPos('Threshold 1', 'Edge Preview')
        t2 = cv2.getTrackbarPos('Threshold 2', 'Edge Preview')
        # update thresholds if change
        if (t1 != prev_t1 or t2 != prev_t2):
            edgeslice = detect_edges(grayslice, t1, t2)
            im.edges = edgeslice
            cv2.imshow('Edge Preview', edgeslice)
        if t1 != prev_t1:
            prev_t1 = t1
            im.t1 = t1
        if t2 != prev_t2:
            prev_t2 = t2
            im.t2 = t2

    # Done editing - save
    print "Saving to XYZ format file",  outputfile
    pointmesh = open(outputfile, 'w')

    # write it out
    pointcount = 0
    linecount = 0
    layercount = 0
    #
    t1 = images[0].t1 # in case not looked at
    t2 = images[0].t2
    for im in images:
        print "  Saving", im.label, 
        edges = im.edges
        #print len(edges)
        # in case not looked at
        if len(edges) == 0:
            print "\n   No individual setting - (inheriting from prev)(%d,%d)" % (t1,t2)
            im.t1 = t1
            im.t2 = t2
            edges = detect_edges(cv2.cvtColor(im.image, cv2.COLOR_BGR2GRAY), im.t1, im.t2)
        else:
            if im.t1: t1 = im.t1
            if im.t2: t2 = im.t2
            print "(%d,%d)" % (t1, t2)

        for line in edges:
            for point in line:
                if point > 0:
                    pointmesh.write("%s\t%s\t%s\n" % (pointcount, linecount, layercount))
                pointcount += 1
            pointcount = 0
            linecount += 1
        linecount = 0
        layercount += 1
    pointmesh.close()
    # All over - clean up
    print "Closing down"
    cv2.destroyAllWindows()
    sys.exit()
