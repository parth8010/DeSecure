import cv2

class FaceDetector:
    def __init__(self, config=None):
        self.detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector.detectMultiScale(gray, 1.3, 5)
        return faces


class FaceAnalyzer:
    def analyze(self, face):
        # Simple texture-based features (placeholder for ML explainability)
        mean = face.mean()
        std = face.std()
        return {
            "mean_intensity": float(mean),
            "std_intensity": float(std)
        }
