import os
import pandas as pd

CSV_PATH = r"D:\7th Semester\Information Security\aadhaar_dataset.csv"
SOCOFING_DIR = r"D:\7th Semester\Information Security\dataset_preparation\sources\SOCOFing"

# Load the CSV
df = pd.read_csv(CSV_PATH)

# Get all unique used fingerprint paths
used_fingerprints = set(df['fingerprint_path'].dropna().unique())
# Normalize paths for accurate comparison
used_fingerprints = {os.path.normpath(p) for p in used_fingerprints}

deleted_count = 0
retained_count = 0

# Walk through the SOCOFing directory
for root, dirs, files in os.walk(SOCOFING_DIR):
    for file in files:
        if file.endswith('.BMP'):
            file_path = os.path.normpath(os.path.join(root, file))
            if file_path not in used_fingerprints:
                try:
                    os.remove(file_path)
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
            else:
                retained_count += 1

print(f"Cleanup complete!")
print(f"Retained fingerprints: {retained_count} (Note: some are used multiple times)")
print(f"Deleted unused fingerprints: {deleted_count}")
