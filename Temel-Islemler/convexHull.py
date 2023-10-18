import cv2
import numpy as np

# Orijinal resmimizi gri tona cevirip blur ile yumusatip threshold ile binary formata getirdik
# resmimizin konturlarini bulduk ve yeni resim icin arkaplanı siyah olan bir tuval hazirladik
# for ile butun contour'lari gezerek .convexHull() fonksiyonu ile dısbukey ortuyu hull'a attik
# ikinci for ile de once resmin konturlarini cizdik ardindan convexHull konturlarini cizdik

img = cv2.imread("../Images/map.jpg")
grayScale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.blur(grayScale, (3, 3))
ret, thresh = cv2.threshold(blur, 35, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
bg = np.zeros((thresh.shape[0], thresh.shape[1], 3), dtype="uint8")
hull = []

for i in range(len(contours)):
    hull.append(cv2.convexHull(contours[i], False))

for i in range(len(contours)):
    cv2.drawContours(bg, contours, i, (255, 0, 0), 3, 8, hierarchy)
    cv2.drawContours(bg, hull, i, (0, 255, 0), 1, 8)

cv2.imshow("Image", bg)
cv2.waitKey(0)
cv2.destroyAllWindows()



