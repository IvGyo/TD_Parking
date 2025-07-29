import cv2
import requests
from threading import Thread

class IPCameraManager:
    def __init__(self, camera_ip, username, password):
        self.camera_ip = camera_ip
        self.auth = (username, password)
        self.stream_url = f"http://{camera_ip}/video"
    
    def capture_frame(self):
        response = requests.get(
            f"http://{self.camera_ip}/snapshot.jpg",
            auth=self.auth
        )
        
        if response.status_code == 200:
            return response.content
        return None
    
    def start_monitoring(self, callback):
        def monitor():
            cap = cv2.VideoCapture(self.stream_url)
            while True:
                ret, frame = cap.read()
                if ret:
                    # Обработка на кадъра
                    callback(frame)
        
        Thread(target=monitor, daemon=True).start()
