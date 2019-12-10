#!/usr/bin/env python
"""
Path Planning Script for Lab 7
Author: Valmik Prabhu
"""
import sys

import rospy
import numpy as np
import traceback
import math

from sensor_msgs.msg import JointState

import baxter_interface

def main():
    right = baxter_interface.Limb('right')
    rj = right.joint_names()

    r = rospy.Rate(1)
    while not rospy.is_shutdown():
        for i in right.joint_angles():
            print(i,"{0:.2f}".format(
                math.degrees(round(right.joint_angles()[i],2))))
        # rospy.Subscriber("robot/joint_states", JointState, callback_1)
        # rospy.Subscriber("robot/joint_names", String, callback)
        # for i in joint_angles:
        #     print("{0:.2f}".format(round(i,2)))
        # # print(joint_angles)
        print("\n")
        r.sleep()


if __name__ == '__main__':
    rospy.init_node('joint_echo')
    main()
