#!/usr/bin/env python
from geometry_msgs.msg import Twist
import rospy
from std_msgs.msg import Int16, Bool


class Follower:
    def __init__(self):
        self.can_start = True
        rospy.loginfo('Put can_start to true')
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        rospy.loginfo('rospy.Publisher(cmd_vel, Twist, queue_size=1)')
        self.start_pilot = rospy.Subscriber('pilot', Bool, self.can_start_pilot)
        rospy.loginfo('rospy.Subscriber(pilot, Bool, self.can_start_pilot)')
        self.twist = Twist()
        for i in range(10):
            self.twist.linear.z = 2.37
            self.twist.linear.x = 1
            self.cmd_vel_pub.publish(self.twist)
            rospy.loginfo('Linear : ' + str(self.twist.linear.x))
            rospy.loginfo('Angular : ' + str(self.twist.angular.z))
            rospy.loginfo('\n')

    def image_drive(self, msg):
        if self.can_start:
            self.twist.linear.z = 5
            self.twist.linear.x = 2
            self.cmd_vel_pub.publish(self.twist)
            rospy.loginfo('Linear : ' + str(self.twist.linear.x))
            rospy.loginfo('Linear z : ' + str(self.twist.linear.z))
            rospy.loginfo('\n')
        else:
            rospy.loginfo('Cannot start')
            self.twist.linear.x = 0

    def can_start_pilot(self, msg):
        rospy.loginfo('Pilot can start')
        self.can_start = msg.data


rospy.init_node('follower')
follower = Follower()
rospy.spin()