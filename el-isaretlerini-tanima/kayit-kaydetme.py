# projeye el isareti ornegi eklemek icin kullanilir

import numpy as np
import cv2

cap = cv2.VideoCapture(0)
kernel = np.ones((9, 9), np.uint8)
sekil = "bes"

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (740, 480))

    kesilmisFrame = frame[0:300, 450:740]
    kesilmisFrameHSV = cv2.cvtColor(kesilmisFrame, cv2.COLOR_BGR2HSV)

    lower_color = np.array([0, 60, 50])
    upper_color = np.array([90, 255, 255])
    filtreliFrame = cv2.inRange(kesilmisFrameHSV, lower_color, upper_color)
    filtreliFrame = cv2.morphologyEx(filtreliFrame, cv2.MORPH_CLOSE, kernel)

    cnt, hierarchy = cv2.findContours(filtreliFrame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnt = sorted(cnt, key=cv2.contourArea, reverse=True)[:10]
    contours = kesilmisFrame.copy()
    elResmi = 0
    if len(cnt) > 0:
        x, y, w, h = cv2.boundingRect(cnt[0])
        cv2.rectangle(contours, (x, y), (x+w, y+h), (0, 255, 0), 3)
        elResmi = filtreliFrame[y:y+h, x:x+w]
        cv2.imshow("El Resmi", elResmi)

    cv2.imshow("Kesilmis Frame", filtreliFrame)
    cv2.imshow("Contours", contours)
    if cv2.waitKey(1) == 27:
        break

cv2.imwrite("veriler/"+sekil+".jpg", elResmi)

cap.release()
cv2.destroyAllWindows()



