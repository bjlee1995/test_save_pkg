import numpy as np
import cv2
from matplotlib import pyplot as plt

filename = '/home/lee/Pictures/bead15.png'
img = cv2.imread(filename,0)
fast = cv2.FastFeatureDetector_create()
kp = fast.detect(img,None)
img2=cv2.drawKeypoints(img,kp,None)
print("Threshold: ", fast.getThreshold())
print("nonmaxSuppression: ", fast.getNonmaxSuppression())
print("neighborhood: ", fast.getType())
print("Total Keypoints with nonmaxSuppression: ", len(kp))
cv2.imshow('img2', img2)
cv2.waitKey()
cv2.destroyAllWindows()

