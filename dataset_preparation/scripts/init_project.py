import os
import shutil
import pandas as pd
import hashlib

BASE_DIR = r"D:\7th Semester\Information Security\aadhaar-inspired-security"
CSV_PATH = r"D:\7th Semester\Information Security\aadhaar_dataset.csv"

# 1. Create Directory Structure
dirs = [
    "data/IdentityShield",
    "data/metadata",
    "models/face_pad",
    "models/face_verification",
    "models/fingerprint_pad",
    "models/fingerprint_matching",
    "preprocessing",
    "authentication",
    "database",
    "api",
    "frontend",
    "experiments",
    "results/metrics",
    "results/graphs",
    "results/confusion_matrices"
]

for d in dirs:
    os.makedirs(os.path.join(BASE_DIR, d), exist_ok=True)

# 2. Sanitize Dataset and Create Metadata
df = pd.read_csv(CSV_PATH)

sanitized_data = []

for idx, row in df.iterrows():
    # Use the actual Aadhaar number from the dataset for testing convenience
    # It's a float in the CSV (e.g., 10286165797.0), so we convert it to int then string
    try:
        synthetic_id = str(int(row['aadhaar_number']))
    except:
        synthetic_id = f"9001{idx:08d}"
        
    # Generate SHA-256 Hash
    hash_obj = hashlib.sha256(synthetic_id.encode())
    credential_hash = hash_obj.hexdigest()
    
    # Internal Identity ID
    identity_id = f"ID{idx:05d}"
    
    # Gather paths and labels
    face_path = row['face_path']
    fingerprint_path = row['fingerprint_path']
    face_label = row['face_label']
    fingerprint_label = row['fingerprint_label']
    
    sanitized_data.append({
        "identity_id": identity_id,
        "synthetic_id": synthetic_id,  # Keep this for the demo simulation later
        "credential_hash": credential_hash,
        "face_path": face_path,
        "face_label": face_label,
        "fingerprint_path": fingerprint_path,
        "fingerprint_label": fingerprint_label
    })

# Save to metadata
sanitized_df = pd.DataFrame(sanitized_data)
metadata_path = os.path.join(BASE_DIR, "data", "metadata", "identities.csv")
sanitized_df.to_csv(metadata_path, index=False)

# 3. Create dummy files to hold structure
with open(os.path.join(BASE_DIR, "README.md"), "w") as f:
    f.write("# Aadhaar-Inspired Digital Identity Verification\n\nA Multi-Layer Defense Framework Against Biometric Impersonation.")

print(f"Project structure initialized at {BASE_DIR}")
print(f"Sanitized metadata saved to {metadata_path} with {len(sanitized_df)} records.")
