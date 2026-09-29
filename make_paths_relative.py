import pandas as pd
import os

BASE_DIR = r"D:\7th Semester\Information Security\aadhaar-inspired-security"

# Function to fix a single path
def make_relative(path_str):
    if not isinstance(path_str, str): return path_str
    if "woman_3434.jpg" in path_str: return "demo_dataset/faces/woman_3434.jpg"
    if "man_6204.jpg" in path_str: return "demo_dataset/faces/man_6204.jpg"
    if "stylegan_male_00690.jpg" in path_str: return "demo_dataset/faces/stylegan_male_00690.jpg"
    if "540__F_Right_ring_finger.BMP" in path_str: return "demo_dataset/fingerprints/540__F_Right_ring_finger.BMP"
    if "529__M_Left_ring_finger.BMP" in path_str: return "demo_dataset/fingerprints/529__M_Left_ring_finger.BMP"
    if "326__M_Left_ring_finger_CR.BMP" in path_str: return "demo_dataset/fingerprints/326__M_Left_ring_finger_CR.BMP"
    return path_str # Fallback

# 1. Update attack_test_matrix.csv
matrix_path = os.path.join(BASE_DIR, "attack_test_matrix.csv")
df1 = pd.read_csv(matrix_path)
df1['Example Face Path'] = df1['Example Face Path'].apply(make_relative)
df1['Example FP Path'] = df1['Example FP Path'].apply(make_relative)
df1.to_csv(matrix_path, index=False)

# 2. Update demo_dataset/aadhaar_dataset.csv
aadhaar_path = os.path.join(BASE_DIR, "demo_dataset", "aadhaar_dataset.csv")
df2 = pd.read_csv(aadhaar_path)
df2['face_path'] = df2['face_path'].apply(make_relative)
df2['fingerprint_path'] = df2['fingerprint_path'].apply(make_relative)
df2.to_csv(aadhaar_path, index=False)

# 3. Update identities.csv
ident_path = os.path.join(BASE_DIR, "data", "metadata", "identities.csv")
df3 = pd.read_csv(ident_path)
df3['face_path'] = df3['face_path'].apply(make_relative)
df3['fingerprint_path'] = df3['fingerprint_path'].apply(make_relative)
df3.to_csv(ident_path, index=False)

print("All CSV paths successfully updated to use local relative repo paths!")
