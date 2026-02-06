import librosa
import numpy as np

def analyze_voice(path):
    y, sr = librosa.load(path, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    score = (np.mean(mfcc) + np.mean(zcr)) / 100
    return min(max(score, 0), 1)
