#!/usr/bin/env python
import rospy
from baxter_interface import gripper as robot_gripper
#from intera_interface import gripper as robot_gripper
from std_msgs.msg import String
import gripper_sub
import tf2_ros


def talker():

  #Create a tf buffer, which is primed with a tf listener
  tfBuffer = tf2_ros.Buffer()
  tfListener = tf2_ros.TransformListener(tfBuffer)

  #Run this program as a new node in the ROS computation graph 
  #called /talker.
  rospy.init_node('main_controller', anonymous=True)

  #Create an instance of the rospy.Publisher object which we can 
  #use to publish messages to a topic. 
  pub = rospy.Publisher('gripper', String, queue_size=10)
  

  # Loop until the node is killed with Ctrl-C
  while not rospy.is_shutdown():

    # Construct a string that we want to publish
    # (In Python, the "%" operator functions similarly
    #  to sprintf in C or MATLAB)
    pub_string = raw_input('Type [open] or [close]: ')
    
    # Publish our string to the 'chatter_talk' topic
    pub.publish(pub_string)
    
    rospy.sleep(1.0)
      
# This is Python's sytax for a main() method, which is run by default
# when exectued in the shell
if __name__ == '__main__':
  # Check if the node has received a signal to shut down
  # If not, run the talker method
  try:
    talker()
  except rospy.ROSInterruptException: pass