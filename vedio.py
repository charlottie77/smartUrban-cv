import numpy as np
import cv2

cap = cv2.VideoCapture(0)
upper_red = np.array([10, 255, 255])
lower_red = np.array([0, 100, 100])


while(True):
	ret, frame = cap.read()

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	img2 = cv2.line(hsv,(200,0),(200,200),(0,0,0),5)
	img3 = cv2.line(img2,(400,0),(400,200),(0,0,0),5)

	mask = cv2.inRange(img3, lower_red, upper_red)


	cv2.imshow('frame', mask)
	cv2.imshow('original', img3)	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()