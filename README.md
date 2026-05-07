# VidGen - DeepFace AI Video Analysis & Deepfake Detection

VidGen is a modern desktop application that detects faces in videos and analyzes whether they are real or fake (deepfake) using artificial intelligence and deep learning (DeepFace).

<img src="https://github.com/user-attachments/assets/978e2f21-8e3a-414d-aa54-0cc326084b3b" width="1000" alt="VidGen Dashboard">

## ✨ Features

- **AI-Powered Analysis**: High-accuracy face analysis using the DeepFace library and VGG-Face model.
- **Deepfake Detection**: Ability to distinguish whether the faces in the video are real or deepfakes.
- **Memory (RAM) Optimization**: Videos are not loaded into memory all at once. Instead, frames are read sequentially and analyzed immediately to prevent out-of-memory (OOM) crashes.
- **Modern and Sleek UI**: A smooth and informative modern user interface built on a Dark Mode theme.
- **Real-Time Progress Bar**: Track the percentage of the video being processed in real-time through the UI.

## Future Work (Roadmap)

- **Custom Deepfake Model**: In future stages, we will not limit ourselves to the pre-built DeepFace library. We will integrate **our own custom deep learning model** trained specifically for deepfake detection. This will maximize our detection accuracy rates.

## Requirements

Python 3.8+ is recommended to run the project.

```bash
pip install -r requirements.txt
```

## Usage

To start the application, run the following command in your terminal or command prompt:

```bash
python deepface_gui.py
```

1. Click on the "Video Yükle" (Upload Video) section in the opened interface to select the video (`.mp4`, `.avi`, etc.) you want to analyze.
2. Click the "Analizi Başlat" (Start Analysis) button.
3. Wait for the progress bar to fill. Once the analysis is complete, the result will be reflected in the "Analiz Geçmişi" (Analysis History) panel.
