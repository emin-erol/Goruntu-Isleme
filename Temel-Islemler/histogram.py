import cv2
import numpy as np
from matplotlib import pyplot as plt

# hist metodu ile resimdeki renklerin kullanim miktarini gosteren grafigi elde ederiz
# .ravel() ile iki boyutlu resmin en ve boyu carpilarak tek dizi elde edilir
# [0,256] ile renk kodu 0 ile 256 arasinda olan butun renkleri grafige dahil eder

img = cv2.imread("../Images/klon.jpg")
cv2.imshow("Image", img)
plt.hist(img.ravel(), 256, [0, 256])
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
