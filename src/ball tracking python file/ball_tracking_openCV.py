#!/usr/bin/env python

import cv2
import numpy as np


def convert_rgb_to_hsv(frame):
	hsv_video=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	return hsv_video

def color_filtering(hsv_video,yellowLower,yellowUpper):
	binary_mask=cv2.inRange(hsv_video,yellowLower,yellowUpper)
	return binary_mask

def getContours(binary_mask):
	_,contours,hierarchy=cv2.findContours(binary_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	return contours

def draw_ball_contour(binary_mask,frame,contours):
	black_video = np.zeros([binary_mask.shape[0], binary_mask.shape[1],3],'uint8')
	for c in contours:
		area=cv2.contourArea(c)
		((x,y),radius)=cv2.minEnclosingCircle(c)

		if area>900:
			cv2.drawContours(frame,[c],-1,(150,0,255),2)
			cx,cy=get_contour_centre(c)
			cv2.circle(frame,(cx,cy),(int)(radius),(0,0,255),1)
			cv2.circle(black_video, (cx,cy),(int)(radius),(0,0,255),1)
			cv2.circle(black_video, (cx,cy),5,(150,150,255),-1)
			print("Area: {}".format(area))
		cv2.imshow("RGB Contours",frame)
		cv2.imshow("Black Image Contours",black_video)
		

def get_contour_centre(c):
	M=cv2.moments(c)
	cx=-1
	cy=-1
	if (M['m00']!=0):
		cx=int(M['m10']/M['m00'])
		cy=int(M['m01']/M['m00'])
	return cx,cy

def main():
	video_name=cv2.VideoCapture("video/tennis-ball-video.mp4")

	while True:
		ret,frame=video_name.read()
		frame=cv2.resize(frame,(0,0),fx=0.5,fy=0.5)
		hsv_video=convert_rgb_to_hsv(frame)
		yellowLower=(30,10,10)
		yellowUpper=(60,255,255)
		binary_mask=color_filtering(hsv_video,yellowLower,yellowUpper)
		contours=getContours(binary_mask)
		draw_ball_contour(binary_mask,frame,contours)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	video_capture.release()
	cv2.destroyAllWindows

if __name__ == '__main__':
	main()