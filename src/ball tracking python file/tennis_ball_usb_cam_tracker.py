#!/usr/bin/env python

import rospy
import numpy as np
import cv2
import sys
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

bridge=CvBridge()

def image_callback(ros_image):
	global bridge

	try:
		cv_image=bridge.imgmsg_to_cv2(ros_image,"bgr8")
	except CvBridgeError as e:
		print(e)

	yellowLower=(30,10,10)
	yellowUpper=(60,255,255)

	hsv_video=cv2.cvtColor(cv_image,cv2.COLOR_BGR2HSV)
	binary_mask=cv2.inRange(hsv_video,yellowLower,yellowUpper)
	_,contours,hierarchy=cv2.findContours(binary_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

	for c in contours:
		area=cv2.contourArea(c)
		((x,y),radius)=cv2.minEnclosingCircle(c)

		if area>40000:
			cv2.drawContours(cv_image,[c],-1,(150,0,255),2)
			cx,cy=get_contour_centre(c)
			cv2.circle(cv_image,(cx,cy),(int)(radius),(0,0,255),1)
			print("Area: {}".format(area))
		cv2.imshow("RGB Contours",cv_image)
	cv2.waitKey(1)

def get_contour_centre(c):
	M=cv2.moments(c)
	cx=-1
	cy=-1
	if (M['m00']!=0):
		cx=int(M['m10']/M['m00'])
		cy=int(M['m01']/M['m00'])
	return cx,cy

def main(args):
	rospy.init_node('image_converter',anonymous=True)
	image_sub=rospy.Subscriber('usb_cam/image_raw',Image,image_callback)
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")
	cv2.destroyAllWindows()


if __name__ == '__main__':
	main(sys.argv)