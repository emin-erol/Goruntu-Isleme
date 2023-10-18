import cv2

img = cv2.imread("contour.png")

grayScale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(grayScale, 127, 255, cv2.THRESH_BINARY)
contour, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnt = contour[0]

area = cv2.contourArea(cnt) # .contourArea() fonksiyonu ile konturlari kullanarak alani bulduk
M = cv2.moments(cnt)
print(M["m00"]) # resmin degerlerini moments ile alip 'm00' degeri ile alanini bulduk
print(area)

perimeter = cv2.arcLength(cnt, True)
print(perimeter)



