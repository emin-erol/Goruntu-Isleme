import cv2
import numpy as np
import Sensors

cap = cv2.VideoCapture("car.mp4")  # videoyu aliyoruz
subtractor = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)  # arkaplan cikarma icin degisken olusturuyoruz
kernel = np.ones((7, 7), np.uint8)  # videoda gurultu azaltmada kullanmak uzere 7x7 lik cekirdek olusturuyoruz
font = cv2.FONT_HERSHEY_COMPLEX_SMALL  # video uzerine yazdiracagimiz yazilarin fontunu tanimliyoruz

sensors = Sensors.ss  # her serit icin olusturulan sensorleri kodumuza dahil ediyoruz

while True:
    ret, frame = cap.read()  # videodaki her bir frame'i tek tek aliyoruz
    if not ret:
        break
    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # frame'i gri tonlu resme ceviriyoruz
    cleanFrame = subtractor.apply(imgGray)  # yukarida tanimladigimiz arkplan cikarici ile arkaplani cikariyoruz
    cleanFrame = cv2.morphologyEx(cleanFrame, cv2.MORPH_OPEN, kernel)  # gurultu azaltiyoruz
    ret2, thresh = cv2.threshold(cleanFrame, 0, 255, cv2.THRESH_BINARY)  # frame'i esikliyoruz (siyah beyaz hale getiriyoruz)

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # siyah beyaz frame'deki konturlari buluyoruz

    filledImg = np.zeros((frame.shape[0], frame.shape[1], 1), np.uint8)  # konturlarin icini beyaz kalan her yeri siyah yapmak icin doldurulmusResim degiskenini tanimliyoruz
    for cnt in contours:  # her bir konturda geziyoruz
        x, y, w, h = cv2.boundingRect(cnt)  # her bir konturun sol ust koordinatlarini, genisligini ve yuksekligini aliyoruz
        if w > 100 and h > 100:  # yaklasik araba boyutundaki konturlari filtreliyoruz
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)  # ilgili konturlari frame'e ciziyoruz
            cv2.rectangle(filledImg, (x, y), (x+w, y+h), 255, -1)  # ayni konturu siyah piksellerden olusan filledImg'ye ici beyaz olacak sekilde ciziyoruz

    totalCarCount = 0  # toplam arac sayisini tutan degiskeni tanimliyoruz
    for sensor in sensors:  # her bir sensor uzerinde geziyoruz
        sMaskResult = cv2.bitwise_and(filledImg, filledImg, mask=sensor.mask)  # sadece sensor icinde kalan kontur bolgesini aliyoruz
        sWhitePixel = np.sum(sMaskResult == 255)  # sensor icinde kalan konturun beyaz piksellerini sayiyoruz
        sRatio = sWhitePixel / sensor.maskArea  # sensor icinde kalan konturdaki beyaz piksel sayisini tum sensorun alanina bolerek konturun sensoru ne kadar kapladigini olcuyoruz

        if sRatio > 0.75 and sensor.situation is False:  # sensor icinde kalan konturun oraninin bire yakin olmasi ve sensorun kapali oldugu durum
            # bu durumda sensor yeni bir arac algilamistir burada sensoru yesile ceviriyoruz ve sensor durumunu true (aktif) hale getiriyoruz
            cv2.rectangle(frame, (sensor.k1.x, sensor.k1.y), (sensor.k2.x, sensor.k2.y), (0, 255, 0), -1)
            sensor.situation = True
        elif sRatio <= 0.75 and sensor.situation is True:  # sensor icinde kalan konturun oraninin sifira yakin olmasi ve sensorun acik olmasi durumu
            # bu durumda sensorun algiladigi arac araliktan cikmis demektir bu halde sensoru kapatip kirmizi renge ceviriyoruz
            # ayni zamanda bir araci sayma islemini bitirdigi icin saydigi arac sayisini bir artiriyoruz
            cv2.rectangle(frame, (sensor.k1.x, sensor.k1.y), (sensor.k2.x, sensor.k2.y), (0, 0, 255), -1)
            sensor.situation = False
            sensor.carCount += 1
        elif sRatio > 0.75 and sensor.situation is True:  # sensor icinde kalan konturun oraninin bire yakin olmasi ve sensorun acik oldugu durum
            # bu durumda sensor algiladigi araci hala algilamaya devam ediyordur bu yuzden araliktan cikana kadar sensor yesil kalacak
            cv2.rectangle(frame, (sensor.k1.x, sensor.k1.y), (sensor.k2.x, sensor.k2.y), (0, 255, 0), -1)
        else:  # bu durum herhangi bir algilamanin olmadigi yani sensorun calismadigi ve aracin olmadigi durumdur bu durumda sensor kirmizi olmaya devam etmelidir
            cv2.rectangle(frame, (sensor.k1.x, sensor.k1.y), (sensor.k2.x, sensor.k2.y), (0, 0, 255), -1)

        # her sensorun icine algiladigi arac sayisini yaziyoruz
        cv2.putText(frame, str(sensor.carCount), (sensor.k1.x, sensor.k1.y + 50), font, 3, (255, 255, 255))
        totalCarCount += sensor.carCount  # her bir sensorun algiladigi arac sayisini toplam arac sayisine ekliyoruz
    # toplam algilanan arac sayisini yaziyoruz
    cv2.putText(frame, "Total Car:" + str(totalCarCount), (650, 800), font, 2, (0, 255, 0), 3)

    cv2.imshow("Result", frame)  # islemler sonucu frame'in son halini goruntuluyoruz

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

