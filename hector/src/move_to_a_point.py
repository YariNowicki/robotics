#!/usr/bin/env python
from __future__ import print_function
import roslib
from hector_uav_msgs.srv import EnableMotors
roslib.load_manifest('teleop_twist_keyboard')
import rospy
from geometry_msgs.msg import Twist
import sys, select, termios, tty
import time



if __name__=="__main__":
    start_time = time.time()
    settings = termios.tcgetattr(sys.stdin)
    rospy.wait_for_service('enable_motors')
    enable_motors = rospy.ServiceProxy('enable_motors', EnableMotors)
    resp = enable_motors(True)
    pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
    rospy.init_node("move_one_line")
    speed = rospy.get_param("~speed", 1.0)
    turn = rospy.get_param("~turn", 1.0)
    x = 0
    y = 0
    z = 0
    th = 0
    status = 0

    try:
        while (1):

            x = 1
            #y = moveBindings[key][1]
            z = 0.5
            #th = moveBindings[key][3]
            #speed = speed * speedBindings[key][0]
            #turn = turn * speedBindings[key][1]
            elapsed_time = time.time() - start_time
            if elapsed_time < 5:
                twist = Twist()
                twist.linear.x = x * speed
                twist.linear.y = y * speed
                twist.linear.z = z * speed
                twist.angular.x = 0
                twist.angular.y = 0
                twist.angular.z = th * turn
                pub.publish(twist)
            elif elapsed_time < 10:
                twist = Twist()
                twist.linear.x = x * speed
                twist.linear.y = y * speed
                z = -0.5
                twist.linear.z = z * speed
                twist.angular.x = 0
                twist.angular.y = 0
                twist.angular.z = th * turn
                pub.publish(twist)
            else:
                print(elapsed_time)
                break

    except Exception as e:
        print(e)

    finally:
        twist = Twist()
        twist.linear.x = 0;
        twist.linear.y = 0;
        twist.linear.z = 0
        twist.angular.x = 0;
        twist.angular.y = 0;
        twist.angular.z = 0
        pub.publish(twist)

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)