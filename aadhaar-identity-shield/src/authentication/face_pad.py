import os
import cv2
import numpy as np
import joblib

BASE_DIR = r"D:\7th Semester\Information Security\aadhaar-inspired-security"
MODEL_PATH = os.path.join(BASE_DIR, "models", "face_pad", "rf_face_pad.pkl")

class FacePAD:
    def __init__(self):
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Face PAD model not found at {MODEL_PATH}")
        self.clf = joblib.load(MODEL_PATH)
        
    def _extract_features(self, image_path):
        img = cv2.imread(image_path)
        if img is None:
            return None
            
        img = cv2.resize(img, (128, 128))
        hist_features = []
        for i in range(3):
            hist = cv2.calcHist([img], [i], None, [32], [0, 256])
            hist = cv2.normalize(hist, hist).flatten()
            hist_features.extend(hist)
            
        return np.array(hist_features)

    def detect_liveness(self, probe_image_path: str) -> dict:
        """
        Classifies the image as LIVE (0) or SPOOF (1).
        """
        if not os.path.exists(probe_image_path):
            return {"status": "ERROR", "message": f"Probe image missing: {probe_image_path}"}
            
        features = self._extract_features(probe_image_path)
        if features is None:
            return {"status": "ERROR", "message": "Failed to read image for PAD."}
            
        try:
            # 0 -> LIVE, 1 -> SPOOF
            prediction = self.clf.predict([features])[0]
            probability = self.clf.predict_proba([features])[0]
            
            is_live = (prediction == 0)
            confidence = float(probability[prediction])
            
            return {
                "status": "LIVE" if is_live else "SPOOF",
                "confidence": confidence,
                "message": "Presentation Attack Detected!" if not is_live else "Live Face Detected."
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Face PAD error: {str(e)}"
            }

if __name__ == "__main__":
    pad = FacePAD()
    print("FacePAD module loaded successfully.")
