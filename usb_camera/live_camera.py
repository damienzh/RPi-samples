import cv2
import time

cap = cv2.VideoCapture(0)
time.sleep(2)

while cap.isOpened():
	ret, frame = cap.read()
	cv2.imshow('camera', frame)
	key = cv2.waitKey(1)
	if key == ord('q'):
		break

cv2.destroyAllWindows()
cap.release()
