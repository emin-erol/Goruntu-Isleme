import cv2
import numpy as np

def nothing(x):
    pass

canvas = np.zeros((512, 512, 3), dtype="uint8")
cv2.namedWindow("Image")
cv2.createTrackbar("R", "Image", 0, 255, nothing)
cv2.createTrackbar("G", "Image", 0, 255, nothing)
cv2.createTrackbar("B", "Image", 0, 255, nothing)
switch = "0: OFF - 1: ON"
cv2.createTrackbar(switch, "Image", 0, 1, nothing)

while True:
    cv2.imshow("Image", canvas)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    r = cv2.getTrackbarPos("R", "Image")
    g = cv2.getTrackbarPos("G", "Image")
    b = cv2.getTrackbarPos("B", "Image")
    s = cv2.getTrackbarPos(switch, "Image")
    if s == 0:
        canvas[:] = [0, 0, 0]
    else:
        canvas[:] = [b, g, r]

cv2.destroyAllWindows()



