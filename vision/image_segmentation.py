#!/usr/bin/env python
"""Segmentation skeleton code for Lab 6
Course: EECS C106A, Fall 2019
Author: Grant Wang

This Python file is the skeleton code for Lab 3. You are expected to fill in
the body of the incomplete functions below to complete the lab. The 'test_..'
functions are already defined for you for allowing you to check your 
implementations.

When you believe you have completed implementations of all the incompeleted
functions, you can test your code by running python segmentation.py at the
command line and step through test images
"""

import os
import numpy as np
import cv2
import matplotlib.pyplot as plt

from scipy import ndimage
from scipy.signal import convolve
from scipy.ndimage.filters import gaussian_filter
from scipy.misc import imresize
from skimage import filters
from sklearn.cluster import KMeans

from skimage.measure import block_reduce
import time
import pdb

this_file = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = '/'.join(this_file.split('/')[:-2]) + '/img'

def read_image(img_name, grayscale=False):
    """ reads an image

    Parameters
    ----------
    img_name : str
        name of image
    grayscale : boolean
        true if image is in grayscale, false o/w
    
    Returns
    -------
    ndarray
        an array representing the image read (w/ extension)
    """

    if not grayscale:
        img = cv2.imread(img_name)
    else:
        img = cv2.imread(img_name, 0)

    return img

def write_image(img, img_name):
    """writes the image as a file
    
    Parameters
    ----------
    img : ndarray
        an array representing an image
    img_name : str
        name of file to write as (make sure to put extension)
    """

    cv2.imwrite(img_name, img)

def show_image(img_name, title='Fig', grayscale=False):
    """show the  as a matplotlib figure
    
    Parameters
    ----------
    img_name : str
        name of image
    tile : str
        title to give the figure shown
    grayscale : boolean
        true if image is in grayscale, false o/w
    """

    if not grayscale:
        plt.imshow(img_name)
        plt.title(title)
        plt.show()
    else:
        plt.imshow(img_name, cmap='gray')
        plt.title(title)
        plt.show()


def threshold_segment_naive(gray_img, lower_thresh, upper_thresh):
    """perform grayscale thresholding using a lower and upper threshold by
    blacking the background lying between the threholds and whitening the
    foreground

    Parameter
    ---------
    gray_img : ndarray
        grayscale image array
    lower_thresh : float or int
        lowerbound to threshold (an intensity value between 0-255)
    upper_thresh : float or int
        upperbound to threshold (an intensity value between 0-255)

    Returns
    -------
    ndarray
        thresholded version of gray_img
    """
    # TODO: Implement threshold segmentation by setting pixels of gray_img inside the 
    # lower_thresh and upper_thresh parameters to 0
    # Then set any value that is outside the range to be 1 
    # Hints: make a copy of gray_img so that we don't alter the original image
    # Boolean array indexing, or masking will come in handy. 
    # See https://docs.scipy.org/doc/numpy-1.13.0/user/basics.indexing.html

     #or gray_img >= upper_thresh)
    img = np.copy(gray_img)
    threshold_arr1 = img <= lower_thresh
    threshold_arr2 = img >=upper_thresh
    threshold_arr = np.logical_or(threshold_arr1,threshold_arr2)
    threshold_arr = threshold_arr.astype(np.int)
    return threshold_arr
    raise NotImplementedError()


def edge_detect_naive(gray_img):
    """perform edge detectionsegment_image using first two steps of Canny (Gaussian blurring and Sobel
    filtering)

    Parameter
    ---------
    gray_img : ndarray
        grayscale image array

    Returns
    -------
    ndarray
        gray_img with edges outlined
    """

    gray_s = gray_img.astype('int16') # convert to int16 for better img quality 
    # TODO: Blur gray_s using Gaussian blurring, convole the blurred image with
    # Sobel filters, and combine to compute the intensity gradient image (image with edges highlighted)
    # Hints: open-cv GaussianBlur will be helpful https://medium.com/analytics-vidhya/gaussian-blurring-with-python-and-opencv-ba8429eb879b 
    # the scipy.ndimage.filters class (imported already) has a useful convolve function

    # Steps
    # 1. apply a gaussian blur with a 5x5 kernel.
    # 2. define the convolution kernel Kx and Ky as defined in the doc.
    # 3. compute Gx and Gy by convolving Kx and Ky respectively with the blurred image.
    # 4. compute G = sqrt(Gx ** 2 + Gy ** 2)
    # 5. Return G
    blur = gaussian_filter(gray_s,5)
    K_x = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    K_y = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
    G_x = convolve(K_x,blur)
    G_y = convolve(K_y,blur)
    G_x_2 = np.square(G_x)
    G_y_2 = np.square(G_y)
    G = np.sqrt(G_x_2 + G_y_2)
    return G
    #raise NotImplementedError()

def edge_detect_canny(gray_img):
    """perform Canny edge detection

    Parameter
    ---------
    gray_img : ndarray
        grayscale image array

    Returns
    -------
    ndarray
        gray_img with edges outlined
    """

    edges = cv2.Canny(gray_img, 100, 200)

    return edges

def cluster_segment(img, n_clusters, random_state=0):
    """segment image using k_means clustering

    Parameter
    ---------
    img : ndarray
        rgb image array
    n_clusters : int
        the number of clusters to form as well as the number of centroids to generate
    random_state : int
        determines random number generation for centroid initialization

    Returns
    -------
    ndarray
        clusters of gray_img represented with similar pixel values
    """
    # Remove this line when you implement this function.
    #raise NotImplementedError()

    # Downsample img first using the mean to speed up K-means
    img_d = block_reduce(img, block_size=(3, 3, 1), func=np.mean)

    # TODO: Generate a clustered image using K-means

    # first convert our 3-dimensional img_d array to a 2-dimensional array
    # whose shape will be (length * width, number of channels) hint: use img_d.shape
    img_r_shape = (img_d.shape[0]*img_d.shape[1],img_d.shape[2])
    img_r = img_d.reshape(img_r_shape)    
    # fit the k-means algorithm on this reshaped array img_r using the
    # the scikit-learn k-means class and fit function
    # see https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
    # the only parameters you have to worry about are n_clusters and random_state
    kmeans = KMeans(n_clusters = n_clusters,random_state=random_state,max_iter=50).fit(img_r)

    # get the labeled cluster image using kmeans.labels_
    clusters = kmeans.labels_

    # reshape this clustered image to the original downsampled image (img_d) shape
    cluster_img = clusters.reshape(img_d.shape[0],img_d.shape[1])

    # Upsample the image back to the original image (img) using nearest interpolation
    img_u = imresize(cluster_img, (img.shape[0], img.shape[1]), interp='bilinear')

    return img_u.astype(np.uint8)

def to_grayscale(rgb_img):
    return np.dot(rgb_img[... , :3] , [0.299 , 0.587, 0.114])

def color_threshold(img):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 
      
    # Threshold of blue in HSV space 
    lower_blue = np.array([35, 140, 60]) 
    upper_blue = np.array([255, 255, 180]) 
  
    # preparing the mask to overlay 
    mask = cv2.inRange(hsv, lower_blue, upper_blue) 
      
    # The black region in the mask has the value of 0, 
    # so when multiplied with original image removes all non-blue regions 
    result = cv2.bitwise_and(img, img, mask = mask) 
  
    return result


def segment_image(img): 
    # ONLY USE ONE THRESHOLDING METHOD

    # perform thresholding segmentatio
    # binary = color_threshold(img)
    # binary = threshold_segment_naive(to_grayscale(img), 100, 200)#.astype(np.uint8)

    # perform clustering segmentation (make image binary)
    # binary = cluster_segment(img, 6)#.astype(np.uint8) / 255

    # binary = edge_detect_naive(to_grayscale(img))

    # if np.mean(binary) > 0.5:
    #     binary = 1 - binary #invert the pixels if K-Means assigned 1's to background, and 0's to foreground

    return binary

"""
below are tests used for sanity checking you image, edit as you see appropriate

"""

def test_thresh_naive(img, lower_thresh, upper_thresh):
    thresh = threshold_segment_naive(img, lower_thresh, upper_thresh)
    show_image(thresh, title='thresh naive', grayscale=True)
    cv2.imwrite(IMG_DIR + "/thresh.jpg", thresh.astype('uint8') * 255)

def test_edge_naive(img):
    edges = edge_detect_naive(img)
    show_image(edges, title='edge naive', grayscale=True)
    cv2.imwrite(IMG_DIR + "/edges.jpg", edges)

def test_edge_canny(img):
    edges = edge_detect_canny(img)
    show_image(edges, title='edge canny', grayscale=True)
    cv2.imwrite(IMG_DIR + "/edges_canny.jpg", edges)

def test_cluster(img, n_clusters):
    clusters = cluster_segment(img, n_clusters).astype(np.uint8)

    cv2.imwrite(IMG_DIR + "/cluster.jpg", clusters)
    clusters = cv2.imread(IMG_DIR + '/cluster.jpg')
    show_image(clusters, title='cluster')

def test_color_threshold(img):
    updated_img = color_threshold(img)
    cv2.imshow('test',updated_img)

# if __name__ == '__main__':
#     # adjust the file names here
#     test_img = read_image('cup_img_color.png')
#     #test_img_color = read_image(IMG_DIR + '/legos.jpg')

#     test_color_threshold(test)
#     # uncomment the test you want to run
#     # it will plot the image and also save it
#     #test_thresh_naive(test_img, 70, 200)
#     #test_edge_naive(test_img)
#     #test_edge_canny(test_img)
#     #test_cluster(test_img_color, 4)
def main():
    test_img = cv2.imread('cup_img_Color.png',1)
    #test_img_color = read_image(IMG_DIR + '/legos.jpg')

    # test_color_threshold(test_img)
    # uncomment the test you want to run
    # it will plot the image and also save it
    #test_thresh_naive(test_img, 70, 200)
    #test_edge_naive(test_img)
    #test_edge_canny(test_img)
    #test_cluster(test_img_color, 4)
main()