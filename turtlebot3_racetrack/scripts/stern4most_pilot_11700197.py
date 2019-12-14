#!/usr/bin/env python
from geometry_msgs.msg import Twist
import rospy
from std_msgs.msg import Int16
import re


class Follower:
    def __init__(self):
        self.cmd_vel_pub = rospy.Publisher('player_one/cmd_vel', Twist, queue_size=1)
        self.err_sub = rospy.Subscriber('err', Int16, self.image_drive)
        self.twist = Twist()

    def image_drive(self, msg):

        self.twist.linear.x = 0.25
        self.twist.angular.z = -float(msg.data) / 100
        self.cmd_vel_pub.publish(self.twist)


rospy.init_node('follower')
follower = Follower()
rospy.spin()
