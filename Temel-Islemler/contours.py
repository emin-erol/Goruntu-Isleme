import cv2

# Resimdeki konturlari olusturabilmek icin once resmi gray formata cevirdik ardindan resmi binary formata cevirdik
# daha sonra .findContours() metodu ile binary formatindaki resmin konturlarini bulduk ve .drawContours metodu ile
# buldugumuz konturlari resmimize yazdirdik

img = cv2.imread("../Images/contour1.png")
grayScale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(grayScale, 127, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(img, contours, -1, (0, 0, 255), 5)
cv2.imshow("Contours", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

