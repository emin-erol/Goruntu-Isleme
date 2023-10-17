import cv2

# bitwise_and: Iki resim arasında 've' operatoru kullanarak bit duzeyinde kesisim islemi uygular
# bitwise_or: Iki resim arasinda 'veya' operatoru kullanarak bit duzeyinde birlesim islemi uygular
# bitwise_xor: Karsilastirilan iki bit degeri ayniysa 0, degilse 1 degeri dondurur
# bitwise_not: Bit degerinin tersini uygular

img1 = cv2.imread("bitwise_1.png")
img2 = cv2.imread("bitwise_2.png")

bitwise_and = cv2.bitwise_and(img2, img1)
bitwise_or = cv2.bitwise_or(img2, img1)
bitwise_not1 = cv2.bitwise_not(img1)
bitwise_not2 = cv2.bitwise_not(img2)
bitwise_xor = cv2.bitwise_xor(img2, img1)


cv2.imshow("Image 1", img1)
cv2.imshow("Image 2", img2)
cv2.imshow("Bitwise And", bitwise_and)
cv2.imshow("Bitwise Or", bitwise_or)
cv2.imshow("Bitwise Not 1", bitwise_not1)
cv2.imshow("Bitwise Not 2", bitwise_not2)
cv2.imshow("Bitwise Xor", bitwise_xor)

cv2.waitKey(0)
cv2.destroyAllWindows()


