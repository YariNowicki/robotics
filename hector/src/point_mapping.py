#!/usr/bin/env python
import rospy
import struct
from std_msgs.msg import Header, ColorRGBA
from nav_msgs.msg import OccupancyGrid, MapMetaData
import sensor_msgs.point_cloud2 as pcl2
from sensor_msgs.msg import PointCloud2, PointField

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def point_cloud_xyzrgb(x, y, map_data, origin_x, origin_y, resolution):

    points = []
    lim_x = x
    lim_y = y
    for i in range(lim_x):
        for j in range(lim_y):
            x = translate(i,0,lim_x-1,origin_x,abs(origin_x)) #use float(i) or translate(i,0,lim_x-1,origin_x,abs(origin_x))
            y = translate(j,0,lim_x-1,origin_y,abs(origin_y)) #use float(j) or translate(j,0,lim_x-1,origin_y,abs(origin_y))
            z = 0
            pt = [x, y, z, 0]
            if map_data[i+ lim_x * j] == 0:
                r = 255
                g = 255
                b = 255
            elif map_data[i+ lim_x * j] == 100:
                r = 0
                g = 0
                b = 0
            else:
                r = 255
                g = 0
                b = 0

#           r = int(x * 255.0)
#           g = int(y * 255.0)
#           b = int(z * 255.0)
            a = 255
            rgb = struct.unpack('I', struct.pack('BBBB', b, g, r, a))[0]
            pt[3] = rgb
            points.append(pt)

    header = Header()
    header.stamp = rospy.Time.now()
    header.frame_id = 'map'
    fields = [PointField('x', 0, PointField.FLOAT32, 1),
          PointField('y', 4, PointField.FLOAT32, 1),
          PointField('z', 8, PointField.FLOAT32, 1),
          PointField('rgb', 12, PointField.UINT32, 1),
          # PointField('rgba', 12, PointField.UINT32, 1),
          ]
    point_cloud = pcl2.create_cloud(header, fields, points)
    point_cloud_map.publish(point_cloud)


def mapCB(data):
    map_header = data.header
    map_x = data.info.width
    map_y = data.info.height
    resolution = data.info.resolution
    origin_x = data.info.origin.position.x
    origin_y = data.info.origin.position.y
    map_data = data.data
    point_cloud_xyzrgb(map_x, map_y, map_data, origin_x, origin_y, resolution)

if __name__ == "__main__":

    rospy.init_node('PointCloud_Map_Generator')
    point_cloud_map = rospy.Publisher('point_cloud_map', PointCloud2, queue_size=10)
    raw_map = rospy.Subscriber("map", OccupancyGrid, mapCB)
    rate = rospy.Rate(10)

    try:
        while not rospy.is_shutdown():
            rate.sleep()

    except Exception as e:
        print(e)