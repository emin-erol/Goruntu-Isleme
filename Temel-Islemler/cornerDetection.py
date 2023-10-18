import cv2
import numpy as np

img = cv2.imread("../Images/filter.png")

grayScale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
grayScale = np.float32(grayScale)

corners = cv2.goodFeaturesToTrack(grayScale, 30, 0.01, 5)
corners = np.int0(corners)

for corner in corners:
    x, y = corner.ravel()
    cv2.circle(img, (x, y), 5,(100, 100, 100), 2)

cv2.imshow("Corner Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

