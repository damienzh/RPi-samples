#! /usr/bin/python3.5
import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
from time import sleep

class TimeLapseVideo:
	def __init__(self, duration, fps, interval):
		"""
		:param duration: video duration in seconds
		:param fps: video fps
		:param internal: time between frames in seconds
		"""
		self.duration = duration 
		self.fps = fps
		self.frame_num = self.duration * self.fps
		self.interval = interval
		self.video_size = (640, 480)
		self.save_image = True
	
	def init_cam(self):
		self.cam = PiCamera()
		self.cam.resolution = (self.video_size[0], self.video_size[1])
		self.rawCapture = PiRGBArray(self.cam)
		print("initialize camera")
		
	def capture_image(self):
		self.cam.capture(self.rawCapture)

		return self.rawCapture.array
		
	def shooting(self, video_name):
		self.init_cam()
		fourcc = cv2.cv2.VideoWriter_fourcc('I', '4', '2', '0')
		self.video = cv2.VideoWriter(video_name, fourcc, self.fps, self.video_size)
		print("will capture {0} images for a {1} seconds video".format(self.frame_num, self.duration)
			  
		for i in range(self.frame_num):
			frame = self.capture_image()
			print("taken {} image".format(i))
			self.video.write(frame)
			if self.save_image:
			  	filename = "{:4}.png".format(i).replace(' ', '0')
			  	cv2.imwrite(filename, frame)
			sleep(self.interval)
			  
		print("finish shooting")
		self.video.release()
		self.cam.release()
		
if __name__ == "__main__":
	duration = 300
	fps = 24
	interval = 120
	tl = TimeLapseVideo(duration, fps, interval)
	tl.shooting('time_lapse.avi')
