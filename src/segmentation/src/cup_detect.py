import os
import numpy as np
import cv2
import matplotlib.pyplot as plt

from scipy import ndimage
from scipy.misc import imresize
from skimage import filters
from sklearn.cluster import KMeans

from scipy import stats

from skimage.measure import block_reduce


#Resources:
# https://answers.opencv.org/question/140096/change-colour-of-canny-output/
# https://stackoverflow.com/questions/51229126/how-to-find-the-red-color-regions-using-opencv
# Used https://www.pyimagesearch.com/2014/04/21/building-pokedex-python-finding-game-boy-screen-step-4-6/
# https://stackoverflow.com/questions/22588146/tracking-white-color-using-python-opencv
# https://www.geeksforgeeks.org/erosion-dilation-images-using-opencv-python/
# https://stackoverflow.com/questions/32669415/opencv-ordering-a-contours-by-area-python
# https://stackoverflow.com/questions/28759253/how-to-crop-the-internal-area-of-a-contour
#https://www.pyimagesearch.com/2016/02/01/opencv-center-of-contour/

#Refers to bounding box top_boundary extends downward, bottom_boundary extends upward, left_boundary ->, right_boundary <-
#as you increase these multipliers

top_boundary = 0
bottom_boundary = 0.3

left_boundary = 0.05
right_boundary = 0.9

def crop_img(img):
	"""
	Crops img according to parameters above (currently set to top left corner)
	"""
	height, width, channels = img.shape
	img_use = np.zeros(img.shape,np.uint8)
	width_lower = int(width*width_low)
	width_higher = int(width*width_high)
	height_lower = int(height*height_low)
	height_higher = int(height*height_high)

	img_portion = img[width_lower:width_higher,height_lower:height_higher]
	img_use[width_lower:width_higher,height_lower:height_higher] = img_portion
	# cv2.imshow('crop',img_use)
	# cv2.waitKey(0)
	return img_use


def color_threshold(img):
	"""
	Mask to filter only pixels whose colors are red or white (in our case corresponds to cup)
	"""
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
	img_erosion = cv2.erode(output,kernel,iterations=5)
	img_dilation = cv2.dilate(img_erosion,kernel,iterations=3)
	output = img_dilation

	# cv2.imshow('threshold',output)
	# cv2.waitKey(0)

	return output

def edge_detection(img):
	"""
	Returns Canny Edge Detection performed on input img
	"""
	gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	blurred_img = cv2.bilateralFilter(gray_img,7,50,20)
	edges_of_img = cv2.Canny(blurred_img,0,100)

	# cv2.imshow('img',edges_of_img)
	# cv2.waitKey(0)
	return edges_of_img



def contour_detection(img):
	"""
	Input: Img = output of Canny Edge Detector

	Output: Returns each contour and the center of the contour (if possible)
	"""
	_, contours, hierachy = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
	centers = []
	for cnt in contours:
		M = cv2.moments(cnt)
		if(len(centers)< 1):
			try:
				x = int(M["m10"] / M["m00"])
				y = int(M["m01"] / M["m00"])
				centers.append((x,y))
			except ZeroDivisionError:
				continue
	return contours,centers


def binarize_img(img,contour_lst,centers):
	"""
	Input: 	Image
			List of Contours
			List of Center position of each contour

	Outputs: bw_img = An image which is black everywhere except at the position of a center (where it is white)
			 screen_img = Image used for Baxter Screen, an image containing contours and center of contours
	"""
	bw_img = np.zeros_like(img)
	baxter_screen_img = np.zeros_like(img)
	cv2.drawContours(baxter_screen_img, contour_lst, -1, (255,255,255))
	for position in centers:
		cv2.circle(bw_img, position, 7, (255, 255, 255), -1)
		cv2.circle(baxter_screen_img, position,7,(0,0,255),-1)
	# cv2.imshow('binary',blank_img)
	# cv2.waitKey(0)
	return bw_img,baxter_screen_img

def drunken_blur(img,opp_score):
	"""
	Input: Image, opponent score (scalar)

	Adds random noise to image with variance being a linear function of opp_score

	Returns: Image with added random noise
	"""
    img_copy = img.copy()
    cv2.randn(img_copy,(0,0,0),(2*opp_score,3*opp_score,4*opp_score))
    return img + img_copy


def find_cup(img):
	"""
	Input: An image, img

	Finds the rims and center points of each cup

	Outputs:Binary = Black-White image containing only the centers of Contours
			Baxter_screen_img = Image containing contours and center of contours (for Baxter screen)
	"""
	cropped_img = crop_img(img)
	# cv2.imshow('cropped',cropped_img)
	# cv2.waitKey(0)
	filtered_img = color_threshold(cropped_img)
	edges_of_img = edge_detection(filtered_img)
	contours,centers = contour_detection(edges_of_img)
	binary, baxter_screen_img = binarize_img(img, contours,centers)
	# cv2.imshow('baxter',baxter_screen_img)
	# cv2.waitKey(10)
	return binary, baxter_screen_img

#
# def main():
# 	img = cv2.imread("img2_Color.png")
# 	cv2.imshow('original image',img)
# 	cv2.waitKey(0)
# 	result = find_cup(img)
# 	# result = color_threshold(result)
# 	cv2.imshow('color filtered',result)
# 	cv2.waitKey(0)
# 	return 0

	# # cv2.imshow('img',img_use)
	# result = circle_detection(img_use)
	# # find_cup(img)
	# cv2.imshow('img',result)
	# cv2.waitKey(0)
# 	#blackout_border(img)

# main()
