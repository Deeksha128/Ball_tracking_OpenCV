#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def chatter_callback(message):
	rospy.loginfo(rospy.get_caller_id() + "I heard %s", message.data)

def listener():
	rospy.Subscriber('chatter',String,chatter_callback)
	rospy.init_node('listener',anonymous=True)

	rospy.spin()

if __name__ == '__main__':
	listener()