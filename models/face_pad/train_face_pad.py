import os
import cv2
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

BASE_DIR = r"D:\7th Semester\Information Security\aadhaar-inspired-security"
TRAIN_CSV = os.path.join(BASE_DIR, "data", "metadata", "train_split.csv")
VAL_CSV = os.path.join(BASE_DIR, "data", "metadata", "val_split.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "face_pad", "rf_face_pad.pkl")

def extract_features(image_path):
    """
    Extracts simple color histogram features to distinguish LIVE vs DEEPFAKE.
    StyleGAN generated images often have distinct color distributions compared to real photos.
    """
    img = cv2.imread(image_path)
    if img is None:
        return None
        
    img = cv2.resize(img, (128, 128))
    
    # Calculate histograms for each channel
    hist_features = []
    for i in range(3):
        hist = cv2.calcHist([img], [i], None, [32], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        hist_features.extend(hist)
        
    return np.array(hist_features)

def load_dataset(csv_path, max_samples=2000):
    df = pd.read_csv(csv_path)
    # Shuffle and subset for faster training demonstration
    df = df.sample(frac=1).reset_index(drop=True)
    if len(df) > max_samples:
        df = df.head(max_samples)
        
    X = []
    y = []
    
    for _, row in df.iterrows():
        features = extract_features(row['face_path'])
        if features is not None:
            X.append(features)
            # Label: Real -> 0 (LIVE), Fake -> 1 (SPOOF)
            y.append(0 if row['face_label'] == 'Real' else 1)
            
    return np.array(X), np.array(y)

if __name__ == "__main__":
    print("Loading training data (subset for speed)...")
    X_train, y_train = load_dataset(TRAIN_CSV, max_samples=2000)
    print(f"Loaded {len(X_train)} training samples.")
    
    print("Loading validation data...")
    X_val, y_val = load_dataset(VAL_CSV, max_samples=500)
    print(f"Loaded {len(X_val)} validation samples.")
    
    print("Training Face PAD Random Forest Model...")
    clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    clf.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred = clf.predict(X_val)
    acc = accuracy_score(y_val, y_pred)
    print(f"Validation Accuracy: {acc * 100:.2f}%")
    print(classification_report(y_val, y_pred, target_names=["LIVE (0)", "SPOOF (1)"]))
    
    print(f"Saving model to {MODEL_PATH}...")
    joblib.dump(clf, MODEL_PATH)
    print("Face PAD training complete.")
