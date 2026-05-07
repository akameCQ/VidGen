# VidGen - DeepFace AI Video Analiz & Deepfake Tespiti

VidGen, yapay zeka ve derin öğrenme (DeepFace) kullanarak videolardaki yüzleri tespit eden ve bu yüzlerin gerçek veya sahte (deepfake) olup olmadığını analiz eden modern bir masaüstü uygulamasıdır.

![Ekran Görüntüsü](assets/screenshot.png)

*(Not: `assets/screenshot.png` dizinine uygulamanın bir ekran görüntüsünü eklemeyi unutmayın.)*

## Özellikler

- **Yapay Zeka Destekli Analiz**: DeepFace ve VGG-Face modeli ile yüksek doğrulukta yüz analizi.
- **Deepfake Tespiti**: Videodaki yüzlerin gerçek mi yoksa deepfake mi olduğunu ayırt edebilme.
- **Bellek (RAM) Optimizasyonu**: Videolar baştan sona tek seferde belleğe yüklenmez. Bunun yerine, bellek taşmalarını (OOM) önlemek için kareler akışkan olarak okunup anında analiz edilir.
- **Modern ve Şık Arayüz**: Karanlık tema (Dark Mode) üzerine kurulu, akıcı ve bilgilendirici modern bir kullanıcı arayüzü.
- **Gerçek Zamanlı İlerleme Çubuğu**: Videonun yüzde kaçının işlendiğini arayüz üzerinden anlık olarak takip edebilme.

## Gelecekte Yapılacaklar (Yol Haritası)

- **Özel Deepfake Modeli**: İlerleyen aşamalarda sadece hazır DeepFace kütüphanesi ile sınırlı kalınmayacak; tamamen deepfake tespiti üzerine eğitilmiş, **kendi geliştirdiğimiz özel derin öğrenme modelimiz** sisteme entegre edilecektir. Böylece tespit doğruluk oranları maksimum seviyeye çıkarılacaktır.

## Gereksinimler

Projenin çalışması için bilgisayarınızda Python 3.8+ kurulu olması önerilir.

```bash
pip install -r requirements.txt
```

## Kullanım

Uygulamayı başlatmak için terminal veya komut satırından aşağıdaki komutu çalıştırın:

```bash
python deepface_gui.py
```

1. Açılan arayüzdeki "Video Yükle" bölümüne tıklayarak analiz etmek istediğiniz videoyu (`.mp4`, `.avi`, vb.) seçin.
2. "Analizi Başlat" butonuna tıklayın.
3. İlerleme çubuğunun dolmasını bekleyin. Analiz bittiğinde sonuç "Analiz Geçmişi" paneline yansıyacaktır.
