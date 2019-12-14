import rospy
from sensor_msgs.msg import LaserScan
from tf.msg import tfMessage
from nav_msgs.msg import MapMetaData, OccupancyGrid
from std_msgs.msg import Float64, String
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped


def get_sensor_data(data):
    pose = data.pose
    print("********************")
    print(str(pose.position.x) + "\t" + str(pose.position.y) + "\t" + str(pose.position.z))
    print("********************")


def listen():
     rospy.init_node('slam_receiver')
     rospy.Subscriber("/scan", LaserScan, get_sensor_data)
     rospy.spin()




if __name__ == '__main__':
    listen()