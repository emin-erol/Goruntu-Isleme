import cv2

videom = cv2.VideoCapture('SecurityCam.mp4')

ret, frame1 = videom.read()
ret, frame2 = videom.read()

while (videom.isOpened()):
    fark = cv2.absdiff(frame1, frame2)
    gri = cv2.cvtColor(fark, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gri, (5, 5), 0)
    _, esik = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    genis = cv2.dilate(esik, None, iterations=3)
    kontur, _ = cv2.findContours(genis, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for k in kontur:
        (x, y, w, h) = cv2.boundingRect(k)
        if cv2.contourArea(k) > 700:
            cv2.rectangle(frame1, (x, y), (w + x, h + y), (0, 0, 255), 2)

    cv2.imshow('feed', frame1)
    frame1 = frame2
    ret, frame2 = videom.read()

    # Eğer q tuşuna basıldı ise oynatmayı durdur.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

videom.release()
cv2.destroyAllWindows()