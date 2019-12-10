#!/usr/bin/env python
import sys
import time
import traceback
import rospy
from baxter_interface import gripper as robot_gripper
from std_msgs.msg import String
from sensor_msgs.msg import JointState
import gripper_sub
import tf2_ros
import math
from math import pi
import Projectile
from path_planner import PathPlanner
from baxter_interface import Limb
import numpy as np

OFFSET = 13

def talker(origin_frame):

  #Run this program as a new node in the ROS computation graph 
  #called /talker.
  rospy.init_node('main_controller', anonymous=True)

  #Create an instance of the rospy.Publisher object which we can 
  #use to publish messages to a topic. 
  pub = rospy.Publisher('gripper', String, queue_size=10)
  
  #Create a tf buffer, which is primed with a tf listener
  tfBuffer = tf2_ros.Buffer()
  tfListener = tf2_ros.TransformListener(tfBuffer)

  planner = PathPlanner("right_arm")
  right = Limb('right')
  # rj = right.joint_names()
  
  r = rospy.Rate(10)

  # Loop until the node is killed with Ctrl-C
  while not rospy.is_shutdown():
    try:
      pub_string = raw_input('Type [open] or [close]: ')
      # Publish our string to the 'chatter_talk' topic
      pub.publish(pub_string)
      while not rospy.is_shutdown():
        try:
          raw_input("Press <Enter> to move the right arm to goal pose 1: ")
          plan = planner.plan_to_joint_default()
          # print(plan)
          if not planner.execute_plan(plan):
            raise Exception("Execution failed")
          time.sleep(2)
        except Exception as e:
          print e
          traceback.print_exc()
        else:
          break

      trans_to_wrist = tfBuffer.lookup_transform(origin_frame, "right_hand", rospy.Time())
      # trans_to_tip = tfBuffer.lookup_transform(origin_frame, "right_gripper", rospy.Time())
      trans_to_base = tfBuffer.lookup_transform(origin_frame, "right_lower_shoulder", rospy.Time())
      trans_to_cup = tfBuffer.lookup_transform(origin_frame, "cup_center", rospy.Time())
      gun = [0,0,0]
      base = [0,0,0]
      goal = [0,0,0]
      # gun[0] = (trans_to_wrist.transform.translation.x+trans_to_tip.transform.translation.x)/2
      # gun[1] = (trans_to_wrist.transform.translation.y+trans_to_tip.transform.translation.y)/2
      # gun[2] = (trans_to_wrist.transform.translation.z+trans_to_tip.transform.translation.z)/2
      gun[0] = trans_to_wrist.transform.translation.x
      gun[1] = trans_to_wrist.transform.translation.y
      gun[2] = trans_to_wrist.transform.translation.z

      base[0] = trans_to_base.transform.translation.x
      base[1] = trans_to_base.transform.translation.y
      base[2] = trans_to_base.transform.translation.z

      goal[0] = trans_to_cup.transform.translation.x
      goal[1] = trans_to_cup.transform.translation.y
      # height of cup
      goal[2] = 0.12065/2
      
      theta1 = Projectile.calc_xy(goal, base, gun)
      print("theta1 = "+str(theta1))

      while not rospy.is_shutdown():
        try:
          raw_input("Press <Enter> to move the right arm to theta1: ")
          goal_joints = right.joint_angles()
          goal_joints["right_s0"] += np.radians(theta1)
          plan = planner.plan_to_joint(goal_joints)
          
          if not planner.execute_plan(plan):
            raise Exception("Execution failed")
          time.sleep(2)
        except Exception as e:
          print e
          traceback.print_exc()
        else:
          break
      trans_to_wrist = tfBuffer.lookup_transform(origin_frame, "right_hand", rospy.Time())
      # trans_to_tip = tfBuffer.lookup_transform(origin_frame, "right_gripper", rospy.Time())
      # gun[0] = (trans_to_wrist.transform.translation.x+trans_to_tip.transform.translation.x)/2
      # gun[1] = (trans_to_wrist.transform.translation.y+trans_to_tip.transform.translation.y)/2
      # gun[2] = (trans_to_wrist.transform.translation.z+trans_to_tip.transform.translation.z)/2
      gun[0] = trans_to_wrist.transform.translation.x
      gun[1] = trans_to_wrist.transform.translation.y
      gun[2] = trans_to_wrist.transform.translation.z

      theta2 = gripper_sub.aim_z(gun,goal)
      print("theta2 = "+str(np.degrees(theta2)))

      while not rospy.is_shutdown():
        try:
          raw_input("Press <Enter> to move the right arm to theta2: ")
          goal_joints = right.joint_angles()
          goal_joints["right_w2"] = pi/2-theta2 + np.radians(OFFSET)
          plan = planner.plan_to_joint(goal_joints)
          
          if not planner.execute_plan(plan):
            raise Exception("Execution failed")
          time.sleep(2)
        except Exception as e:
          print e
          traceback.print_exc()
        else:
          break
    #   Construct a string that we want to publish
    # (In Python, the "%" operator functions similarly
    #  to sprintf in C or MATLAB)
      pub_string = raw_input('Type [open] or [close]: ')
    # Publish our string to the 'chatter_talk' topic
      pub.publish(pub_string)

      # print(np.degrees(joint_angles))
      # print(delta)
      # if np.amax(error) >= .1:
      #   print("go")
        # gripper_sub.default_state(JOINT_DEFAULT)

    # aim_xy(end_coord, base_coord, cup_coord, joint_state)

    
    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
      print('loading')
      pass
    r.sleep()
      
# This is Python's sytax for a main() method, which is run by default
# when exectued in the shell
if __name__ == '__main__':
  # Check if the node has received a signal to shut down
  # If not, run the talker method
  try:
    # rospy.init_node('shoot_once', anonymous=True)
    talker(sys.argv[1])
  except rospy.ROSInterruptException: pass
