import numpy as np
import cv2

cap = cv2.VideoCapture(0)
upper_red = np.array([10, 255, 255])
lower_red = np.array([0, 100, 100])

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


while (True):
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    img2 = cv2.line(hsv, (200, 0), (200, 500), (255, 255, 255), 5)
    img3 = cv2.line(img2, (400, 0), (400, 500), (255, 255, 255), 5)
    img_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    img_doc = cv2.rectangle(img_gray, (500, 0), (600, 100), (255, 255, 255), 3)

    mask = cv2.inRange(img3, lower_red, upper_red)
    ROI_slider = mask[0:500, 250:350]
    for x in range(0, 497, 3):
        test = ROI_slider[x:x+3, 0:100]
        up = ROI_slider[x-3:x, 0:100]
        red_num = np.count_nonzero(test)
        black_num = np.count_nonzero(up)
        # if red_num > 100 and black_num < 30:
            # print('the position is ', x)

    _, threshold_doc = cv2.threshold(img_doc, 127, 255, cv2.THRESH_BINARY)
    ROI_doc = threshold_doc[0:100, 500:600]
    px1 = ROI_doc[25, 25]//255
    px2 = ROI_doc[75, 25]//255
    px3 = ROI_doc[25, 75]//255
    px4 = ROI_doc[75, 75]//255
    class_str = '%s%s%s%s' % (px1, px2, px3, px4)
    print(dict_doc[class_str])
    # cv2.imshow('frame', mask)

    cv2.imshow('original', frame)
    cv2.imshow('ROI', ROI_slider)
    # cv2.imshow('threshold', threshold_doc)
    cv2.imshow('doc-ROI', ROI_doc)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
