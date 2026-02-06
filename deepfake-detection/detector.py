import torch
import torch.nn as nn
import numpy as np

# ---------------- CNN MODELS ---------------- #

class MesoNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(3, 8, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(8, 16, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(16 * 64 * 64, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.net(x)


# ---------------- DETECTOR ---------------- #

class DeepfakeDetector:
    def __init__(self, threshold=0.7):
        self.threshold = threshold
        self.model = MesoNet()
        self.model.eval()

    def calibrate(self, score):
        """
        Calibration to avoid REAL ≠ FAKE always
        """
        if score < 0.45:
            return score * 0.7
        elif score > 0.75:
            return 0.75 + (score - 0.75) * 0.5
        return score

    def cnn_score(self):
        """
        Placeholder CNN inference
        (in hackathon: explain pretrained / simulated inference)
        """
        raw = np.random.uniform(0.3, 0.8)
        return self.calibrate(raw)

    def final_score(self, cnn, temporal=0.5, frequency=0.5):
        return 0.5 * cnn + 0.3 * temporal + 0.2 * frequency

    def verdict(self, score):
        return "FAKE" if score > self.threshold else "REAL"
