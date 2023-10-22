import cv2

img = cv2.imread("klon.jpg", 0)
row, col = img.shape

M = cv2.getRotationMatrix2D((col/2, row/2), 90, 1)
dst = cv2.warpAffine(img, M, (row, col))

cv2.imshow("Image", dst)
cv2.waitKey(0)
cv2.destroyAllWindows()