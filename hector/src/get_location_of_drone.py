#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped, Pose, Point
from nav_msgs.msg import Odometry
from visualization_msgs.msg import Marker
from hector_uav_msgs.srv import EnableMotors


def callback(data):
    add_point = Point()
    add_point.x = data.pose.pose.position.x
    add_point.y = data.pose.pose.position.y
    add_point.z = data.pose.pose.position.z

    # Publish the Marker
    if not rospy.is_shutdown():
        if in_range(add_point):
            marker.points.append(add_point)
            marker_pub.publish(marker)

def listener():
    # rospy.Subscriber("/sensor_pose", PoseStamped, callback)
    rospy.Subscriber("/state", Odometry, callback)
    rospy.spin()

def in_range(point):
    if point.x < 0.5 and point.y < 0.5 and point.z < 0.5:
        return False
    return True


if __name__ == '__main__':
    rospy.init_node('location')
    marker_pub = rospy.Publisher('marker', Marker, queue_size=10)
    rospy.wait_for_service('enable_motors')
    enable_motors = rospy.ServiceProxy('enable_motors', EnableMotors)
    print("motors enabled")
    resp = enable_motors(True)
    shape = Marker.LINE_STRIP
    marker = Marker()
    marker.header.frame_id = "/nav"
    marker.header.stamp = rospy.get_rostime()

    # Set the namespace and id for this marker.This serves to create a unique ID
    # Any marker sent with the same namespace and id will overwrite the old one
    marker.ns = "basic_shapes"
    marker.id = 0
    marker.type = shape
    marker.action = Marker.ADD

    marker.pose.position.x = 0
    marker.pose.position.y = 0
    marker.pose.position.z = 0

    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0

    marker.scale.x = 0.1
    marker.color.r = 0.0
    marker.color.g = 1.0
    marker.color.b = 0.0
    marker.color.a = 1.0

    marker.lifetime = rospy.Duration()

    listener()
