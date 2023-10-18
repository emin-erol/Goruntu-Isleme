import cv2

# resimdeki ucgenin agirlik merkezini bulmak icin resmi once gray formata ve ardından binary formata cevirdik
# daha sonra ucgenin bulundugu alani konturladik ve icerisindeki degerleri .moments() metodu ile aldik
# son olarak da agirlik merkezi koordinatlarini bulduk ve resme ekledik

img = cv2.imread("contour.png")

grayScale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(grayScale, 127, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cnt = contours[0]
M = cv2.moments(cnt)

x = int(M["m10"] / M["m00"])
y = int(M["m01"] / M["m00"])

cv2.circle(img, (x, y), 5, (0, 0, 0), -1)

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

