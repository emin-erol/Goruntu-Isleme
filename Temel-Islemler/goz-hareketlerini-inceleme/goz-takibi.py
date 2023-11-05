import cv2

cap = cv2.VideoCapture("eye_motion.mp4")

while True:
    ret, frame = cap.read()
    roi = frame[80:210, 230:450]
    rows, cols, _ = roi.shape
    grayScale = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(grayScale, 0, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    (x, y, w, h) = cv2.boundingRect(contours[0])
    cv2.rectangle(roi, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.line(roi, (x+int(w/2), 0), (x+int(w/2), rows), (0, 0, 255), 2)
    cv2.line(roi, (0, y+int(h/2)), (cols, y+int(h/2)), (0, 0, 255), 2)

    cv2.imshow("Roi", roi)
    cv2.imshow("Threshold", thresh)
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()