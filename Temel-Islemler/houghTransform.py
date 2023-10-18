import cv2
import numpy as np

# once resmi gri tona cevirdik ve mevcut cizgilerin koselerini tespit etmek icin .Canny() fonksiyonunu kullandik
# ardindan cizgi tanima fonksiyonu .HoughLineP() fonksiyonu ile cizgileri birlestirdik
# for dongusunde de bu noktalari img ye yazdirdik

img = cv2.imread("../Images/h_line.png")

grayScale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(grayScale, 75, 150)
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=200)

for l in lines:
    x1, y1, x2, y2 = l[0]
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

cv2.imshow("Image", img)
cv2.imshow("Gray", grayScale)
cv2.imshow("Edges", edges)

cv2.waitKey(0)
cv2.destroyAllWindows()