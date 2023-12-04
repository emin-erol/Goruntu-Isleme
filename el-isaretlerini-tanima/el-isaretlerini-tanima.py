# Bu uygulamada kameradan alinan el goruntuleri islenerek kullanicinin hangi sayiyi isaret ettigi bulunur
import numpy as np
import cv2
import os

# webcam den goruntumuzu aliyoruz
cap = cv2.VideoCapture(0)
# framelere morfolojik islemler uygulamak icin cekirdek tanimliyoruz
kernel = np.ones((9, 9), np.uint8)

def resimFarkBul(resim1, resim2):
    # kontrol edilecek olan iki resim arasindaki farki bulur
    resim2 = cv2.resize(resim2, (resim1.shape[1], resim1.shape[0]))  # boyutlari ayni olmasi icin resim2'yi resim1 boyutuyla esitliyoruz
    farkResim = cv2.absdiff(resim1, resim2)
    farkSayi = cv2.countNonZero(farkResim)

    return farkSayi

def veriYukle():
    # daha onceden kaydedilmis resimleri ve onlarin isimlerini listelerde sakliyoruz
    isimler = []
    resimler = []

    dosyalar = os.listdir("veriler/")
    for dosya in dosyalar:
        isimler.append(dosya.replace(".jpg", ""))
        resimler.append(cv2.imread("veriler/"+dosya, 0))

    return isimler, resimler

def siniflandir(resim, isimler, resimler):
    # webcam'den alinan anlik frame ile veriler dosyasindaki kaydedilmis resimler karsilastirilir
    # arada en az fark olana kadar devam eder ve sonucu en az fark olan resimle eslestirir
    minIndex = 0
    minDeger = resimFarkBul(resim, resimler[0])
    for i in range(len(isimler)):

        farkDegeri = resimFarkBul(resim, resimler[i])
        if farkDegeri < minDeger:
            minDeger = farkDegeri
            minIndex = i

    return isimler[minIndex]


veriIsimler, veriResimler = veriYukle()

while True:
    ret, frame = cap.read()  # her bir frame i ayri olarak aliyoruz
    frame = cv2.flip(frame, 1)  # ters goruntuyu duzluyoruz
    frame = cv2.resize(frame, (740, 480))  # frame i yeniden boyutlandiriyoruz

    kesilmisFrame = frame[0:300, 450:740]  # eli belirli bir konumda incelemek icin frame'de yer ayiriyoruz
    kesilmisFrameHSV = cv2.cvtColor(kesilmisFrame, cv2.COLOR_BGR2HSV)  # frame'i hsv formatina ceviriyoruz

    # ten rengi icin yaklasik hsv kodlarini belirtiyoruz (farklı framelerde farklilik gosterebilir)
    lower_color = np.array([0, 65, 50])
    upper_color = np.array([90, 255, 255])
    # tanimladigimiz hsv araligini kesilmisFrame'e uyguluyoruz
    filtreliFrame = cv2.inRange(kesilmisFrameHSV, lower_color, upper_color)
    # gurultu temizleme islemi
    filtreliFrame = cv2.morphologyEx(filtreliFrame, cv2.MORPH_CLOSE, kernel)
    # frame'deki konturlari buluyoruz
    cnt, hierarchy = cv2.findContours(filtreliFrame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # en buyuk konturu almak icin konturlari buyukten kucuge siraliyoruz
    cnt = sorted(cnt, key=cv2.contourArea, reverse=True)[:10]
    if len(cnt) > 0:
        x, y, w, h = cv2.boundingRect(cnt[0])  # en buyuk konturun degerlerini aliyoruz
        cv2.rectangle(kesilmisFrame, (x, y), (x+w, y+h), (0, 255, 0), 3)  # konturu frame'e ciziyoruz
        elResmi = filtreliFrame[y:y+h, x:x+w]  # frame'deki kontur bolgesini cikarip aliyoruz
        # cv2.imshow("El Resmi", elResmi)
        print(siniflandir(elResmi, veriIsimler, veriResimler))

    cv2.imshow("Kesilmis Frame", filtreliFrame)
    cv2.imshow("Contours", kesilmisFrame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()



