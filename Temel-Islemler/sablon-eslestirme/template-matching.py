import cv2
import numpy as np

img = cv2.imread("klon.jpg")
temp = cv2.imread("klon-template.jpg")

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
tempGray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
w, h = tempGray.shape[::-1]  # aradigimiz parcanin cozunurlugunu aldik

# resmimizde template i ariyoruz eslestirmeye calisiyoruz ve sonucu result degiskenine atiyoruz
# benzerlik arttikca ilgili yerdeki piksel beyazlasir yani 1 e yaklasir o yuzden 1'e en yakin yerlerin konumunu alip location'a atiyoruz
result = cv2.matchTemplate(imgGray, tempGray, cv2.TM_CCOEFF_NORMED)
location = np.where(result >= 0.95)

# butun benzerlik olan noktalari dolasarak orada dikdortgen cizdiriyoruz ve tespiti saglamis oluyoruz
for p in zip(*location[::-1]):
    cv2.rectangle(img, p, (p[0] + w, p[1] + h), (0, 255, 0), 3)

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()


