#!/usr/bin/env python
import rospy
from baxter_interface import gripper as robot_gripper
from std_msgs.msg import String
#from intera_interface import gripper as robot_gripper
OPEN_POS = 100
CLOSE_POS = 70
# print(right_gripper.valid_parameters_text())
# print(right_gripper.parameters())
# right_gripper.set_holding_force(15.0)
# print(right_gripper.parameters())

def calibrate(gripper):
	print('Calibrating...')
	return gripper.calibrate()

def open_grip(gripper):
	print('setting to position: ', OPEN_POS)
	return gripper.command_position(OPEN_POS)

def close_grip(gripper):
	print('setting to position: ', CLOSE_POS)
	return gripper.command_position(CLOSE_POS)

def callback(message):

    #Print the contents of the message to the console
    #print(message.data)
    if message.data == "open":
    	success = open_grip(right_gripper)
    elif message.data == "close":
    	success = close_grip(right_gripper)
    print(success)


#Define the method which contains the node's main functionality
def listener():

    #Create a new instance of the rospy.Subscriber object which we can 
    #use to receive messages of type std_msgs/String from the topic /chatter_talk.
    #Whenever a new message is received, the method callback() will be called
    #with the received message as its first argument.
    rospy.Subscriber("gripper", String, callback)

    #Wait for messages to arrive on the subscribed topics, and exit the node
    #when it is killed with Ctrl+C
    rospy.spin()

if __name__ == '__main__':
	rospy.init_node('gripper_test')
	right_gripper = robot_gripper.Gripper('right')
	calibrate(right_gripper)
	listener()