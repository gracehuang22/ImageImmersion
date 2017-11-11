import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')


import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread(sys.argv[1])

mask = np.zeros(img.shape[:2],np.uint8)

bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)

# rectIndex = sys.argv[2]
# rectPoints = rectIndex.split(",")
size = np.shape(img)

# for x in range(0, size[0]):
#     for y in range(0, size[1]):
    # print img[x,y]


locations = [(30,30), (size[0]/3-30, size[1]/3-30)]
pastimg = img
numZeros = np.count_nonzero(pastimg)
for position in locations:
    rectPoints = [position[0],position[1],size[0]/3*2,size[1]/3*2]
    rect = (int(rectPoints[0]),int(rectPoints[1]),int(rectPoints[2]),int(rectPoints[3]))
    cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
    print "%d" % (np.count_nonzero(img))
    if np.count_nonzero(img) > numZeros:
        pastimg = img
        print "yes"


img = pastimg
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask2[:,:,np.newaxis]

plt.imshow(img),plt.colorbar(),plt.show()
