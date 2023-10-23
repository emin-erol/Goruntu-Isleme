import cv2

cap = cv2.VideoCapture("/Users/eminerol/PycharmProjects/pythonProject/videoOkuma/video.avi")

while True:
    ret, frame = cap.read()
    if ret == False:
        break
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Video", frame)
    if cv2.waitKey(40) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
