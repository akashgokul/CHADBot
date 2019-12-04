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

#Resources:
# https://answers.opencv.org/question/140096/change-colour-of-canny-output/
# https://stackoverflow.com/questions/51229126/how-to-find-the-red-color-regions-using-opencv
# Used https://www.pyimagesearch.com/2014/04/21/building-pokedex-python-finding-game-boy-screen-step-4-6/
# https://stackoverflow.com/questions/22588146/tracking-white-color-using-python-opencv
# https://www.geeksforgeeks.org/erosion-dilation-images-using-opencv-python/
# https://stackoverflow.com/questions/32669415/opencv-ordering-a-contours-by-area-python
# https://stackoverflow.com/questions/28759253/how-to-crop-the-internal-area-of-a-contour

# Filters red and white parts
def color_threshold(img):
	img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	mask1 = cv2.inRange(img_hsv, (0,50,20), (5,255,255))
	mask2 = cv2.inRange(img_hsv, (175,50,20), (180,255,255))
	lower_white = np.array([0,0,168])
	upper_white = np.array([230,240,255])
	mask3 = cv2.inRange(img_hsv,lower_white,upper_white)
	mask = cv2.bitwise_or(mask1,mask2)
	mask = cv2.bitwise_or(mask3,mask)
	output = cv2.bitwise_and(img,img,mask=mask)

	kernel = np.ones([3,3])
	img_erosion = cv2.erode(output,kernel,iterations=2)
	img_dilation = cv2.dilate(img_erosion,kernel,iterations=3)
	output = img_dilation

	cv2.imshow('threshold',output)
	cv2.waitKey(0)

	return output

def edge_detection(img):
	gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	blurred_img = cv2.bilateralFilter(gray_img,7,50,20)
	edges_of_img = cv2.Canny(blurred_img,00,100)

	cv2.imshow('img',edges_of_img)
	cv2.waitKey(0)
	return edges_of_img



#Finds rim of cup contour
def contour_detection(img):
	_, contours, hierachy = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
	cup_contour = [contours[i] for i in range(0,5)]
	return cup_contour

#Creates an image where pixel value is 0 (black) if not inside a cup rim
# O.w. the pixel value is white (255,255,255)
def binarize_img(img,contour_lst):
	blank_img = np.zeros_like(img)
	cv2.drawContours(blank_img, contour_lst, -1, (255,255,255))

	return blank_img



# Returns contours of rim of cups
def find_cup(img):
	filtered_img = color_threshold(img)
	edges_of_img = edge_detection(filtered_img)
	contours = contour_detection(edges_of_img)
	binary = binarize_img(img, contours)
	return binary


def main():
	img = cv2.imread("img2_Color.png")
	result = find_cup(img)
	cv2.imshow('img',result)
	cv2.waitKey(0)

main()
