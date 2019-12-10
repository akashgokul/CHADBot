#!/usr/bin/env python
"""Skeleton code for Lab 6
Course: EECS C106A, Fall 2019
Author: Amay Saxena

This file implements a ROS node that subscribes to topics for RGB images,
pointclouds, and camera calibration info, and uses the functions you
implemented to publish a segmented pointcloud to the topic /segmented_points.

Once you are confident in your implementation in image_segmentation.py and
pointcloud_segmentation.py, run this file to begin publishing a segmented
pointcloud.
"""

from __future__ import print_function
from collections import deque

import numpy as np
import rospy
import message_filters
import ros_numpy
import tf
import tf2_ros
import geometry_msgs.msg
from sensor_msgs import point_cloud2
from sensor_msgs.msg import Image, CameraInfo, PointCloud2, PointField
import numpy as np
import cv2
import socket
import pickle

from cv_bridge import CvBridge
import cv_bridge

from image_segmentation import segment_image
from pointcloud_segmentation import segment_pointcloud

HOST = ''    # The remote host
PORT = 50077


def get_camera_matrix(camera_info_msg):
    # TODO: Return the camera intrinsic matrix as a 3x3 numpy array
    # by retreiving information from the CameraInfo ROS message.
    # Hint: numpy.reshape may be useful here.
    K = np.array(camera_info_msg.K)
    K_final = K.reshape((3,3))
    return K_final

def isolate_object_of_interest(points, image, cam_matrix, trans, rot):
    segmented_image, screen_img = segment_image(image)
    points = segment_pointcloud(points, segmented_image, cam_matrix, trans, rot)
    return points,screen_img

def numpy_to_pc2_msg(points):
    return ros_numpy.msgify(PointCloud2, points, stamp=rospy.Time.now(),
        frame_id='camera_depth_optical_frame')

class PointcloudProcess:
    """
    Wraps the processing of a pointcloud from an input ros topic and publishing
    to another PointCloud2 topic.

    """
    def __init__(self, points_sub_topic,
                       image_sub_topic,
                       cam_info_topic,
                       points_pub_topic):

        self.num_steps = 0
        self._br = tf2_ros.TransformBroadcaster()
        self.messages = deque([], 5)
        self.pointcloud_frame = None
        points_sub = message_filters.Subscriber(points_sub_topic, PointCloud2)
        image_sub = message_filters.Subscriber(image_sub_topic, Image)
        caminfo_sub = message_filters.Subscriber(cam_info_topic, CameraInfo)

        self._bridge = CvBridge()
        self.listener = tf.TransformListener()

        self.points_pub = rospy.Publisher(points_pub_topic, PointCloud2, queue_size=10)
        self.image_pub = rospy.Publisher('segmented_image', Image, queue_size=10)

        ts = message_filters.ApproximateTimeSynchronizer([points_sub, image_sub, caminfo_sub],
                                                          10, 0.1, allow_headerless=True)
        ts.registerCallback(self.callback)

    def callback(self, points_msg, image, info):
        try:
            intrinsic_matrix = get_camera_matrix(info)
            rgb_image = ros_numpy.numpify(image)
            points = ros_numpy.numpify(points_msg)
        except Exception as e:
            rospy.logerr(e)
            return
        self.num_steps += 1
        self.messages.appendleft((points, rgb_image, intrinsic_matrix))

    def publish_once_from_queue(self):
        if self.messages:
            points, image, info = self.messages.pop()
            try:
                trans, rot = self.listener.lookupTransform(
                                                       '/camera_color_optical_frame',
                                                       '/camera_depth_optical_frame',
                                                       rospy.Time(0))
                rot = tf.transformations.quaternion_matrix(rot)[:3, :3]
            except (tf.LookupException,
                    tf.ConnectivityException,
                    tf.ExtrapolationException):
                return
            points, screen_img = isolate_object_of_interest(points, image, info,
                np.array(trans), np.array(rot))
            points_msg = numpy_to_pc2_msg(points)


            cv2.imshow('screen_img',screen_img)
            cv2.waitKey(5)
            # msg = cv_bridge.CvBridge().cv2_to_imgmsg(screen_img, encoding="bgr8")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            s.sendall(pickle.dumps(screen_img))
            s.close()


            x_seen = []
            y_seen = []
            z_seen = []
            for pt in point_cloud2.read_points(points_msg, skip_nans=True):
                curr_x = pt[0]
                curr_y = pt[1]
                curr_z = pt[2]

                x_seen.append(curr_x)
                y_seen.append(curr_y)
                z_seen.append(curr_z)
            if(len(x_seen) > 0 and len(y_seen) > 0 and len(z_seen) > 0):
                x_seen, y_seen, z_seen = np.array(x_seen), np.array(y_seen), np.array(z_seen)
                center_pt = [np.mean(x_seen),np.mean(y_seen),np.mean(z_seen)]

                temp = geometry_msgs.msg.TransformStamped()
                temp.header.frame_id = "camera_depth_optical_frame"
                temp.header.stamp = rospy.Time.now()
                temp.child_frame_id = "cup_center"

                temp.transform.translation.x = center_pt[0]
                temp.transform.translation.y = center_pt[1]
                temp.transform.translation.z = center_pt[2]

                temp.transform.rotation.x = 0
                temp.transform.rotation.y = 0
                temp.transform.rotation.z = 0
                temp.transform.rotation.w = 1
                # print(temp)
                self._br.sendTransform(temp)
                # sendCoords.send(cup_names)
                print("Published segmented pointcloud at timestamp:",
                       points_msg.header.stamp.secs)
    

def main():
    CAM_INFO_TOPIC = '/camera/color/camera_info'
    RGB_IMAGE_TOPIC = '/camera/color/image_raw'
    POINTS_TOPIC = '/camera/depth/color/points'
    POINTS_PUB_TOPIC = 'segmented_points'

    rospy.init_node('realsense_listener')
    process = PointcloudProcess(POINTS_TOPIC, RGB_IMAGE_TOPIC,
                                CAM_INFO_TOPIC, POINTS_PUB_TOPIC)
    r = rospy.Rate(1000)

    while not rospy.is_shutdown():
        process.publish_once_from_queue()
        r.sleep()

if __name__ == '__main__':
    main()
