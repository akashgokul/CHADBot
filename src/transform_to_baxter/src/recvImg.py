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
import socket
import pickle
import tf2_ros
# import geometry_msgs.msg
from sensor_msgs.msg import (
    Image,
)
      
# This is Python's sytax for a main() method, which is run by default
# when exectued in the shell
if __name__ == '__main__':
  pub = rospy.Publisher('/robot/xdisplay', Image, latch=True, queue_size=1)
  # Check if the node has received a signal to shut down
  # If not, run the talker method

  #Run this program as a new node in the ROS computation graph 
  #called /turtlebot_controller.
  rospy.init_node('recv_coords', anonymous=True)
  br = tf2_ros.TransformBroadcaster()

  try:

    # Create a timer object that will sleep long enough to result in
    # a 1Hz publishing rate
    r = rospy.Rate(1) # 1hz

    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = 50077              # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    print("waiting")
    s.listen(1)
    conn, addr = s.accept()
    message = ''
    # print ('Connected by', addr)
    # trans = tfBuffer.lookup_transform(origin_frame, goal_frames[i], rospy.Time())
    while not rospy.is_shutdown():
      data = conn.recv(1024)
      
      if not data:
        s.listen(1)
        conn, addr = s.accept()
        temp = pickle.loads(message)
        pub.publish(temp)
        message = ''
        # print("\n")
        continue

      message += data
      # print(data)
      # print("\n")
      r.sleep()

    conn.close()

  except rospy.ROSInterruptException:
    pass