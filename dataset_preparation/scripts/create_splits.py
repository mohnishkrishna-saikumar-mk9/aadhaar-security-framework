import os
import pandas as pd
from sklearn.model_selection import train_test_split

METADATA_PATH = r"D:\7th Semester\Information Security\aadhaar-inspired-security\data\metadata\identities.csv"
OUT_DIR = r"D:\7th Semester\Information Security\aadhaar-inspired-security\data\metadata"

df = pd.read_csv(METADATA_PATH)

# Combine labels to stratify effectively across both face and fingerprint classes
df['stratify_col'] = df['face_label'] + "_" + df['fingerprint_label']

# Split: 70% Train, 30% Temp
train_df, temp_df = train_test_split(df, test_size=0.30, random_state=42, stratify=df['stratify_col'])

# Split Temp into 15% Validation, 15% Test
val_df, test_df = train_test_split(temp_df, test_size=0.50, random_state=42, stratify=temp_df['stratify_col'])

# Drop the temporary stratify column
train_df = train_df.drop(columns=['stratify_col'])
val_df = val_df.drop(columns=['stratify_col'])
test_df = test_df.drop(columns=['stratify_col'])

# Save splits
train_df.to_csv(os.path.join(OUT_DIR, "train_split.csv"), index=False)
val_df.to_csv(os.path.join(OUT_DIR, "val_split.csv"), index=False)
test_df.to_csv(os.path.join(OUT_DIR, "test_split.csv"), index=False)

print(f"Dataset split completed successfully:")
print(f"Train: {len(train_df)} rows")
print(f"Validation: {len(val_df)} rows")
print(f"Test: {len(test_df)} rows")
