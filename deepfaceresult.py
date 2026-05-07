import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import cv2 # type: ignore
#cv video işlemede kullanılan kütüphane
import numpy as np
from deepface import DeepFace # type: ignore
#cv den aldığımız frameleri incelemek icin kullanacağımız kütüpane


class DeepFaceResults:
    def __init__(self, path):
        # def init clası oluşturuken kullandığımız temel yapı 
        #self classsın icinde değişkeni kullanabilmemizisağlayan şeydir
        self.path = path
        DeepFace.build_model("VGG-Face")
       

    def start(self, progress_callback=None):
        # gui fonksiyonunun icinde çalıştırdığımız start fonksiyonunin icinde sinyali ve pathı atamamıza yerdımcı oluyor
        return self.detected_frames(progress_callback)

    def detected_frames(self, progress_callback=None):
        #gelen dosya yolunundaki dosyayı cv2 ile incelememizi sağlayan fonksiyon = videocapture
        vidObj = cv2.VideoCapture(self.path)
        
        # Toplam kare sayısını al (ilerleme çubuğu için)
        total_frames = int(vidObj.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames <= 0:
            total_frames = 1
            
        current_frame = 0
        success = True

        while success:
            success, frame = vidObj.read()
            #videocapture fonksiyonu ile aldığımız değişkeni read fonksiyonu ile framelere ayırıyoruz
            if success:
                current_frame += 1
                if progress_callback:
                    # İlerleme oranını yüzde olarak hesaplayıp callback'e gönderiyoruz
                    progress = min(99, int((current_frame / total_frames) * 100))
                    if progress_callback(progress) is False:
                        vidObj.release()
                        return "Stopped"

                frame = cv2.resize(frame, (224, 224))
                # Her kareyi tek tek analiz et, bellekte tutma (OOM sorununu önler)
                if not self.tensorflow_model(frame):
                    vidObj.release()
                    if progress_callback:
                        progress_callback(100)
                    return "Fake"
        
        vidObj.release()
        if progress_callback:
            progress_callback(100)
        return "Real"

    def tensorflow_model(self, frame):
        if not isinstance(frame, np.ndarray):
            return False
        
        temp_path = "temp_frame.jpg"
        cv2.imwrite(temp_path, frame)
        #framesin içinden aldığımız frameleri temp pathe göndererek işncelememiz icin saklıyor

        analysis = DeepFace.extract_faces(
            temp_path,
            detector_backend='opencv',
            anti_spoofing=True,
            enforce_detection=False,
        )
        

        for i, face in enumerate(analysis):
            print(face)
            if not face['is_real']:
                return False

        return True


# Driver Code
if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "C:\\Users\\ERKON TEKNİK\\Desktop\\hm\\15.mp4"
    deep_face = DeepFaceResults(path) 
    print(deep_face.start())