import librosa
import numpy as np
import logging

logger = logging.getLogger(__name__)

def analyze_voice(path):
    try:
        y, sr = librosa.load(path, sr=None)
        mfcc = librosa.feature.mfcc(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        
        # Calculate confidence score
        score = (np.mean(mfcc) + np.mean(zcr)) / 100
        confidence = min(max(score, 0), 1)
        
        # Determine verdict based on threshold
        verdict = "FAKE" if confidence > 0.7 else "REAL"
        
        # Spectral features for visualization
        spectral = np.mean(mfcc, axis=0).tolist()
        
        return {
            "success": True,
            "verdict": verdict,
            "confidence": float(confidence),
            "spectral": spectral
        }
    except Exception as e:
        logger.error(f"Voice analysis error: {e}")
        return {
            "success": False,
            "error": str(e)
        }
