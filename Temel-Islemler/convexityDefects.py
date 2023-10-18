import cv2

img = cv2.imread("../Images/star.png")
grayScale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(grayScale, 127, 255, 0)
contours, _ = cv2.findContours(thresh, 2, 1)
cnt = contours[0]

hull = cv2.convexHull(cnt, returnPoints=False)
defects = cv2.convexityDefects(cnt, hull)

for i in range(defects.shape[0]):
    s, e, f, d = defects[i, 0]
    start = tuple(cnt[s][0])
    end = tuple(cnt[e][0])
    far = tuple(cnt[f][0])
    cv2.line(img, start, end, (0, 255, 0), 2)
    cv2.circle(img, far, 5, (0, 255, 0), -1)

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
