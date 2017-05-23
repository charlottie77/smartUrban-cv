import numpy as np
import cv2

red_u = np.uint8([[[0,0,255]]])
#red_l = np.uint8([[[1,0,0]]])

hsv_red_u = cv2.cvtColor(red_u,cv2.COLOR_BGR2HSV)
#hsv_red_l = cv2.cvtColor(red_l,cv2.COLOR_BGR2HSV)

print(hsv_red_u,' - upper')
#print(hsv_red_l,' - lower')
