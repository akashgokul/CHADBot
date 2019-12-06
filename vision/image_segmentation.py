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
