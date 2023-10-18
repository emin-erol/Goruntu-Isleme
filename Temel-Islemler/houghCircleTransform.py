import numpy as np
import cv2

img1 = cv2.imread("../Images/coins.jpg")
img2 = cv2.imread("../Images/balls.jpg")

grayScale1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
grayScale2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

imgBlur1 = cv2.medianBlur(grayScale1, 5)
imgBlur2 = cv2.medianBlur(grayScale2, 5)

circles1 = cv2.HoughCircles(imgBlur1, cv2.HOUGH_GRADIENT, 1, img1.shape[0]/16, param1=300, param2=10, minRadius=63, maxRadius=67)
circles2 = cv2.HoughCircles(imgBlur2, cv2.HOUGH_GRADIENT, 1, img1.shape[0]/50, param1=150, param2=10, minRadius=2, maxRadius=60)

if circles1 is not None:
    circles1 = np.uint16(np.around(circles1))
    for i in circles1[0,:]:
        cv2.circle(img1, (i[0], i[1]), i[2], (0, 255, 0), 2)

if circles2 is not None:
    circles2 = np.uint16(np.around(circles2))
    for j in circles2[0,:]:
        cv2.circle(img2, (j[0], j[1]), j[2], (0, 255, 0), 2)


#cv2.imshow("Image 1", img1)
cv2.imshow("Image 2", img2)

cv2.waitKey(0)
cv2.destroyAllWindows()