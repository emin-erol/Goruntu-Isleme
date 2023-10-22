import cv2
import numpy as np

img_filter = cv2.imread("filter.png")
img_median = cv2.imread("median.png")
img_bilateral = cv2.imread("bilateral.png")

blur = cv2.blur(img_filter, (5, 5)) # (5,5) ifadesi blurlama miktarini gosterir daima pozitif tek sayi girilir
blur2 = cv2.GaussianBlur(img_filter, (5, 5), cv2.BORDER_DEFAULT)
blur_m = cv2.medianBlur(img_filter, 11)
blur_b = cv2.bilateralFilter(img_bilateral, 9, 65, 65)

cv2.imshow("Original", img_bilateral)
cv2.imshow("Bilateral Blur", blur_b)


cv2.waitKey(0)
cv2.destroyAllWindows()
