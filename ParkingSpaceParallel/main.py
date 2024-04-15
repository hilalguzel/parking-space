import cv2
import cvzone
import pickle
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import time
import psutil

# Video akışı
cap = cv2.VideoCapture('carPark.mp4')

# Daha önce kaydedilmiş park yerlerini yükle
with open('CarParkPosition', 'rb') as f:
    posList = pickle.load(f)
width, height = 107, 48

# Park yerlerini kontrol etmek için fonksiyon
def check_parking_space_single(img_processed, pos):
    x, y = pos

    # Park yerini kırp
    img_crop = img_processed[y:y+height, x:x+width]

    # Kırpılmış görüntüdeki beyaz piksellerin sayısını say
    count = cv2.countNonZero(img_crop)
    cvzone.putTextRect(img, str(count), (x, y + height -3), scale=1,
                       thickness=2, offset=0, colorR=(0, 0, 255))

    # Piksel sayısına göre renk ve kalınlığı belirle
    if count < 950:
        color = (0, 255, 0)
        thickness =3
    else:
        color = (0, 0, 255)
        thickness = 2

    # Park yerini çevreleyen dikdörtgeni çiz
    cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)

    # Piksel sayısını ekrana yazdır
    cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                       thickness=2, offset=0, colorR=color)

    return count  # Return the count value

# Boş park yerlerini kontrol etmek için paralel fonksiyon
def check_parking_space_parallel(img_processed):
    space_counter = 0

    with ThreadPoolExecutor() as executor:
        # Paralel olarak park yerlerini kontrol et
        futures = [executor.submit(check_parking_space_single, img_processed, pos) for pos in posList]
        # Toplam boş park yerlerini say
        for future in futures:
            count = future.result()
            if count is not None and count < 950:
                space_counter += 1

    # Boş park yerlerinin sayısını ekrana yazdır
    cvzone.putTextRect(img, f'Free {space_counter}/ {len(posList)}', (100, 50), scale=3,
                       thickness=5, offset=20, colorR=(0, 200, 0))

# Ana döngü
while True:
    start_time = time.time()  # İşlemin başlangıcı

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Video akışından bir kare al
    success, img = cap.read()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
    img_threshold = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY_INV, 25, 16)
    img_median = cv2.medianBlur(img_threshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    img_dilate = cv2.dilate(img_median, kernel, iterations=1)

    # Boş park yerlerini kontrol et
    start_processing_time = time.time()  # İşlemin başlangıcı
    check_parking_space_parallel(img_dilate)
    end_processing_time = time.time()  # İşlemin bitişi

    # Toplam işlem süresini ve boş park yerlerini kontrol etme süresini hesapla
    total_processing_time = end_processing_time - start_processing_time
    total_time = time.time() - start_time

    # CPU kullanımını ölç
    cpu_usage = psutil.cpu_percent()

    # RAM kullanımını ölç
    ram_usage = psutil.virtual_memory().percent

    # İşlem süreleri ve kaynak kullanımını ekrana yazdır
    print(f"Toplam İşlem Süresi: {total_time} saniye")
    print(f"Boş Park Yeri Kontrol Süresi: {total_processing_time} saniye")
    print(f"CPU Kullanımı: {cpu_usage}%")
    print(f"RAM Kullanımı: {ram_usage}%")

    cv2.imshow("Image", img)
    cv2.waitKey(1)
