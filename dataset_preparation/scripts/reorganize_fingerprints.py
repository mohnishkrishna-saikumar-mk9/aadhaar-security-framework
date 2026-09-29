import os
import shutil
import pandas as pd

CSV_PATH = r"D:\7th Semester\Information Security\aadhaar_dataset.csv"
TARGET_DIR = r"D:\7th Semester\Information Security\dataset_preparation\sources\face-fingerprint-dataset\fingerprint"
REAL_DIR = os.path.join(TARGET_DIR, "real")
ALTERED_DIR = os.path.join(TARGET_DIR, "altered")

os.makedirs(REAL_DIR, exist_ok=True)
os.makedirs(ALTERED_DIR, exist_ok=True)

df = pd.read_csv(CSV_PATH)
moved_files = set()

for idx, row in df.iterrows():
    old_path = row['fingerprint_path']
    label = row['fingerprint_label']
    filename = os.path.basename(old_path)
    
    # Determine new directory based on label
    if label == 'Real':
        new_path = os.path.join(REAL_DIR, filename)
    else:
        new_path = os.path.join(ALTERED_DIR, filename)
        
    # Copy file if it hasn't been copied yet (some Real fingerprints might be duplicated)
    if new_path not in moved_files:
        try:
            # We use copy2 to preserve metadata, and because moving might fail if duplicated rows try to move the same source file twice
            shutil.copy2(old_path, new_path)
            moved_files.add(new_path)
        except Exception as e:
            print(f"Error copying {old_path} to {new_path}: {e}")
            
    # Update CSV with new path
    df.at[idx, 'fingerprint_path'] = new_path

# Save the updated CSV
df.to_csv(CSV_PATH, index=False)
print(f"Successfully copied exactly the {len(moved_files)} used fingerprint images!")
print("CSV has been updated with the new paths.")
