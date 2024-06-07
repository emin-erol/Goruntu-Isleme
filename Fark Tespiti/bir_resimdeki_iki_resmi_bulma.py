import cv2
import numpy as np

# resim okuma
img = cv2.imread("../Images/hayvanlar.jpg")
imgArea = img.shape[0] * img.shape[1]

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# resimde gurultu azaltma"
filteredImg = cv2.bilateralFilter(imgGray, 5, 75, 75)

thresh = cv2.threshold(filteredImg, 230, 255, cv2.THRESH_BINARY_INV)[1]
contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
# contours = sorted(contours, key=cv2.contourArea, reverse=True)
t_min = 0.2 * imgArea
t_max = 0.5 * imgArea

filteredContours = [cnt for cnt in contours if t_min < cv2.contourArea(cnt) < t_max]

x1, y1, w1, h1 = cv2.boundingRect(filteredContours[0])
frame1 = img[y1:y1+h1, x1:x1+w1]
x2, y2, w2, h2 = cv2.boundingRect(filteredContours[1])
frame2 = img[y2:y2+h2, x2:x2+w2]

cv2.imshow("Frame 1", frame1)
cv2.imshow("Frame 2", frame2)
cv2.imshow("Eşikleme",thresh)
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

