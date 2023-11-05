import cv2

img1 = cv2.imread("klon.jpg")
img2 = cv2.imread("klon1.jpg")

img1 = cv2.resize(img1, (640, 480))
img2 = cv2.resize(img2, (640, 480))

img3 = cv2.medianBlur(img1, 7)

# diff = cv2.subtract(img1, img2)
diff = cv2.subtract(img1, img3)
b, g, r = cv2.split(diff)

if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
    print("The images are completely same")
else:
    print("The images are not completely same")

cv2.imshow("Image 1", img1)
cv2.imshow("Image 2", img2)
cv2.imshow("Difference", diff)

cv2.waitKey(0)
cv2.destroyAllWindows()





