import cv2
import pickle

#img = cv2.imread('carParkImg.png')

#Araba park yerlerinin koordinatlarını tutmak için liste
width, height = 107, 48

try:
    # Daha önce kaydedilmiş park yerleri yükle
    with open('CarParkPosition', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

# Fareye tıklanıp tıklanmadığını belirlemek için fonksiyon
def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        # Yeni bir park yeri ekleyin
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            # Fare bırakıldığında park yeri çizgisinin üzerindeyse, o park yeri silinir
            if x1< x< x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    # Güncellenmiş park yerleri dosyaya kaydet
    with open('CarParkPosition', 'wb') as f:
        pickle.dump(posList, f)

# Ana döngü
while True:
    # Görüntüyü oku
    img = cv2.imread('carParkImg.png')

    # Kaydedilmiş park yerlerini çiz
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    #cv2.rectangle(img, (50, 192), (157, 240), (255, 0, 255), 2)
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(1)