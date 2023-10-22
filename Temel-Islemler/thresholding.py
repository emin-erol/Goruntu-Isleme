import cv2

img = cv2.imread("klon.jpg", 0)

ret, th1 = cv2.threshold(img, 150, 200, cv2.THRESH_BINARY) # resme kabaca threshold uygular
th2 = cv2.adaptiveThreshold(img, 250, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2) # kenar kisimlari daha da netlestirerek bir threshld uygular
# yukaridaki 250 ifadesi goruntunun parlakligini ayarlar, 9 ifadesi siyah detay miktarini ayarlar, 2 ifadesi beyazlik miktarini ayarlar

th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 2)
# gaussian ile daha detayli bir sonuc alinir

cv2.imshow("Image", img)
cv2.imshow("th1", th1)
cv2.imshow("th2", th2)
cv2.imshow("th3", th3)

cv2.waitKey(0)
cv2.destroyAllWindows()