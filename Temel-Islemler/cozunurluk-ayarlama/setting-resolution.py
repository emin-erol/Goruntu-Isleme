import cv2

cap = cv2.VideoCapture(0)

w = cap.get(3)  # genisligi aldik
h = cap.get(4)  # yuksekligi aldik

name = "Live Video"
cv2.namedWindow(name)

print("Width: ", w)
print("Height: ", h)

# genislik ve yukseklik degerlerini degistiriyoruz
cap.set(3, 640)
cap.set(4, 480)

# yeni degerleri konsolda gosteriyoruz
print("New Width: ", str(cap.get(3)))
print("New Height: ", str(cap.get(4)))

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    cv2.imshow(name, frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()



