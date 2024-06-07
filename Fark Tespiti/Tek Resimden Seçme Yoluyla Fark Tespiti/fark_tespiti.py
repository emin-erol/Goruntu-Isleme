from PyQt5.QtWidgets import *
import cv2
import numpy as np
import imutils
from skimage.metrics import structural_similarity as compare_ssim

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 'FARK TESPİTİ' basligi
        self.setWindowTitle("Fark Tespiti")
        self.setGeometry(200, 200, 700, 500)
        self.header = QLabel("FARK TESPİTİ", self)
        self.header.move(230, 30)
        self.header.setStyleSheet("font-size: 22pt; font-weight: bold")

        # 'Load an Image' butonu
        self.picButton = QPushButton("Resim Yükle", self)
        self.picButton.clicked.connect(self.openFileDialog)
        self.picButton.setFixedSize(150, 50)
        self.picButton.setStyleSheet("font-size: 11pt")
        sizeOfPicButton = self.picButton.sizeHint()
        self.picButton.move(int((self.width() - sizeOfPicButton.width()) / 2),
                            int((self.height() - sizeOfPicButton.height()) / 2))

        # koordinatlarin yazdirilacagi label'lar
        self.noktaLabel1 = QLabel("1. Nokta Koordinatları: ", self)
        self.noktaLabel2 = QLabel("2. Nokta Koordinatları: ", self)
        self.noktaLabel1.move(280, 200)
        self.noktaLabel2.move(280, 250)
        self.noktaLabel1.hide()
        self.noktaLabel2.hide()

        # kirpma isleminin basarili oldugunu bildiren label
        self.successLabel = QLabel("Kırpma İşlemi Başarılı!", self)
        self.successLabel.move(285, 410)
        self.successLabel.hide()

        # kirpilan resmi silen buton
        self.deleteButton = QPushButton("Resmi Sil", self)
        self.deleteButton.setFixedSize(150, 50)
        self.deleteButton.move(280, 300)
        self.deleteButton.clicked.connect(self.deleteImage)
        self.deleteButton.hide()

        self.secondButton = QPushButton("İkinci Resmi Seç", self)
        self.secondButton.setFixedSize(150, 50)
        self.secondButton.move(280, 350)
        self.secondButton.clicked.connect(self.ikinciResim)
        self.secondButton.hide()

        self.compareButton = QPushButton("Resimleri Karşılaştır", self)
        self.compareButton.setFixedSize(150, 50)
        self.compareButton.move(280, 350)
        self.compareButton.clicked.connect(self.resimKarsilastir)
        self.compareButton.hide()

        self.fileName = 0
        self.indis = 0

    def openFileDialog(self):
        if self.fileName == 0:
            options = QFileDialog.Options()
            self.fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Dosya Seç", "", "All Files (*);;Python Files (*.py)",
                                                  options=options)

        if self.fileName:
            self.noktaLabel1.show()
            self.noktaLabel2.show()
            # self.cropButton.show()
            self.deleteButton.show()
            self.picButton.hide()
            self.openFile()

    def openFile(self):
        self.points = []
        self.img = cv2.imread(self.fileName)

        def mouseEvents(event, x, y, flags, params):
            if event == cv2.EVENT_LBUTTONDOWN:
                if len(self.points) < 2:
                    self.points.append((x, y))
                if len(self.points) == 2:
                    self.cropImage()

        cv2.namedWindow("Image")
        cv2.imshow("Image", self.img)
        cv2.setMouseCallback("Image", mouseEvents)
        cv2.waitKey(0)

    def cropImage(self):
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]
        self.noktaLabel1.hide()
        self.noktaLabel2.hide()
        self.noktaLabel1.setText(f"1. Nokta Koordinatı: ({x1}, {y1})")
        self.noktaLabel2.setText(f"2. Nokta Koordinatı: ({x2}, {y2})")
        self.noktaLabel1.show()
        self.noktaLabel2.show()

        cv2.rectangle(self.img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imshow("Image", self.img)
        self.cropped_img = self.img[y1:y2, x1:x2]
        if self.indis == 0:
            cv2.imwrite("fark_resmi1.jpg", self.cropped_img)
            self.indis += 1
            self.successLabel.show()
            self.secondButton.show()

        elif self.indis == 1:
            cv2.imwrite("fark_resmi2.jpg", self.cropped_img)
            self.indis += 1
            self.secondButton.hide()
            self.successLabel.show()
            self.compareButton.show()

    def ikinciResim(self):
        self.noktaLabel1.setText("1. Nokta Koordinatı: ")
        self.noktaLabel2.setText("2. Nokta Koordinatı: ")
        self.successLabel.hide()
        self.secondButton.hide()
        self.openFile()

    def resimKarsilastir(self):
        self.noktaLabel1.hide()
        self.noktaLabel2.hide()
        self.deleteButton.hide()
        self.successLabel.hide()
        self.successLabel.setText("Resimler Başarıyla Karşılaştırıldı!")
        self.successLabel.show()
        self.compareButton.hide()
        self.img1 = cv2.imread("fark_resmi1.jpg")
        self.img2 = cv2.imread("fark_resmi2.jpg")

        # resimlerin boyutlarinin duzenlenmesi
        self.img1 = cv2.resize(self.img1, (640, 480))
        self.img2 = cv2.resize(self.img2, (640, 480))
        self.img_height = self.img1.shape[0]

        # resimlerin gri formata gecirilmesi
        gray1 = cv2.cvtColor(self.img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(self.img2, cv2.COLOR_BGR2GRAY)

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
            cv2.circle(self.img1, c, 10, (0, 255, 0), 2)
            cv2.circle(self.img2, c, 10, (0, 255, 0), 2)

        # gerekli gorsellerin ekranda gosterilmesi
        cv2.imshow("Image 1", self.img1)
        cv2.imshow("Image 2", self.img2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def deleteImage(self):
        pass

