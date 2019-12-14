#!/usr/bin/env python
import rospy
import cv2
import os
from sensor_msgs.msg import Image
from hector_uav_msgs.srv import EnableMotors
from geometry_msgs.msg import Twist, Pose, PoseStamped
from cv_bridge import CvBridge, CvBridgeError
from keras.models import Sequential, load_model


def callback(data):
    moveBindings = {
        0: (1, 0, 0, 0),
        1: (1, 0, 0, -1),
        2: (0, 0, 0, 1),
        3: (0, 0, 0, -1),
        4: (1, 0, 0, 1),
        5: (-1, 0, 0, 0),
        6: (-1, 0, 0, 1),
        7: (-1, 0, 0, -1),
        8: (1, -1, 0, 0),
        9: (1, 0, 0, 0),
        10: (0, 1, 0, 0),
        11: (0, -1, 0, 0),
        12: (1, 1, 0, 0),
        13: (-1, 0, 0, 0),
        14: (-1, -1, 0, 0),
        15: (-1, 1, 0, 0),
        16: (0, 0, 1, 0),
        17: (0, 0, -1, 0),
    }
    h = data.height
    w = data.width
    cv_image = CvBridge().imgmsg_to_cv2(data, "bgr8")
    # temporal fix, check image is not corrupted
    if not (cv_image[h / 2, w / 2, 0] == 178 and cv_image[h / 2, w / 2, 1] == 178 and cv_image[
        h / 2, w / 2, 2] == 178):
        success = True
    else:
        pass
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    cv_image = cv2.resize(cv_image, (32, 32))
    state = cv_image.reshape(1, 1, cv_image.shape[0], cv_image.shape[1])
    model = load_model('/home/yari/Projects/catkin_ws/src/hector/model/turtle_c2c_dqn_ep100.h5')
    pred = model.predict(state)
    pred = pred.tolist()
    action = pred.index(max(pred))
    twist = Twist()
    twist.linear.x = moveBindings[action][0]
    twist.linear.y = moveBindings[action][1]
    twist.linear.z = moveBindings[action][2]
    twist.angular.z = moveBindings[action][3]
    cmd_pub.publish(twist)


def listener():

    rospy.Subscriber("/front_cam/camera/image", Image, callback)
    rospy.spin()


if __name__ == '__main__':
    bridge = CvBridge()
    rospy.init_node('navigator')
    rospy.wait_for_service('enable_motors')
    enable_motors = rospy.ServiceProxy('enable_motors', EnableMotors)
    resp = enable_motors(True)
    cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
    rospy.Subscriber("/front_cam/camera/image", Image, callback)
    rospy.spin()