"""
Assign face image paths to aadhaar_dataset.csv based on gender column.
- Male rows  → face-fingerprint-dataset/faces/man/
- Female rows → face-fingerprint-dataset/faces/woman/
Overwrites face_path column. Does not change any other column.
"""

import os
import pandas as pd
import random

MAN_DIR   = r"D:\7th Semester\Information Security\face-fingerprint-dataset\faces\man"
WOMAN_DIR = r"D:\7th Semester\Information Security\face-fingerprint-dataset\faces\woman"
CSV_PATH  = r"D:\7th Semester\Information Security\aadhaar_dataset.csv"

# Get sorted file lists
man_files   = sorted(f for f in os.listdir(MAN_DIR)   if f.lower().endswith(('.jpg', '.jpeg', '.png')))
woman_files = sorted(f for f in os.listdir(WOMAN_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png')))

print(f"Man images:   {len(man_files)}")
print(f"Woman images: {len(woman_files)}")

# Shuffle so assignment is random, not sequential
random.seed(42)
random.shuffle(man_files)
random.shuffle(woman_files)

df = pd.read_csv(CSV_PATH)
print(f"CSV rows: {len(df)}")
print(df.groupby('gender').size())

man_idx   = 0
woman_idx = 0

for i, row in df.iterrows():
    if row['gender'] == 'Male':
        if man_idx >= len(man_files):
            print(f"WARNING: ran out of man images at row {i}!")
            break
        df.at[i, 'face_path'] = os.path.join(MAN_DIR, man_files[man_idx])
        man_idx += 1
    elif row['gender'] == 'Female':
        if woman_idx >= len(woman_files):
            print(f"WARNING: ran out of woman images at row {i}!")
            break
        df.at[i, 'face_path'] = os.path.join(WOMAN_DIR, woman_files[woman_idx])
        woman_idx += 1

df.to_csv(CSV_PATH, index=False)
print(f"\nDone! Assigned {man_idx} male paths and {woman_idx} female paths.")
print(f"Sample male path:   {df[df['gender']=='Male']['face_path'].iloc[0]}")
print(f"Sample female path: {df[df['gender']=='Female']['face_path'].iloc[0]}")
