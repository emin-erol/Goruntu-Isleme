from ultralytics import YOLO
import pyautogui as pg
import numpy as np
import cv2

model = YOLO("yolov8n-face.pt")
EKRAN_GENISLIGI, EKRAN_UZUNLUGU = pg.size()
EKRAN_MERKEZI = (EKRAN_GENISLIGI // 2, EKRAN_UZUNLUGU // 2)

pg.FAILSAFE = False

cap = cv2.VideoCapture(0)

kalibrasyon_merkezi = None
esik_degeri = 5
gecerli_merkez = None
gecerli_merkez_filtreli = None

while True:
    ret, frame = cap.read()

    if not ret:
        break

    sonuc = model(frame, verbose=False)

    for i in range(len(sonuc[0].boxes)):
        x1, y1, x2, y2 = sonuc[0].boxes.xyxy[i]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        merkez_x = x1 + (x2 - x1) // 2
        merkez_y = y1 + (y2 - y1) // 2
        gecerli_merkez = (merkez_x, merkez_y)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.circle(frame, gecerli_merkez, 5, (255, 0, 0), -1)

        if kalibrasyon_merkezi is None:
            kalibrasyon_merkezi = gecerli_merkez

    aci = None
    if kalibrasyon_merkezi is not None:
        cv2.circle(frame, kalibrasyon_merkezi, 5, (0, 0, 255), -1)
        if gecerli_merkez is not None:
            cv2.line(frame, kalibrasyon_merkezi, gecerli_merkez, (0, 255, 255), 2)

            yon_vektoru = np.array(gecerli_merkez) - np.array(kalibrasyon_merkezi)

            aci = np.degrees(np.arctan2(yon_vektoru[0], yon_vektoru[1]))
            mesafe = np.linalg.norm(yon_vektoru)

            if mesafe > esik_degeri:
                if gecerli_merkez_filtreli is None:
                    gecerli_merkez_filtreli = np.array(gecerli_merkez)
                else:
                    alpha = 0.2
                    gecerli_merkez_filtreli = alpha * np.array(gecerli_merkez) + (1 - alpha) * gecerli_merkez_filtreli

                yon_vektoru_filtreli = gecerli_merkez_filtreli - np.array(kalibrasyon_merkezi)
                aci = np.degrees(np.arctan2(yon_vektoru_filtreli[0], yon_vektoru_filtreli[1]))

                if aci < 0:
                    aci += 360

                hareket_miktari = mesafe * 15
                dx = int(np.cos(np.deg2rad(aci - 270)) * hareket_miktari)
                dy = int(np.sin(np.deg2rad(aci - 270)) * hareket_miktari)

                if hareket_miktari > 20:
                    pg.moveTo(EKRAN_MERKEZI[0] + dx, EKRAN_MERKEZI[1] + dy, 0.2)

            cv2.putText(frame, f"{int(aci)} deg", (gecerli_merkez[0] - 10, gecerli_merkez[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)

    cv2.imshow("Sonuc", frame)

    key = cv2.waitKey(1)
    if key == 27 or cv2.getWindowProperty("Sonuc", cv2.WND_PROP_VISIBLE) < 1:
        break

    elif key == ord('c'):
        if 'merkez_x' in locals() and 'merkez_y' in locals():
            kalibrasyon_merkezi = (merkez_x, merkez_y)
            gecerli_merkez_filtreli = np.array(kalibrasyon_merkezi)
            pg.moveTo(EKRAN_MERKEZI[0], EKRAN_MERKEZI[1])

cap.release()
cv2.destroyAllWindows()
