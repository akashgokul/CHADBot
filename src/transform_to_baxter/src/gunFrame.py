#!/usr/bin/env python
#The line above tells Linux that this file is a Python script,
#and that the OS should use the Python interpreter in /usr/bin/env
#to run it. Don't forget to use "chmod +x [filename]" to make
#this script executable.

#Import the rospy package. For an import to work, it must be specified
#in both the package manifest AND the Python file in which it is used.
import rospy
import tf2_ros
import sys
import tf2_ros
import geometry_msgs.msg
# This is Python's sytax for a main() method, which is run by default
# when exectued in the shell
if __name__ == '__main__':
  
  # Check if the node has received a signal to shut down
  # If not, run the talker method

  #Run this program as a new node in the ROS computation graph 
  #called /turtlebot_controller.
  rospy.init_node('gun_frame', anonymous=True)
  br = tf2_ros.TransformBroadcaster()
  
  temp = geometry_msgs.msg.TransformStamped()
  temp.header.frame_id = "right_hand"
  temp.header.stamp = rospy.Time.now()
  temp.child_frame_id = "gun_frame"

  temp.transform.translation.x = 0
  temp.transform.translation.y = 0
  temp.transform.translation.z = 0

  temp.transform.rotation.x = 0
  temp.transform.rotation.y = 0
  temp.transform.rotation.z = 0
  temp.transform.rotation.w = 1

  try:

    # Create a timer object that will sleep long enough to result in
    # a 1Hz publishing rate
    r = rospy.Rate(1) # 1hz

    print("gun defined")
    # print ('Connected by', addr)
    # trans = tfBuffer.lookup_transform(origin_frame, goal_frames[i], rospy.Time())
    while not rospy.is_shutdown():
      br.sendTransform(temp)
      r.sleep()

    conn.close()
  except rospy.ROSInterruptException:
    pass