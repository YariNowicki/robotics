#!/usr/bin/env python
import rospy
from geometry_msgs.msg import TwistStamped
from geometry_msgs.msg import Vector3
from std_msgs.msg import String


def pilot():
    pub = rospy.Publisher('/command/twist', TwistStamped, queue_size=10)
    rospy.init_node('pilot')
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        t = TwistStamped()
        t.twist.linear.z = 10
        t.twist.linear.x = 4
        t.twist.angular.z = 5
        print('publish')
        pub.publish(t)
        rate.sleep()


if __name__ == '__main__':
    pilot()