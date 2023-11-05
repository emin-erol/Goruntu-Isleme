# iki resim arasinda kizak kullanarak resimlerin yogunluklarini degistiriyoruz


import cv2

def nothing(x):
    pass


img1 = cv2.imread("klon.jpg")
img2 = cv2.imread("balls.jpg")

img1 = cv2.resize(img1, (640, 480))
img2 = cv2.resize(img2, (640, 480))

# iki resmi birlestiriyoruz
output = cv2.addWeighted(img1, 0.5, img2, 0.5, 0)

# pencere ve trackbar olusturuyoruz
windowName = "Image Transition"
cv2.namedWindow(windowName)

cv2.createTrackbar("Alpha-Beta", windowName, 0, 1000, nothing)

# her frame'i gosteriyoruz ve output degiskenini guncelliyoruz
while True:
    cv2.imshow(windowName, output)
    alpha = cv2.getTrackbarPos("Alpha-Beta", windowName) / 1000
    beta = 1 - alpha
    output = cv2.addWeighted(img1, alpha, img2, beta, 0)

    print(alpha, beta)

    if cv2.waitKey(1) == 27:
        break

cv2.waitKey(0)
cv2.destroyAllWindows()

