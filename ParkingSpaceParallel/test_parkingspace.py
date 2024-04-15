# test_parkingspace.py

import unittest
import cv2
import numpy as np

# check_parking_space_parallel fonksiyonunu içeren modülü ekle
from main import check_parking_space_parallel

class TestParkingSpace(unittest.TestCase):
    def test_check_parking_space_parallel(self):
        # Test için gerekli bağımlılıkları hazırla
        img_processed = np.zeros((100, 100), dtype=np.uint8)  # Örnek bir işlenmiş görüntü

        # check_parking_space_parallel fonksiyonunu çağır
        result = check_parking_space_parallel(img_processed)

        # Beklenen sonuçları kontrol et (örneğin, bir sayı)
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)

if __name__ == '__main__':
    unittest.main()
