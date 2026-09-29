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
MODEL_PATH = os.path.join(BASE_DIR, "models", "fingerprint_pad", "rf_fp_pad.pkl")

def extract_features(image_path):
    """
    Extracts simple image features to distinguish GENUINE vs SPOOF fingerprints.
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None
        
    img = cv2.resize(img, (96, 96))
    
    # Calculate histogram
    hist = cv2.calcHist([img], [0], None, [32], [0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    
    # Calculate basic statistics
    mean_val = np.mean(img)
    std_val = np.std(img)
    
    features = np.hstack([hist, [mean_val, std_val]])
    return features

def load_dataset(csv_path, max_samples=2000):
    df = pd.read_csv(csv_path)
    df = df.sample(frac=1).reset_index(drop=True)
    if len(df) > max_samples:
        df = df.head(max_samples)
        
    X = []
    y = []
    
    for _, row in df.iterrows():
        features = extract_features(row['fingerprint_path'])
        if features is not None:
            X.append(features)
            # Label: Real -> 0 (GENUINE), Fake -> 1 (SPOOF)
            y.append(0 if row['fingerprint_label'] == 'Real' else 1)
            
    return np.array(X), np.array(y)

if __name__ == "__main__":
    print("Loading training data (subset for speed)...")
    X_train, y_train = load_dataset(TRAIN_CSV, max_samples=2000)
    print(f"Loaded {len(X_train)} training samples.")
    
    print("Loading validation data...")
    X_val, y_val = load_dataset(VAL_CSV, max_samples=500)
    print(f"Loaded {len(X_val)} validation samples.")
    
    print("Training Fingerprint PAD Random Forest Model...")
    clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    clf.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred = clf.predict(X_val)
    acc = accuracy_score(y_val, y_pred)
    print(f"Validation Accuracy: {acc * 100:.2f}%")
    print(classification_report(y_val, y_pred, target_names=["GENUINE (0)", "SPOOF (1)"]))
    
    print(f"Saving model to {MODEL_PATH}...")
    joblib.dump(clf, MODEL_PATH)
    print("Fingerprint PAD training complete.")
