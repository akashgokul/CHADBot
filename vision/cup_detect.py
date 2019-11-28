import os
import numpy as np
import cv2
import matplotlib.pyplot as plt

from scipy import ndimage
from scipy.misc import imresize
from skimage import filters
from sklearn.cluster import KMeans

from skimage.measure import block_reduce
import time
import pdb

def color_threshold(img):
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	lower_red = np.array([0,155,84])
	upper_red = np.array([10,255,255])

	lower_red2 = np.array([161,155,84])
	upper_red2 = np.array([179,255,255])

	mask1 = cv2.inRange(hsv, lower_red, upper_red)
	mask2 = cv2.inRange(hsv,lower_red2,upper_red2)

	mask = mask1 + mask2 
	res = cv2.bitwise_and(img,img, mask= mask)

	return res

def main():
	img = cv2.imread("img1_Color.png",1)
	result1 = color_threshold(img)
	gray_result1 = cv2.cvtColor(result1, cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray_result1,100,150)
	cv2.imshow('edges',edges)
	cv2.waitKey(0)

main()