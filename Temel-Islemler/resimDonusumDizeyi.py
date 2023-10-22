import cv2
import numpy as np

img = cv2.imread("klon.jpg", 0)
row, col = img.shape

M = np.float32([[1, 0, 50], [0, 1, 50]]) # x ve y eksenindeki kayma miktarlarini matris seklinde olusturduk
dst = cv2.warpAffine(img, M, (row, col)) # img yi M matrisi olceginde kaydirip dst'ye esitledik

cv2.imshow("Image", dst)
cv2.waitKey(0)
cv2.destroyAllWindows()