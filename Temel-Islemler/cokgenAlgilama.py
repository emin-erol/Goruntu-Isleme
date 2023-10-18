import numpy as np
import cv2

font = cv2.FONT_HERSHEY_SIMPLEX
font1 = cv2.FONT_HERSHEY_COMPLEX

img = cv2.imread("../Images/polygons.png")
grayScale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(grayScale, 240, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    epsilon = 0.01 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    cv2.drawContours(img, [approx], 0, (0, 255, 0), 3)

    x = approx.ravel()[0]
    y = approx.ravel()[1]

    if len(approx) == 3:
        cv2.putText(img, "Triangle", (x, y), font1, 1, (0))

    elif len(approx) == 4:
        cv2.putText(img, "Rectangle", (x, y), font1, 1, (0))

    elif len(approx) == 5:
        cv2.putText(img, "Pentagon", (x, y), font1, 1, (0))

    elif len(approx) == 6:
        cv2.putText(img, "Hexagon", (x, y), font1, 1, (0))

    else:
        cv2.putText(img, "Ellipse", (x, y), font1, 1, (0))

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()


