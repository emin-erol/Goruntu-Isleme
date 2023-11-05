import numpy as np
import cv2

def findMaxContour(contourlar):
    max_i = 0
    maxArea = 0

    for i in range(len(contourlar)):
        faceArea = cv2.contourArea(contourlar[i])
        if faceArea > maxArea:
            maxArea = faceArea
            max_i = i

    try:
        cnt = contourlar[max_i]
    except:
        contourlar = [0]
        cnt = contours[0]

    return cnt


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (720, 480))

    roi = frame[50:350, 260:460]
    cv2.rectangle(frame, (260, 50), (460, 350), (0, 0, 255), 0)

    roiHSV = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    lowerColor = np.array([0, 15, 79], np.uint8)
    upperColor = np.array([65, 255, 255], np.uint8)

    mask = cv2.inRange(roiHSV, lowerColor, upperColor)
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)
    mask = cv2.medianBlur(mask, 15)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        try:
            c = findMaxContour(contours)

            extLeft = tuple(c[c[:, :, 0].argmin()][0])
            extRight = tuple(c[c[:, :, 0].argmax()][0])
            extTop = tuple(c[c[:, :, 1].argmin()][0])

            cv2.circle(roi, extLeft, 5, (0, 0, 255), -1)
            cv2.circle(roi, extRight, 5, (0, 0, 255), -1)
            cv2.circle(roi, extTop, 5, (0, 0, 255), -1)
        except:
            pass

    cv2.imshow("Frame", frame)
    cv2.imshow("Maskelenmis Yuz", mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

