import cv2
import numpy as np

# erode islemi resmi bozmaya yarar kernel matrisi oranında piksellerle bozar iterations ifadesi de
# resmin kac kere bozulacagini tutar
# dilate islemi resmi verilen kernel ve iterations miktarinca kalinlastirarak bozar
# morphologyEx resmin icindeki nesnenin disindaki veya icindeki gurultuyu temizlemeyi saglar
# morphologyEx MORPH_OPEN ile nesnenin disindaki gurultu temizlenir
# morphologyEx MORPH_CLOSE ile nesnenin icindeki gurultu temizlenir
# morphologyEx MORPH_GRADIENT ile nesnenin cevresi beyaz ici siyah hale getirilir

img = cv2.imread("klon.jpg", 0)
kernel = np.ones((5, 5), dtype="uint8")
erosion = cv2.erode(img, kernel, iterations=1)
dilation = cv2.dilate(img, kernel, iterations=1)
opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)

cv2.imshow("Image", img)
cv2.imshow("Image With Erosion", erosion)
cv2.imshow("Image With Dilation", dilation)
cv2.imshow("Image With Opening Morphology", opening)
cv2.imshow("Image With Closing Morphology", closing)
cv2.imshow("Image With Gradient Morphology", gradient)


cv2.waitKey(0)
cv2.destroyAllWindows()