import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')

import numpy as np
import cv2
import scipy
import math
from scipy import ndimage
from matplotlib import pyplot as plt
from PIL import Image


def readImage(image):
    im = cv2.imread( image )
    #im = im.astype(np.uint8)
    return im

def energyFunction(image):
    im = cv2.imread( image )

    im = im.astype(np.uint8)
    # print("im", im)
    img = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)

    print("img", img)

    dx = ndimage.sobel(img, 0)  # horizontal derivative
    dy = ndimage.sobel(img, 1)  # vertical derivative
    mag = np.hypot(dx, dy)  # magnitude
    mag *= 255.0 / np.max(mag)  # normalize (Q&D)

    posXDer = np.abs(dx)
    posYDer = np.abs(dy)
    energyFunction = posXDer + posYDer

    print("posXDer ", posXDer)
    print("posYDer", posYDer)

    return energyFunction


# Find minimum seam from top to bottom edge
def findMinimumSeam(energyMap):
    # First, an accumulated cost matrix must be constructed by starting at the
    # top edge and iterating through the rows of the energy map.
    # The value of a pixel in the accumuluated cost matrix is equal to
    # its corresponding pixel value in the energy map added to the minimum of
    # its three top neighbors (top-left, top-center, and top-right) from the
    # accumulated cost matrix. The value of the very top row (which obviously
    # has no rows above it) of the accumulated cost matrix is equal to the energy map.
    # Boundary conditions in this step are also taken into consideration.
    # If a neighboring pixel is not available due to the left or right edge,
    # it is simply not used in the minimum of top neighbors calculation.

    rows = len(energyMap)
    columns = len(energyMap[0])
    accumulatedCost = [[0.0] * columns for i in range(rows)]
    for i in range(rows-1,1, -1):
        columns = len(energyMap[i])
        for j in range(columns-1, 1, -1):
            #get topNeighbors if they are valid
            topNeighbors = []
            if (i-1 > 0): #top center
                topNeighbors.append(energyMap[i-1][j])
            if (i-1 > 0 and j-1 > 0): #topleft
                topNeighbors.append(energyMap[i-1][j-1])
            if (i-1 > 0 and j+1 < columns-1): #topright
                topNeighbors.append(energyMap[i-1][j+1])

            if len(topNeighbors) == 0 :
                break;

            minOfNeighbors = min(topNeighbors)

            print ("topNeighbors", topNeighbors)
            accumulatedCost[i][j] = energyMap[i][j] + minOfNeighbors
    #The minimum seam is then calculated by backtracing from the bottom to the top edge.
    #First, the minimum value pixel in the bottom row of the accumulated cost matrix
    #is located. This is the bottom pixel of the minimum seam.
    #The seam is then traced back up to the top row of the accumulated cost matrix by following.
    #The minimum seam coordinates are recorded.
    minPath = []

    for i in range(rows-1,1,-1):
        print ("accumulatedCost[i]", accumulatedCost[i])
        minOfBottomRow = min(i for i in accumulatedCost[i] if i > 0.0)
        print ("minOfBottomRow", minOfBottomRow)
        #print("accCost[i]", accumulatedCost[i])
        minValPixelX = accumulatedCost[i].index(minOfBottomRow)
        print ("minValPixelX", minValPixelX)
        minPath.append((minValPixelX,i))
        #print("x", minValPixelX)

    return minPath

def highlightSeam(image, path):
    rows = len(path)
    highlightedEnergyMap = image
    print("highlightedEnergyMap 0,1", highlightedEnergyMap[0][1])

    for i in range(rows-1,0, -1):
        highlightedEnergyMap[path[i][1]][path[i][0]] = [255, 0, 0]

    return highlightedEnergyMap

def deleteSeam(image, path):
    return image
    # rows = len(image)
    # columns = len(image[0])
    # path_set = set(path)
    # seen_set = set()
    # deleted  = [[0,0,0] * columns for i in range(rows)]
    #
    # for x in range(columns-1):
    # 	for y in range(rows-1):
    #         print("y,x", deleted[y][x])
    #         if (x,y) not in path_set and y not in seen_set:
    # 			deleted[y][x] = image[y][x]
    #         elif (x,y) in path_set:
    # 			seen_set.add(y)
    #         else:
    # 			deleted[y][x-1] = image[y][x]
    #
    # return deleted

def main():
    #mag = sobel(sys.argv[1])
    image = readImage(sys.argv[1])
    print ("image", image)
    energyMap = energyFunction(sys.argv[1])
    returnPath = findMinimumSeam(energyMap)
    highlightedEnergyMap = highlightSeam(image, returnPath)
    scipy.misc.imsave('seamCarving.jpg', energyMap)

    deleted = deleteSeam(image, returnPath)
    print( "deleted", deleted)
    scipy.misc.imsave('deleted.jpg', deleted)
    cv2.imshow('image',highlightedEnergyMap)

if __name__ == "__main__":
	main()
