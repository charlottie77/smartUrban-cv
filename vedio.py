import numpy as np
import cv2

cap = cv2.VideoCapture(0)
# red recognition threshold in hsv model
upper_red = np.array([10, 255, 255])
lower_red = np.array([0, 100, 100])
# gray threshold in gray space
gray_threshold = 127

# doc dictionary
dict_doc = {
    '0000': 'null',
    '0001': 'd3',
    '0010': 'null',
    '0011': 'd2',
    '0100': 'null',
    '0101': 'null',
    '0110': 'd1',
    '0111': 'null',
    '1000': 'null',
    '1001': 'null',
    '1010': 'null',
    '1011': 'null',
    '1100': 'null',
    '1101': 'null',
    "1110": 'null',
    "1111": 'null'
}

# camera run forever until press 'q' on the keyboard
while (True):
    ret, frame = cap.read()

# change the color space in to hsv
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
# draw the slider calibrate area
    img2 = cv2.line(hsv, (200, 0), (200, 500), (255, 255, 255), 5)
    img3 = cv2.line(img2, (400, 0), (400, 500), (255, 255, 255), 5)
# change the frame into gray image
    img_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
# draw the doc calibrate area
    img_doc = cv2.rectangle(img3, (500, 0), (600, 100), (255, 255, 255), 3)

# frame thresholding use simple thresholding
    _, threshold_doc = cv2.threshold(img_gray, gray_threshold, 255, cv2.THRESH_BINARY)
# define the area and the key points of doc recognition
    ROI_doc = threshold_doc[0:100, 500:600]
    px1 = ROI_doc[25, 25] // 255
    px2 = ROI_doc[75, 25] // 255
    px3 = ROI_doc[25, 75] // 255
    px4 = ROI_doc[75, 75] // 255
# transform the recognition result into string
    class_str = '%s%s%s%s' % (px1, px2, px3, px4)

# use mask to regonition the red area
    mask = cv2.inRange(img3, lower_red, upper_red)
# define the slider regonition area
    ROI_slider = mask[0:500, 250:350]
# loop to get the position of slider bar
# the range of loop should be change in case the calibrate area of slider has been changed
# calculate 3 rows once to be precise, the height of slider area minus 3 is the range
    for x in range(0, 497, 3):
        test = ROI_slider[x:x+3, 0:100]
        up = ROI_slider[x-3:x, 0:100]
        red_num = np.count_nonzero(test)
        black_num = np.count_nonzero(up)
        # recognition and print the result
        # the doc can be recognized only when slider has been recognized
        if red_num > 100 and black_num < 30:
            print('the position is ', x, 'the doc is ', dict_doc[class_str])
    # cv2.imshow('frame', mask)
    cv2.imshow('calib', img_doc)
    cv2.imshow('ROI', ROI_slider)
    # cv2.imshow('threshold', threshold_doc)
    cv2.imshow('doc-ROI', ROI_doc)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
