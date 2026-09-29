import os
import cv2
import numpy as np
import joblib

BASE_DIR = r"D:\7th Semester\Information Security\aadhaar-inspired-security"
MODEL_PATH = os.path.join(BASE_DIR, "models", "fingerprint_pad", "rf_fp_pad.pkl")

class FingerprintPAD:
    def __init__(self):
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Fingerprint PAD model not found at {MODEL_PATH}")
        self.clf = joblib.load(MODEL_PATH)
        
    def _extract_features(self, image_path):
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return None
            
        img = cv2.resize(img, (96, 96))
        hist = cv2.calcHist([img], [0], None, [32], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        
        mean_val = np.mean(img)
        std_val = np.std(img)
        
        return np.hstack([hist, [mean_val, std_val]])

    def detect_liveness(self, probe_image_path: str) -> dict:
        """
        Classifies the fingerprint image as GENUINE (0) or SPOOF (1).
        """
        if not os.path.exists(probe_image_path):
            return {"status": "ERROR", "message": f"Probe image missing: {probe_image_path}"}
            
        features = self._extract_features(probe_image_path)
        if features is None:
            return {"status": "ERROR", "message": "Failed to read image for Fingerprint PAD."}
            
        try:
            # 0 -> GENUINE, 1 -> SPOOF
            prediction = self.clf.predict([features])[0]
            probability = self.clf.predict_proba([features])[0]
            
            is_genuine = (prediction == 0)
            confidence = float(probability[prediction])
            
            return {
                "status": "GENUINE" if is_genuine else "SPOOF",
                "confidence": confidence,
                "message": "Presentation Attack Detected!" if not is_genuine else "Genuine Fingerprint Detected."
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Fingerprint PAD error: {str(e)}"
            }

if __name__ == "__main__":
    pad = FingerprintPAD()
    print("Fingerprint PAD module loaded successfully.")
