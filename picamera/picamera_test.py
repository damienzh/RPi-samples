import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
from time import sleep

camera = PiCamera()
rawCapture = PiRGBArray(camera)
camera.resolution = (640, 480)

sleep(0.5)

camera.capture(rawCapture, format="bgr")
image = rawCapture.array

cv2.imshow("image", image)
cv2.waitKey(0)