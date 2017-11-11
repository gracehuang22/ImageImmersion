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
    im = im.astype(np.uint8)
    return im


def energyFunction(image):
    im = cv2.imread( image )
    im = im.astype(np.uint8)
    img = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)

    dx = ndimage.sobel(img, 0)  # horizontal derivative
    dy = ndimage.sobel(img, 1)  # vertical derivative
    mag = np.hypot(dx, dy)  # magnitude
    mag *= 255.0 / np.max(mag)  # normalize (Q&D)

    posXDer = np.abs(dx)
    posYDer = np.abs(dy)
    energyFunction = posXDer + posYDer

    return energyFunction

def getNeighbors(accumulatedCost, currRow, currCol):
    #get topNeighbors if they are valid
    neighbors = []
    columns = len(accumulatedCost[0])
    # The value of the very top row (which obviously
    # has no rows above it) of the accumulated cost matrix is equal to the energy map.
    # Boundary conditions in this step are also taken into consideration.
    # If a neighboring pixel is not available due to the left or right edge,
    # it is simply not used in the minimum of top neighbors calculation.

    if (currRow-1 > 0 and currCol-1 > 0): #add topleft
        neighbors.append(accumulatedCost[currRow-1][currCol-1])
    if (currRow-1 > 0): #add top center
        neighbors.append(accumulatedCost[currRow-1][currCol])
    if (currRow-1 > 0 and currCol+1 < columns-1): #add topright
        neighbors.append(accumulatedCost[currRow-1][currCol+1])

    return neighbors

def findMinimumSeam(energyMap):
    rows = len(energyMap)
    columns = len(energyMap[0])
    minPath = []
    # First, an accumulated cost matrix must be constructed by starting at the
    # top edge and iterating through the rows of the energy map.
    accumulatedCost = [[0.0] * columns for i in range(rows)]
    for i in range(0,rows, 1):
        for j in range(0, columns, 1):

            neighbors = getNeighbors(accumulatedCost, i, j)

            if (len(neighbors) == 0):
                accumulatedCost[0][j] = energyMap[0][j]
                break;

            minOfNeighbors = min(neighbors)

            # The value of a pixel in the accumuluated cost matrix is equal to
            # its corresponding pixel value in the energy map added to the minimum of
            # its three top neighbors (top-left, top-center, and top-right) from the
            # accumulated cost matrix.
            accumulatedCost[i][j] = energyMap[i][j] + minOfNeighbors

    # The minimum seam is then calculated by backtracing from the bottom to the top edge.
    # First, the minimum value pixel in the bottom row of the accumulated cost matrix
    # is located. This is the bottom pixel of the minimum seam.
    # The seam is then traced back up to the top row of the accumulated cost matrix by following.
    # The minimum seam coordinates are recorded.
    minPath = []
    minBottomPixelX = np.argmin(accumulatedCost[rows-1])
    currMinX = minBottomPixelX
    minPath.append((currMinX,rows-1))

    for i in range(rows-2,-1,-1):
        minNeighbors = getNeighbors(accumulatedCost, i, currMinX)
        if (len(minNeighbors) == 0):
            minNeighbors.append(accumulatedCost[i][j])
            break
        #subtract 1 because can be left, mid, right. left = -1, mid = 0, right = 1
        currMinX = np.argmin(minNeighbors) - 1 + currMinX
        minPath.append((currMinX,i))
    return minPath

def highlightSeam(image, path):
    rows = len(path)
    highlightedEnergyMap = image
    print("highlightedEnergyMap 0,1", highlightedEnergyMap[0][1])

    for i in range(rows-1,-1, -1):
        highlightedEnergyMap[path[i][1]][path[i][0]] = [255, 0, 0]

    return highlightedEnergyMap

def deleteSeam(image, path):
    rows = len(image)
    columns = len(image[0])
    deleted = np.zeros((rows, columns-1, 3), dtype=np.uint8)

    for y in range(rows-1):
    	for x in range(columns-1):
            if (x,y) in path:
    	       deleted[y][x] = image[y][x+1]
            else:
               deleted[y][x] = image[y][x]

    return deleted

def main():
    imageFile = sys.argv[1]
    origImage = readImage(imageFile)
    for i in range(10):
        image = readImage(imageFile)
        energyMap = energyFunction(imageFile)
        returnPath = findMinimumSeam(energyMap)
        highlightedEnergyMap = highlightSeam(origImage, returnPath)
        highlightedImg = Image.fromarray(highlightedEnergyMap, 'RGB')
        highlightedImg.save('seam.jpg')

        deleted = deleteSeam(image, returnPath)
        img = Image.fromarray(deleted, 'RGB')
        img.save('deleted.png')
        #img.show()
        imageFile = 'deleted.png'



if __name__ == "__main__":
	main()