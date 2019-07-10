#! /usr/bin/python3.5
import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
from time import sleep

class TimeLapse:
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
	
	def init_cam(self, width, height):
		self.cam = PiCamera()
		self.cam.resolution = (width, height)
		self.rawCapture = PiRGBArray(self.cam)
		
	def capture_image(self):
		self.cam.capture(self.rawCapture)

		return self.rawCapture.array
		
	def constructVideo(self):
		self.video = cv2.VideoWriter()
		
if __name__ == "__main__":
	tl = TimeLapse(300, 24, 600)
