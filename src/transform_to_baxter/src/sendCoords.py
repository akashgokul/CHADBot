#!/usr/bin/env python
#The line above tells Linux that this file is a Python script,
#and that the OS should use the Python interpreter in /usr/bin/env
#to run it. Don't forget to use "chmod +x [filename]" to make
#this script executable.

#Import the rospy package. For an import to work, it must be specified
#in both the package manifest AND the Python file in which it is used.
import rospy
import tf2_ros
import tf
import sys
import socket
import pickle
# from geometry_msgs.msg import Twist

#Define the method which contains the main functionality of the node.
def send(goal_frames, origin_frame = "ar_marker_8"):
  """
  Inputs:
  - origin_frame: the tf frame of the AR tag on your table
  - target_frames: the tf frame of the target cups
  """

  ################################### YOUR CODE HERE ##############

  #Create a tf buffer, which is primed with a tf listener
  tfBuffer = tf2_ros.Buffer()
  tfListener = tf2_ros.TransformListener(tfBuffer)
  
  # # Create a timer object that will sleep long enough to result in
  # # a 1Hz publishing rate
  r = rospy.Rate(10) # 10hz
  HOST = ''    # The remote host
  PORT = 50007       # The same port as used by the server
  # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # # # Loop until the node is killed with Ctrl-C
  # s.connect((HOST, PORT))
  while not rospy.is_shutdown():
    try:
      for i in range(0,len(goal_frames)):
        # print(type(origin_frame))
        # print(type(goal_frames))
        trans = tfBuffer.lookup_transform(origin_frame, goal_frames[i], rospy.Time())

        # parent = trans.header.frame_id
        # child = trans.child_frame_id
        # trans_x = trans.transform.translation.x
        # trans_y = trans.transform.translation.y
        # trans_z = trans.transform.translation.z
        # rot_x = trans.transform.rotation.x
        # rot_y = trans.transform.rotation.y
        # rot_z = trans.transform.rotation.z
        # rot_w = trans.transform.rotation.w

        # t = str([parent,child,
        # trans_x,trans_y,trans_z,
        # rot_x,rot_y,rot_z,rot_z])
        

        print(goal_frames[i])
        # print(t)
        print("\n")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.sendall(pickle.dumps(trans))
        # s.sendall(t)
        s.close()

    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
      print('nope')
      pass
    # Use our rate object to sleep until it is time to publish again
    # print("\n")
    r.sleep()
  # s.close()

      
# This is Python's sytax for a main() method, which is run by default
# when exectued in the shell
if __name__ == '__main__':
  # Check if the node has received a signal to shut down
  # If not, run the talker method

  #Run this program as a new node in the ROS computation graph 
  #called /send_coords.
  rospy.init_node('send_coords', anonymous=True)

  try:
  	# print(sys.argv[2])
    send(sys.argv[2:], sys.argv[1])
  except rospy.ROSInterruptException:
    pass