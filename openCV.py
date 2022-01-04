import time
import cv2
import numpy as np
import imutils
import pyautogui
from mss import mss

template = cv2.imread("crop.png")
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 50, 200)
(h, w) = template.shape[:2]

start_time = time.time()
mon = {'top': 430, 'left': 580, 'width': 150, 'height': 190}
with mss() as sct:
    while True:
        last_time = time.time()
        img = sct.grab(mon)
        img = np.array(img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 50, 200)
        
        found = None

        for scale in np.linspace(0.2, 1.0, 20)[::-1]:
            resized = imutils.resize(gray, width=int(gray.shape[1] * scale))
            r = gray.shape[1] / float(resized.shape[1])

            if resized.shape[0] < h or resized.shape[1] < w:
                break

            edged = cv2.Canny(resized, 50, 200)
            result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF_NORMED)
            (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
            
            print(maxVal)
            if maxVal > 0.5:
                if found is not None:
                    if maxVal > found[0]:
                        found = (maxVal, maxLoc, r)
                found = (maxVal, maxLoc, r)


        if found is not None:
            (_, maxLoc, r) = found
            (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
            (endX, endY) = (int((maxLoc[0] + w) * r), int((maxLoc[1] + h) * r))

            cv2.rectangle(img, (startX, startY), (endX, endY), (180, 105, 255), 2)
            pyautogui.moveTo( (startX + endX) / 2 + 580, (startY + endY) / 2 + 430, 0.1)
            pyautogui.click()
            pyautogui.click()
            exit
            found = None

        print('The loop took: {0}'.format(time.time()-last_time))
        cv2.imshow('test', np.array(img))

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
