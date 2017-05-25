import numpy as np
import cv2

red_u = np.uint8([[[0, 0, 255]]])
black = np.uint8([[[0, 0, 0]]])
white = np.uint8([[[255, 255, 255]]])

hsv_red_u = cv2.cvtColor(red_u, cv2.COLOR_BGR2HSV)
hsv_black = cv2.cvtColor(black, cv2.COLOR_BGR2HSV)
hsv_white = cv2.cvtColor(white, cv2.COLOR_BGR2HSV)

print(hsv_red_u, ' - red')
print(hsv_black, ' - black')
print(hsv_white, ' - white')

