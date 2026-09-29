"""
Step 2 only: StyleGAN faces already extracted to stylegan_faces/.
Update aadhaar_dataset.csv — add face_label column.
For each of 4 groups (Real Male, Real Female, Fake Male, Fake Female):
  - First 1847 rows → keep existing face_path, face_label = Real
  - Last  1848 rows → replace face_path with StyleGAN image, face_label = Fake
"""

import os, csv
import cv2
import numpy as np
import pandas as pd
import random

PARQUET_DIR  = r"D:\7th Semester\Information Security\140k-Real-and-Fake-Faces\data"
STYLEGAN_DIR = r"D:\7th Semester\Information Security\stylegan_faces"
MALE_OUT     = os.path.join(STYLEGAN_DIR, "male")
FEMALE_OUT   = os.path.join(STYLEGAN_DIR, "female")
CSV_PATH     = r"D:\7th Semester\Information Security\aadhaar_dataset.csv"
ONNX_MODEL   = r"D:\7th Semester\Information Security\gender_googlenet.onnx"

NEED_PER_GENDER = 3696  # 1848 * 2 categories (Real+Fake) per gender

os.makedirs(MALE_OUT, exist_ok=True)
os.makedirs(FEMALE_OUT, exist_ok=True)

# ── Load ONNX gender model ───────────────────────────────────────────
print("Loading ONNX gender model...", flush=True)
gender_net = cv2.dnn.readNetFromONNX(ONNX_MODEL)
MODEL_MEAN = (104.0, 117.0, 123.0)
GENDER_LABELS = ['female', 'male']

def predict_gender(img_bgr):
    blob = cv2.dnn.blobFromImage(img_bgr, 1.0, (224, 224), MODEL_MEAN, swapRB=False)
    gender_net.setInput(blob)
    preds = gender_net.forward()
    return GENDER_LABELS[preds[0].argmax()]

print("StyleGAN faces already extracted. Skipping Step 1.", flush=True)


# ════════════════════════════════════════════════════════════════════
# STEP 2: Update CSV — add face_label column, assign StyleGAN paths
# ════════════════════════════════════════════════════════════════════
print("\n=== STEP 2: Updating aadhaar_dataset.csv ===", flush=True)

df = pd.read_csv(CSV_PATH)

# Get StyleGAN file lists
sg_male_files   = sorted(os.listdir(MALE_OUT))
sg_female_files = sorted(os.listdir(FEMALE_OUT))

random.seed(42)
random.shuffle(sg_male_files)
random.shuffle(sg_female_files)

sg_male_idx   = 0
sg_female_idx = 0

REAL_COUNT = 1847  # real face rows per group
FAKE_COUNT = 1848  # stylegan face rows per group

# Add face_label column (default Real)
df['face_label'] = 'Real'

# Process each of the 4 groups
for aadhaar_label in ['Real', 'Fake']:
    for gender in ['Male', 'Female']:
        mask = (df['label'] == aadhaar_label) & (df['gender'] == gender)
        group_indices = df[mask].index.tolist()

        print(f"  Group: Aadhaar={aadhaar_label}, Gender={gender} → {len(group_indices)} rows", flush=True)

        # First 1847 → keep face path, face_label = Real (already set)
        # Last 1848  → replace face path with StyleGAN, face_label = Fake
        fake_indices = group_indices[REAL_COUNT:]  # last 1848

        for idx in fake_indices:
            if gender == 'Male':
                if sg_male_idx >= len(sg_male_files):
                    print("  WARNING: ran out of StyleGAN male images!", flush=True)
                    break
                sg_path = os.path.join(MALE_OUT, sg_male_files[sg_male_idx])
                sg_male_idx += 1
            else:
                if sg_female_idx >= len(sg_female_files):
                    print("  WARNING: ran out of StyleGAN female images!", flush=True)
                    break
                sg_path = os.path.join(FEMALE_OUT, sg_female_files[sg_female_idx])
                sg_female_idx += 1

            df.at[idx, 'face_path']  = sg_path
            df.at[idx, 'face_label'] = 'Fake'

df.to_csv(CSV_PATH, index=False)

print("\n=== COMPLETE! ===", flush=True)
print(df.groupby(['label', 'gender', 'face_label']).size(), flush=True)
print(f"\nStyleGAN male assigned:   {sg_male_idx}", flush=True)
print(f"StyleGAN female assigned: {sg_female_idx}", flush=True)
