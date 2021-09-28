#!/usr/bin/env python

import cv2
import numpy as np
import rospy
import sys
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

bridge=CvBridge()

def image_callback(frame):
	global bridge

	try:
		cv_image=bridge.imgmsg_to_cv2(frame)
	except CvBridgeError as e:
		print(e)

	yellowLower=(30,10,100)
	yellowUpper=(60,255,255)

	hsv_video=cv2.cvtColor(cv_image,cv2.COLOR_BGR2HSV)
	binary_mask=cv2.inRange(hsv_video,yellowLower,yellowUpper)
	_,contours,hierarchy=cv2.findContours(binary_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

	black_video = np.zeros([binary_mask.shape[0], binary_mask.shape[1],3],'uint8')
	for c in contours:
		area=cv2.contourArea(c)
		((x,y),radius)=cv2.minEnclosingCircle(c)

		if area>900:
			cv2.drawContours(cv_image,[c],-1,(150,0,255),2)
			cx,cy=get_contour_centre(c)
			cv2.circle(cv_image,(cx,cy),(int)(radius),(0,0,255),1)
			cv2.circle(black_video, (cx,cy),(int)(radius),(0,0,255),1)
			cv2.circle(black_video, (cx,cy),5,(150,150,255),-1)
			print("Area: {}".format(area))
		cv2.imshow("RGB Contours",cv_image)
		cv2.imshow("Black Image Contours",black_video)
	cv2.waitKey(1)

def get_contour_centre(c):
	M=cv2.moments(c)
	cx=-1
	cy=-1
	if (M['m00']!=0):
		cx=int(M['m10']/M['m00'])
		cy=int(M['m01']/M['m00'])
	return cx,cy

def video_subscriber():
	rospy.init_node('Subscriber',anonymous=True)
	rospy.Subscriber('tennis_ball_image',Image,image_callback)
	rospy.spin()
	
	cv2.destroyAllWindows()


if __name__ == '__main__':
	video_subscriber()