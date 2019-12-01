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
	lower_red = np.array([0,120,70])
	upper_red = np.array([10,255,255])

	lower_red2 = np.array([170,120,70])
	upper_red2 = np.array([180,255,255])

	mask1 = cv2.inRange(hsv, lower_red, upper_red)
	mask2 = cv2.inRange(hsv,lower_red2,upper_red2)

	mask = mask1 + mask2 
	res = img.copy()
	res[np.where(mask==0)] = 0
	return res

def find_cup_rim(img):
	cup_contour = cv2.imread('cup_contour4_Color.png')
	cup = cv2.cvtColor(cup_contour,cv2.COLOR_BGR2GRAY)
	img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	ret1,thresh1 = cv2.threshold(cup,127,255,0)
	ret2,thresh2 = cv2.threshold(img_gray,127,255,0)
	_,contours,hierachy = cv2.findContours(thresh1, cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
	temp_contours = sorted(contours,key=cv2.contourArea,reverse=True)
	temp_contour = temp_contours[10]
	_,contours,hierarchy=cv2.findContours(thresh2,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(cup_contour,temp_contour,-1, (0,255,0),2)
	cv2.imshow('img',cup_contour)
	cv2.waitKey(0)
	for c in contours:
    #iterate through each contour in the target image and use cv2.matchShape to compare the contour shape
	    match=cv2.matchShapes(temp_contour,c,2,0.0)
	    print("match")
	    #if match value is less than 0.15
	    if match >= 0.5:
	        cv2.drawContours(img, [c], -1, (0,255,0),2)
	return img


def main():
	img = cv2.imread("img2_Color.png")
	# img_prime = img.reshape(img.shape[0]*img.shape[1],img.shape[2])
	# result1 = color_threshold(img)
	# gray_result1 = cv2.cvtColor(result1, cv2.COLOR_BGR2GRAY)
	# edges = cv2.Canny(gray_result1,200,255)
	# # kmeans = KMeans(n_clusters = 5,random_state=0).fit(img_prime)
	# # clusters = kmeans.cluster_centers_[kmeans.labels_]
	# # result = clusters.reshape(img.shape[0],img.shape[1],img.shape[2])
	result1 = color_threshold(img)
	result2 = find_cup_rim(result1)
	cv2.imshow('img',result1)
	cv2.waitKey(0)

main()