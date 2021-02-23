import numpy as np
import cv2
from matplotlib import pyplot as plt

filename = '/home/lee/Pictures/bead15.png'

img = cv2.imread(filename, 0)
star = cv2.xfeatures2d.StarDetector_create()
brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()
kp = star.detect(img,None)
kp, des = brief.compute(img, kp)
img2 = cv2.drawKeypoints(img, kp, None, (255,0,0))
cv2.imshow('img2', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()