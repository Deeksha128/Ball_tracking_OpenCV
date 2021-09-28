#!/usr/bin/env python

import cv2
import numpy as np
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


def video_publisher():
	bridge=CvBridge()
	rospy.init_node("Publisher",anonymous=True)
	pub=rospy.Publisher("tennis_ball_image",Image,queue_size=10)
	rate=rospy.Rate(10)


	video_capture=cv2.VideoCapture("video/tennis-ball-video.mp4")
	

	while not rospy.is_shutdown():
		ret,frame=video_capture.read()
		frame=cv2.resize(frame,(0,0),fx=0.5,fy=0.5)
		rospy.loginfo("Reading video")
		msg_frame=bridge.cv2_to_imgmsg(frame,"bgr8")
		pub.publish(msg_frame)

		rate.sleep()
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	video_capture.release()
	cv2.destroyAllWindows


if __name__ == '__main__':
	try:
		video_publisher()
	except rospy.ROSInterruptException:
		pass