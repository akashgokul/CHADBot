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

from cup_detect import *

from scipy import ndimage
from scipy.misc import imresize
from skimage import filters
from sklearn.cluster import KMeans

from skimage.measure import block_reduce
import time
import pdb



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
    copy_img = gray_img[:]
    copy_img[(copy_img < upper_thresh) & (copy_img > lower_thresh)] = 0
    copy_img[copy_img != 0] = 1
    return copy_img


def to_grayscale(rgb_img):
    return np.dot(rgb_img[... , :3] , [0.299 , 0.587, 0.114])

def segment_image(img):
    # ONLY USE ONE THRESHOLDING METHOD

    # perform thresholding segmentation
    # print(img[... , 0])
    # binary = find_cup(img)
    # binary = to_grayscale(binary).astype(np.uint8)
    binary, screen_img = find_cup(img)
    binary = threshold_segment_naive(binary[... , 2], 0, 200).astype(np.uint8)
    # 125, 256

    # perform clustering segmentation (make image binary)
    #binary = cluster_segment(img, 2).astype(np.uint8) / 255

    # binary = edge_detect_canny(to_grayscale(img)).astype(np.uint8)

    # binary = edge_detect_naive(to_grayscale(img)).astype(np.uint8)
    # if np.mean(binary) > 0.5:
    #     binary = 1 - binary #invert the pixels if K-Means assigned 1's to background, and 0's to foreground

    return binary, screen_img
