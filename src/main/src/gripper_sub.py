#!/usr/bin/env python
import rospy
from baxter_interface import gripper as robot_gripper
from std_msgs.msg import String
import math

import baxter_interface
import baxter_external_devices
from baxter_interface import CHECK_VERSION
import Projectile
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

def default_state(joint_state):
    RIGHT = baxter_interface.Limb('right')
    RJ = RIGHT.joint_names()

    joint_command = {}
    for i in range(0,len(joint_state)):
        joint_command[RJ[i]] = float(math.joint_state[i])
    # RIGHT.set_joint_positions(joint_command)
    RIGHT.move_to_joint_positions(joint_command,timeout = 1)

def aim_xy(end_coord, base_coord, cup_coord, joint_state):
    # calculate xy angle
    theta1 = Projectile.calc_xy(cup_coord, base_coord, end_coord)
    # go to xy coord with jointset
    # anlges = [theta1]+joint_state[1:]

    # joint_command = {}
    # for i in range(0,len(anlges)):
    #     joint_command[RJ[i]] = float(anlges[i])
    # RIGHT.set_joint_positions(joint_command)

    return theta1

def aim_z(end_coord, cup_coord):
    # calculate z angle
    h, d = Projectile.convertfrom3D(end_coord, cup_coord)
    theta2 = Projectile.projectile(h, d)

    # adjust to z angle jointset
    # anlges = joint_state[:-1]+[theta2]

    # joint_command = {}
    # for i in range(0,len(anlges)):
    #     joint_command[RJ[i]] = float(anlges[i])
    # RIGHT.set_joint_positions(joint_command)

    return theta2


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
    global RIGHT
    global RJ
    rospy.init_node('gripper_test')
    right_gripper = robot_gripper.Gripper('right')

    # left = baxter_interface.Limb('left')
    # lj = left.joint_names()

    calibrate(right_gripper)
    print("Calibrated!")
    listener()