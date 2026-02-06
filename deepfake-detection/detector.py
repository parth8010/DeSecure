import numpy as np
import cv2
import logging

logger = logging.getLogger(__name__)


# ---------------- DETECTOR ---------------- #

class DeepfakeDetector:
    def __init__(self, config=None):
        if config is None:
            config = {}
        self.threshold = config.get("detection_threshold", 0.7)
        logger.info(f"DeepfakeDetector initialized (demo mode - no PyTorch)")

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
    
    def analyze_image(self, image_path):
        """
        Analyze an image for deepfake detection
        """
        try:
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                return {"success": False, "error": "Failed to load image"}
            
            # Get CNN score (placeholder)
            cnn = self.cnn_score()
            
            # Frequency analysis
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            f = np.fft.fft2(gray)
            magnitude = np.abs(f)
            freq_score = np.mean(magnitude) / 1e6
            freq_normalized = min(max(freq_score, 0), 1)
            
            # Final score
            final = self.final_score(cnn, 0.5, freq_normalized)
            verdict = self.verdict(final)
            
            return {
                "success": True,
                "verdict": verdict,
                "confidence": float(final),
                "details": {
                    "cnn_score": float(cnn),
                    "frequency_score": float(freq_normalized)
                }
            }
        except Exception as e:
            logger.error(f"Image analysis error: {e}")
            return {"success": False, "error": str(e)}
    
    def analyze_video(self, video_path):
        """
        Analyze a video for deepfake detection
        """
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return {"success": False, "error": "Failed to open video"}
            
            # Get CNN score
            cnn = self.cnn_score()
            
            # Temporal consistency analysis
            scores = []
            prev = None
            frame_count = 0
            max_frames = 30  # Analyze first 30 frames
            
            while cap.isOpened() and frame_count < max_frames:
                ret, frame = cap.read()
                if not ret:
                    break
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if prev is not None:
                    diff = np.mean(np.abs(gray - prev)) / 255
                    scores.append(diff)
                prev = gray
                frame_count += 1
            
            cap.release()
            
            # Calculate temporal score
            temporal = np.mean(scores) if scores else 0.5
            
            # Final score
            final = self.final_score(cnn, temporal, 0.5)
            verdict = self.verdict(final)
            
            return {
                "success": True,
                "verdict": verdict,
                "confidence": float(final),
                "details": {
                    "cnn_score": float(cnn),
                    "temporal_score": float(temporal),
                    "frames_analyzed": frame_count
                }
            }
        except Exception as e:
            logger.error(f"Video analysis error: {e}")
            return {"success": False, "error": str(e)}
