#!/usr/bin/env python
from std_msgs.msg import String
import rospy
from playerTime import PlayerTime

class Communicator:
    def __init__(self):
        self_game_sub = rospy.Subscriber('game_on', String, self.start_race)


    def start_race(self, msg):
        if msg == 'Start':
            execfile('stern4most_vision_11700197.py')
            execfile('stern4most_pilot_11700197.py')


rospy.init_node('communicator')
communicator = Communicator()
rospy.spin()