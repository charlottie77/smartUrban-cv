import numpy as np
import cv2
import asyncio
import json
import websockets



async def time(websocket, path):

    # while True:
    #     now = datetime.datetime.utcnow().isoformat() + 'Z'
    #     await websocket.send(now)
    #     await asyncio.sleep(0.1)

    cap = cv2.VideoCapture(1)
    # red recognition threshold in hsv model
    upper_red = np.array([10, 255, 255])
    lower_red = np.array([0, 100, 100])
    # gray threshold in gray space
    gray_threshold = 127
    slider_begin_x = 200
    slider_begin_y = 0
    slider_end_x = 250
    slider_end_y = 600

    slider_height = slider_end_y - slider_begin_y

    slider_reg_width = 50
    slider_reg_height = 600
    # slider_real_height = 0

    doc_begin_x = 300
    doc_begin_y = 0
    doc_end_x = 350
    doc_end_y = 50

    doc_reg = 50
    doc_1 = doc_reg // 4
    doc_3 = doc_reg // 4 * 3

    x_temp = 0

    # doc dictionary
    dict_doc = {
        '0000': 'null',
        '0001': 'null',
        '0010': 'null',
        '0011': 'null',
        '0100': 'null',
        '0101': 's1',
        '0110': 'null',
        '0111': 'null',
        '1000': 'null',
        '1001': '24h',
        '1010': 'null',
        '1011': 'null',
        '1100': 's2',
        '1101': 'null',
        "1110": 'null',
        "1111": 'null'
    }

    while (True):
        ret, frame = cap.read()

        # change the color space in to hsv
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # draw the slider calibrate area
        img2 = cv2.rectangle(hsv, (slider_begin_x, slider_begin_y), (slider_end_x, slider_end_y), (255, 255, 255), 1)
        # img2 = cv2.line(hsv, (200, 0), (200, 500), (255, 255, 255), 5)
        # img3 = cv2.line(img2, (400, 0), (400, 500), (255, 255, 255), 5)
        # change the frame into gray image
        img_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # draw the doc calibrate area
        img_doc = cv2.rectangle(img2, (doc_begin_x, doc_begin_y), (doc_end_x, doc_end_y), (255, 255, 255), 1)

        # frame thresholding use simple thresholding
        _, threshold_doc = cv2.threshold(img_gray, gray_threshold, 255, cv2.THRESH_BINARY)
        # define the area and the key points of doc recognition
        ROI_doc = threshold_doc[doc_begin_y:doc_end_y, doc_begin_x:doc_end_x]
        # ROI_doc = threshold_doc[0:100, 100:200]
        px1 = ROI_doc[doc_1, doc_1] // 255
        px2 = ROI_doc[doc_3, doc_1] // 255
        px3 = ROI_doc[doc_1, doc_3] // 255
        px4 = ROI_doc[doc_3, doc_3] // 255
        # transform the recognition result into string
        class_str = '%s%s%s%s' % (px1, px2, px3, px4)
        # print(class_str)

        # use mask to regonition the red area
        mask = cv2.inRange(img2, lower_red, upper_red)
        # define the slider regonition area
        ROI_slider = mask[0:slider_reg_height, slider_begin_x:slider_end_x]
        # loop to get the position of slider bar
        # the range of loop should be change in case the calibrate area of slider has been changed
        # calculate 3 rows once to be precise, the height of slider area minus 3 is the range
        for x in range(0, slider_height - 3, 3):
            test = ROI_slider[x:x + 3, 0:slider_reg_width]
            up = ROI_slider[x - 3:x, 0:slider_reg_width]
            red_num = np.count_nonzero(test)
            black_num = np.count_nonzero(up)
            # recognition and print the result
            # the doc can be recognized only when slider has been recognized
            # print(red_num)
            # print(black_num)
            if red_num > 100 and black_num < 30 and x_temp != x:
                # percentage
                xp = x / 300
                print('the position is ', xp, 'the doc is ', dict_doc[class_str])
                now = {'dock':dict_doc[class_str],'slider':xp}
                x_temp = x
                await websocket.send(json.dumps(now))
                # print(x / slider_real_height)

        # cv2.imshow('frame', mask)
        cv2.imshow('calib', img_doc)
        cv2.imshow('ROI', ROI_slider)
        # cv2.imshow('threshold', threshold_doc)
        cv2.imshow('doc-ROI', ROI_doc)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

start_server = websockets.serve(time, '192.168.1.74', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

# camera run forever until press 'q' on the keyboard


