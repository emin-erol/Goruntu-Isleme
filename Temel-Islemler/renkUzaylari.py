import cv2

img = cv2.imread("../Images/klon.jpg")
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow("Klon BGR", img)
cv2.imshow("Klon RGB", img_rgb)
cv2.imshow("Klon HSV", img_hsv)
cv2.imshow("Klon GRAY", img_gray)

cv2.waitKey(0)
cv2.destroyAllWindows()
