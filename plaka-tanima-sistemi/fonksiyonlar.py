import cv2
import numpy as np

def resimAc(imageName):
    # Dosyadan resim okumak icin dosyanin yolunu seciyoruz
    img = cv2.imread("Images/"+imageName)
    cv2.namedWindow("1 - Orijinal Resim", cv2.WINDOW_NORMAL)
    cv2.imshow("1 - Orijinal Resim", img)
    return img

def griyeCevir(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.namedWindow("2 - Griye Donusturme Islemi", cv2.WINDOW_NORMAL)
    cv2.imshow("2 - Griye Donusturme Islemi", imgGray)
    return imgGray

def gurultuAzalt(imgGray):
    # bilateralFilter fonksiyonu kenarlari koruyarak resimlerde yumusatma islemi yapar
    # 9 degeri filtre boyutunu, ilk 75 degeri benzer renkli piksellerin daha fazla vurgulanmasini,
    # ikinci 75 degeri ise piksellerin fiziksel uzakliklarina dayali olarak benzer piksellere daha fazla agirlik verilmesini saglar
    gurultuAzalt = cv2.bilateralFilter(imgGray, 9, 75, 75)
    cv2.namedWindow("3 - Gurultu Temizleme Islemi", cv2.WINDOW_NORMAL)
    cv2.imshow("3 - Gurultu Temizleme Islemi", gurultuAzalt)
    return gurultuAzalt

def histogramEsitleme(gurultuAzalt):
    # histogram esitleme ile goruntudeki piksel dagilimini esitleyerek goruntunun kontrasti artirilir belirginlestirilir
    hisEsitleme = cv2. equalizeHist(gurultuAzalt)
    cv2.namedWindow("4 - Histogram Esitleme Islemi", cv2.WINDOW_NORMAL)
    cv2.imshow("4 - Histogram Esitleme Islemi", hisEsitleme)
    return hisEsitleme

def morfolojikIslem(hisEsitleme):
    # acma islemi uygulayarak goruntudeki kucuk parcalar yok edilmeye calisilir gurultulerin etkisi azaltilir
    # kernel degiskeni (5,5) boyutunda bir cekirdek matris tutar bununla acma islemi uygulanir
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    morfolojikResim = cv2.morphologyEx(hisEsitleme, cv2.MORPH_OPEN, kernel, iterations=15)
    cv2.namedWindow("5 - Morfolojik Acilim Islemi", cv2.WINDOW_NORMAL)
    cv2.imshow("5 - Morfolojik Acilim Islemi", morfolojikResim)
    return morfolojikResim

def goruntuCikarma(hisEsitleme, morfolojikResim):
    # burada morfolojik isleme tabi tutulmus goruntuyu histogram uygulanmis goruntuden cikartacagiz
    goruntuCikarilmisResim = cv2.subtract(hisEsitleme, morfolojikResim)
    cv2.namedWindow("6 - Goruntu Cikarma Islemi", cv2.WINDOW_NORMAL)
    cv2.imshow("6 - Goruntu Cikarma Islemi", goruntuCikarilmisResim)
    return goruntuCikarilmisResim

def goruntuEsikle(goruntuCikarilmisResim):
    ret, goruntuEsikle = cv2.threshold(goruntuCikarilmisResim, 0, 255, cv2.THRESH_OTSU)
    cv2.namedWindow("7 - Goruntu Esikleme Islemi", cv2.WINDOW_NORMAL)
    cv2.imshow("7 - Goruntu Esikleme Islemi", goruntuEsikle)
    return goruntuEsikle

def cannyEdge(goruntuEsikleme):
    # goruntu uzerindeki kenarlari algiliyoruz; 250,255 araligi ile beyaza cok kenarlari algilar
    cannyGoruntu = cv2.Canny(goruntuEsikleme, 250, 255)
    cv2.namedWindow("8 - Canny Edge Islemi", cv2.WINDOW_NORMAL)
    cv2.imshow("8 - Canny Edge Islemi", cannyGoruntu)
    # bu islem ile kenarlar 0 ile 255 degeri arasinda donusturur negatif degerleri pozitif yapar
    cannyGoruntu = cv2.convertScaleAbs(cannyGoruntu)
    return cannyGoruntu

def genisletmeIslemi(cannyGoruntu):
    # kenarlari guclendirmek icin genisletme uyguluyoruz
    cekirdek = np.ones((3, 3), np.uint8)
    genisletilmisGoruntu = cv2.dilate(cannyGoruntu, cekirdek, iterations=1)
    cv2.namedWindow("9 - Kenarlari Genisletme Islemi", cv2.WINDOW_NORMAL)
    cv2.imshow("9 - Kenarlari Genisletme Islemi", genisletilmisGoruntu)
    return genisletilmisGoruntu

def konturIslemi(img, genisletilmisGoruntu):
    # kenarlara dayanan resimdeki konturlari bulma
    contours, hierarchy = cv2.findContours(genisletilmisGoruntu, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # rakamlari alana gore siraliyoruz boylece sayi plakasi ilk 10 konturda olacak
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None
    for c in contours:
        # yaklasik cizgi belirliyoruz
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.06 * peri, True) # %6 hata payi ile yaklasiklik
        # yaklasik konturun dort noktasi varsa o zaman plakamizi yaklasik olarak buldugumuzu varsayabiliriz
        if len(approx) == 4:
            screenCnt = approx
            break
    final = cv2.drawContours(img, [screenCnt], -1, (9, 236, 255), 3) # cerceveyi ciziyoruz
    cv2.namedWindow("10 - Konturlu Goruntu", cv2.WINDOW_NORMAL)
    cv2.imshow("10 - Konturlu Goruntu", final)
    return screenCnt

def maskelemeIslemi(img, imgGray, screenCnt):
    # numara plakasi disindaki kismi maskeleme
    mask = np.zeros(imgGray.shape, np.uint8)
    yeniGoruntu = cv2.drawContours(mask, [screenCnt], 0, (255, 255, 255), -1)
    yeniGoruntu = cv2.bitwise_and(img, img, mask=mask)
    cv2.namedWindow("11 - Plaka", cv2.WINDOW_NORMAL)
    cv2.imshow("11 - Plaka", yeniGoruntu)
    return yeniGoruntu

def plakaIyilestir(yeniGoruntu):
    # numara plakasini iyilestirmek icin histogram esitleme islemi uyguluyoruz
    # goruntuyu YCrCb modeline donusturup 3 kanala boluyoruz
    y, cr, cb = cv2.split(cv2.cvtColor(yeniGoruntu, cv2.COLOR_RGB2YCrCb))
    y = cv2.equalizeHist(y)
    # histogram uyguladiktan sonra 3 kanali tekrar birlestiriyoruz
    sonResim = cv2.cvtColor(cv2.merge([y, cr, cb]), cv2.COLOR_YCrCb2RGB)
    cv2.namedWindow("12 - Iyilestirilmis Plaka", cv2.WINDOW_NORMAL)
    cv2.imshow("12 - Iyilestirilmis Plaka", sonResim)
    return sonResim

def goruntule(resimAdi):
    image = resimAc(resimAdi)
    griResim = griyeCevir(image)
    gurultusuzResim = gurultuAzalt(griResim)
    histogramEsitlenmisResim = histogramEsitleme(gurultusuzResim)
    morfolojikResim = morfolojikIslem(histogramEsitlenmisResim)
    goruntuCikarilmisResim = goruntuCikarma(histogramEsitlenmisResim, morfolojikResim)
    goruntuEsiklenmisResim = goruntuEsikle(goruntuCikarilmisResim)
    cannyEdgeResim = cannyEdge(goruntuEsiklenmisResim)
    genisletilmisResim = genisletmeIslemi(cannyEdgeResim)
    konturlanmisResim = konturIslemi(image, genisletilmisResim)
    maskelenmisResim = maskelemeIslemi(image, griResim, konturlanmisResim)
    plakaIyilestir(maskelenmisResim)



