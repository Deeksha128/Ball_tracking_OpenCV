#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def talk():
	pub = rospy.Publisher('chatter',String,queue_size=10)
	rospy.init_node('talker',anonymous=True)
	rate=rospy.Rate(1)

	i=0
	while not rospy.is_shutdown():
		hello_str= "Hello World %s" %i
		rospy.loginfo(hello_str)
		pub.publish(hello_str)
		rate.sleep()
		i=i+1


if __name__=='__main__':
	try:
		talk()
	except rospy.ROSInterruptException:
		pass