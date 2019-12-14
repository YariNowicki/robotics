#!/usr/bin/env python
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def callback(data):
    try:
        cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)
    cv2.imshow("Image window", cv_image)
    cv2.waitKey(3)


def listener():
     rospy.init_node('live_feed')
     rospy.Subscriber("/front_cam/camera/image", Image, callback)
     rospy.spin()


if __name__ == '__main__':
    bridge = CvBridge()
    listener()

