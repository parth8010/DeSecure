import cv2
import numpy as np
import matplotlib.pyplot as plt

def temporal_scores(video_path):
    cap = cv2.VideoCapture(video_path)
    scores = []
    prev = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if prev is not None:
            diff = np.mean(np.abs(gray - prev)) / 255
            scores.append(diff)
        prev = gray

    cap.release()
    return scores


def frequency_score(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    f = np.fft.fft2(gray)
    magnitude = np.abs(f)
    return np.mean(magnitude) / 1e6
