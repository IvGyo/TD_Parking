import cv2
import pytesseract
import numpy as np
from tensorflow.keras.models import load_model

class LicensePlateRecognizer:
    def __init__(self):
        self.model = load_model('models/plate_detection.h5')
        
    def detect_plate(self, image_path):
        # Зареждане на изображението
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Обработка на изображението
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        edges = cv2.Canny(blur, 50, 150)
        
        # Намиране на контури
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:  # Минимална площ за номер
                # Извличане на текста с OCR
                x, y, w, h = cv2.boundingRect(contour)
                plate_img = gray[y:y+h, x:x+w]
                
                # OCR разпознаване
                plate_text = pytesseract.image_to_string(
                    plate_img, 
                    config='--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                )
                
                if len(plate_text.strip()) >= 6:
                    return self.clean_plate_text(plate_text)
        
        return None
    
    def clean_plate_text(self, text):
        # Почистване и форматиране на текста
        return ''.join(c for c in text if c.isalnum()).upper()
