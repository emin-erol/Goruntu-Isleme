# Gerekli kutuphanelerin yuklenmesi
import numpy as np
import cv2
import imutils
from skimage.metrics import structural_similarity as compare_ssim

# resim dosyalarinin okunmasi
img1 = cv2.imread("../Images/city1.jpg")
img2 = cv2.imread("../Images/city2.jpg")

# resimlerin boyutlarinin duzenlenmesi
img1 = cv2.resize(img1, (640, 480))
img2 = cv2.resize(img2, (640, 480))
img_height = img1.shape[0]

# resimlerin gri formata gecirilmesi
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# compare_ssim algoritmasini kullanarak resimler arasindaki farkin bulunmasi
(score, diff) = compare_ssim(gray1, gray2, full=True)
diff = (diff * 255).astype("uint8")
print("SSIM: {}".format(score))

# fark goruntusunun esiklenmesi ve konturlarinin bulunmasi
thresh = cv2.threshold(diff, 150, 255, cv2.THRESH_BINARY_INV)[1]
contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)

# konturlarin merkezlerinin hesaplanmasi
centroids = []
for cnt in contours:
    M = cv2.moments(cnt)
    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        add_centroid = True
        for c in centroids:
            if np.linalg.norm(np.array([cx, cy]) - np.array(c)) < 30:
                add_centroid = False
        if add_centroid:
            centroids.append((cx, cy))

# merkezleri bulunan konturlarin cizilmesi
for c in centroids:
    cv2.circle(img1, c, 10, (0, 255, 0), 2)
    cv2.circle(img2, c, 10, (0, 255, 0), 2)

# gerekli gorsellerin ekranda gosterilmesi
cv2.imshow("Image 1", img1)
cv2.imshow("Image 2", img2)
cv2.imshow("Diff", diff)
cv2.imshow("Thresh", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

